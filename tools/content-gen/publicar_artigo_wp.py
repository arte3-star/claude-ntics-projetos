#!/usr/bin/env python3
"""
publicar_artigo_wp.py — Publica artigo mensal no WordPress da NTICS via REST API.

Uso:
  # Dry-run: mostra payload sem postar
  python tools/content-gen/publicar_artigo_wp.py --dry-run \\
    --content-file tmp/artigo-m02-body.html \\
    --title "Por que investir em juventude..." \\
    --slug autoridade-e-conexao-juventude-esg \\
    --excerpt "Empresas que investem em juventude..." \\
    --hero output/marketing/artigos/hero-autoridade-e-conexao-m02.jpg \\
    --inline output/marketing/artigos/img-roda-conversa-comunidade.jpg

  # Publish: posta direto como status=publish
  python tools/content-gen/publicar_artigo_wp.py --publish ... (mesmos args)
"""

import argparse
import base64
import json
import mimetypes
import ssl
import sys
import urllib.request
from pathlib import Path

# Norton intercepta SSL no Windows
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

ROOT = Path(__file__).resolve().parents[2]

env = dict(
    l.split('=', 1) for l in (ROOT / '.env').read_text(encoding='utf-8').splitlines()
    if '=' in l and not l.startswith('#')
)
WP_URL = env['WP_URL']
AUTH = 'Basic ' + base64.b64encode(f"{env['WP_USER']}:{env['WP_APP_PASSWORD']}".encode()).decode()

# IDs descobertos via /wp-json/wp/v2 (confirmados em 2026-05-22)
CAT_ARTIGOS = 73
TAGS_PADRAO = [91, 89]  # ESG, RESPONSABILIDADE SOCIAL
AUTHOR_NTICS = 1


def upload_media(image_path: Path) -> dict:
    """Sobe imagem para a biblioteca de midia. Retorna dict com id, source_url, etc."""
    filename = image_path.name
    mime = mimetypes.guess_type(filename)[0] or 'image/jpeg'
    data = image_path.read_bytes()
    req = urllib.request.Request(
        f"{WP_URL}/wp-json/wp/v2/media",
        data=data,
        headers={
            'Authorization': AUTH,
            'Content-Type': mime,
            'Content-Disposition': f'attachment; filename="{filename}"',
        },
        method='POST',
    )
    r = urllib.request.urlopen(req, context=ctx, timeout=120).read()
    return json.loads(r)


def extract_article_inner(html: str) -> str:
    """Extrai o conteudo INTERNO do <article class="article-body"> (sem o wrapper).
    Se nao tiver wrapper, retorna o HTML inteiro."""
    import re
    m = re.search(r'<article[^>]*>(.*)</article>', html, re.DOTALL)
    return m.group(1).strip() if m else html.strip()


