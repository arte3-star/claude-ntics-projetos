"""
Gera carrossel NTICS via HTML/CSS + Playwright.

USO:
  python render.py <briefing-slug>
  python render.py conhecendo-os-ods-wilson-sons

ENTRADAS:
  briefings/{slug}.json    — variaveis por card
  template.html.jinja      — layout
  style.css                — identidade NTICS
  assets/                  — logos fixos

SAIDAS:
  output/{slug}/
    01-{label}.png         — cards 1856x2304
    ...
    08-{label}.png
    linkedin-carrossel.pdf — PDF unificado
"""

import asyncio
import json
import sys
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from urllib.parse import quote
from jinja2 import Template
from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = ROOT.parent.parent.parent  # tools/content-gen/carrossel-html/ → projeto


def file_url(path: Path) -> str:
    """Converte caminho local para file:// URL absoluto."""
    return "file:///" + str(path.resolve()).replace("\\", "/").replace(" ", "%20")


async def render_card(playwright_page, card, slug, idx, output_dir):
    """Renderiza um card como PNG 1856x2304."""
    tpl_text = (ROOT / "template.html.jinja").read_text(encoding="utf-8")
    # Inlinear CSS no <head> em vez de <link rel="stylesheet">
    css_text = (ROOT / "style.css").read_text(encoding="utf-8")
    tpl_text = tpl_text.replace(
        '<link rel="stylesheet" href="style.css">',
        f'<style>\n{css_text}\n</style>'
    )
    # Logo NTICS: caminho absoluto
    logo_url = file_url(ROOT / "assets" / "logo-ntics-branca.png")
    tpl_text = tpl_text.replace('src="assets/logo-ntics-branca.png"', f'src="{logo_url}"')

    tpl = Template(tpl_text)

    # Resolve foto relativa à raiz do projeto → absoluta
    foto_url = ""
    if card.get("foto"):
        foto_path = (PROJECT_ROOT / card["foto"]).resolve()
        if foto_path.exists():
            foto_url = file_url(foto_path)
        else:
            print(f"  AVISO: foto nao encontrada: {foto_path}")

    html = tpl.render(
        badge_text=card["badge_text"],
        badge_color=card["badge_color"],
        badge_text_color=card.get("badge_text_color", "#FFFFFF"),
        headline_line1=card["headline_line1"],
        headline_line2=card["headline_line2"],
        headline_color=card["headline_color"],
        body=card["body"],
        foto=foto_url,
    )

    # Salva HTML para debug e para que o browser resolva os caminhos relativos
    html_path = output_dir / f"_card_{idx:02d}.html"
    html_path.write_text(html, encoding="utf-8")

    # Navega e screenshot
    await playwright_page.goto(file_url(html_path))
    await playwright_page.wait_for_load_state("networkidle", timeout=30000)
    # Espera fontes carregarem
    await playwright_page.wait_for_function('document.fonts.ready', timeout=15000)
    await playwright_page.wait_for_timeout(800)

    png_path = output_dir / f"{idx:02d}-{card['label']}.png"
    # screenshot da viewport completa (1856x2304)
    await playwright_page.screenshot(path=str(png_path), full_page=False, clip={
        "x": 0, "y": 0, "width": 1856, "height": 2304
    })
    print(f"  [{idx:02d}] {card['label']:14s} → {png_path.name}")
    return png_path


async def main(slug):
    briefing_path = ROOT / "briefings" / f"{slug}.json"
    if not briefing_path.exists():
        print(f"ERRO: briefing nao encontrado: {briefing_path}")
        return

    briefing = json.loads(briefing_path.read_text(encoding="utf-8"))
    output_dir = ROOT / "output" / slug
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Renderizando: {briefing['titulo']}")
    print(f"Output: {output_dir}\n")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={"width": 1856, "height": 2304},
            device_scale_factor=1,
        )
        page = await context.new_page()

        pngs = []
        for idx, card in enumerate(briefing["cards"], start=1):
            png = await render_card(page, card, slug, idx, output_dir)
            pngs.append(png)

        await browser.close()

    # Gera PDF unificado
    from fpdf import FPDF
    pdf = FPDF(orientation="P", unit="mm", format=(210, 262.5))
    pdf.set_auto_page_break(False)
    for png in pngs:
        pdf.add_page()
        pdf.image(str(png), x=0, y=0, w=210, h=262.5)
    pdf_path = output_dir / "linkedin-carrossel.pdf"
    pdf.output(str(pdf_path))
    print(f"\nPDF: {pdf_path}")
    print(f"Concluido. {len(pngs)} cards + PDF em {output_dir}")


if __name__ == "__main__":
    slug = sys.argv[1] if len(sys.argv) > 1 else "conhecendo-os-ods-wilson-sons"
    asyncio.run(main(slug))