def replace_image_src(html: str, mapping: dict, key_to_filename: dict = None) -> str:
    """Substitui src de imagens pelos source_url do WP.
    Aceita tanto src="filename.jpg" quanto src="{img:KEY}"."""
    for local_basename, wp_url in mapping.items():
        html = html.replace(f'src="{local_basename}"', f'src="{wp_url}"')
    if key_to_filename:
        for key, filename in key_to_filename.items():
            wp_url = mapping.get(filename)
            if wp_url:
                html = html.replace('{img:' + key + '}', wp_url)
    return html


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--content-file', required=True, help='HTML body do artigo (com <article>)')
    p.add_argument('--title', required=True)
    p.add_argument('--slug', required=True)
    p.add_argument('--excerpt', default='')
    p.add_argument('--hero', required=True, help='Caminho local do hero (vira featured_media)')
    p.add_argument('--inline', action='append', default=[], help='Imagens inline (pode repetir)')
    p.add_argument('--dry-run', action='store_true', help='Nao publica, so imprime payload')
    p.add_argument('--publish', action='store_true', help='POST com status=publish')
    p.add_argument('--draft', action='store_true', help='POST com status=draft')
    p.add_argument('--update-id', type=int, help='Atualiza post existente ao inves de criar novo')
    p.add_argument('--prompts-file', help='JSON com array {key, filename, prompt} para resolver placeholders {img:KEY}')
    args = p.parse_args()

    if not (args.dry_run or args.publish or args.draft):
        sys.exit('ERRO: escolha --dry-run, --publish ou --draft')

    print(f"WP URL: {WP_URL}")
    print(f"Titulo: {args.title}")
    print(f"Slug:   {args.slug}")
    print(f"Hero:   {Path(args.hero).name}")
    print(f"Inline: {[Path(p).name for p in args.inline]}")
    print()

    # --- Upload de imagens ---
    media_mapping = {}  # basename local -> source_url WP
    hero_id = None

    if not args.dry_run:
        print("[1/3] Subindo imagens para biblioteca de midia WP...")
        hero_obj = upload_media(Path(args.hero))
        hero_id = hero_obj['id']
        media_mapping[Path(args.hero).name] = hero_obj['source_url']
        print(f"  Hero id={hero_obj['id']}  -> {hero_obj['source_url']}")
        for inline in args.inline:
            obj = upload_media(Path(inline))
            media_mapping[Path(inline).name] = obj['source_url']
            print(f"  Inline id={obj['id']}  -> {obj['source_url']}")
    else:
        # dry-run: nao sobe, simula mapping
        media_mapping[Path(args.hero).name] = f"[DRY-RUN: {Path(args.hero).name}]"
        for inline in args.inline:
            media_mapping[Path(inline).name] = f"[DRY-RUN: {Path(inline).name}]"

    # --- Preparar content HTML ---
    raw_html = Path(args.content_file).read_text(encoding='utf-8')
    inner = extract_article_inner(raw_html)
    key_to_filename = None
    if args.prompts_file:
        prompts = json.loads(Path(args.prompts_file).read_text(encoding='utf-8'))
        # Inferir slug do hero filename (--slug nao chega aqui em formato util)
        # Resolver "{slug}" nos filenames se tiver
        hero_slug = Path(args.hero).stem.replace('hero-', '')
        key_to_filename = {
            p['key']: p['filename'].replace('{slug}', hero_slug)
            for p in prompts
        }
    content_html = replace_image_src(inner, media_mapping, key_to_filename)

    payload = {
        'title': args.title,
        'slug': args.slug,
        'content': content_html,
        'excerpt': args.excerpt,
        'categories': [CAT_ARTIGOS],
        'tags': TAGS_PADRAO,
        'author': AUTHOR_NTICS,
        'status': 'publish' if args.publish else 'draft',
    }
    if hero_id:
        payload['featured_media'] = hero_id

    # --- Dry-run: so imprime ---
    if args.dry_run:
        print("[DRY-RUN] Payload que SERIA postado:")
        print(json.dumps({
            **payload,
            'content': f"[{len(content_html)} chars de HTML; preview 200: {content_html[:200]}...]",
        }, indent=2, ensure_ascii=False))
        print(f"\nTotal content size: {len(content_html)} chars")
        print("Para postar de verdade: trocar --dry-run por --publish ou --draft")
        return

    # --- Post (cria ou atualiza) ---
    if args.update_id:
        url = f"{WP_URL}/wp-json/wp/v2/posts/{args.update_id}"
        action = f"Atualizando post id={args.update_id}"
    else:
        url = f"{WP_URL}/wp-json/wp/v2/posts"
        action = f"Criando post com status={payload['status']}"
    print(f"\n[2/3] {action}...")
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(
        url,
        data=data,
        headers={'Authorization': AUTH, 'Content-Type': 'application/json'},
        method='POST',
    )
    try:
        r = urllib.request.urlopen(req, context=ctx, timeout=60).read()
        post = json.loads(r)
        print(f"\n[3/3] OK!")
        print(f"  id:     {post['id']}")
        print(f"  status: {post['status']}")
        print(f"  link:   {post['link']}")
        print(f"  edit:   {WP_URL}/wp-admin/post.php?post={post['id']}&action=edit")
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"ERRO HTTP {e.code}: {body[:800]}")
        sys.exit(1)


if __name__ == '__main__':
    main()
