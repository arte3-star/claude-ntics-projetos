"""
Aplica branding NTICS final nos cards de um carrossel (Pillow):
  - Logo NTICS Projetos (branca) no canto superior esquerdo, sobre a foto
  - Pill arredondada com 'ntics.com.br' no canto inferior direito, acima da barra gradiente

USO:
  python tools/content-gen/aplicar_branding_ntics.py <slug-do-projeto>
  python tools/content-gen/aplicar_branding_ntics.py cultura-na-comunidade-rabobank

ENTRADA: output/marketing/carrosseis/cases/{slug}/01-capa.jpg ... 07-impacto.jpg (e os demais cards de conteudo)
SAIDA:   output/marketing/carrosseis/cases/{slug}/branded/NN-slug.jpg
         (os originais ficam intactos; o branded/ pode ser usado para publicacao)

Aplica apenas em cards de conteudo (01-07). Pula o CTA (08-cta.jpg), que ja tem identidade propria.
"""

import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path("g:/O meu disco/Claude-NTICS-Projetos")
LOGO_PATH = ROOT / "brand-book/site/assets/LOGO NTICS - BRANCA.png"
FONT_PATH = "C:/Windows/Fonts/arialbd.ttf"  # Arial Bold para a pill ntics.com.br

# Posicionamento relativo ao tamanho do card (1856x2304)
LOGO_TOP_PCT = 0.030     # 3% do topo
LOGO_LEFT_PCT = 0.035    # 3.5% da esquerda
LOGO_WIDTH_PCT = 0.220   # 22% da largura total

PILL_RIGHT_PCT = 0.035   # 3.5% da borda direita
PILL_BOTTOM_PCT = 0.030  # 3% da borda inferior (acima da barra gradiente)
PILL_TEXT = "ntics.com.br"
PILL_PAD_X_PCT = 0.025   # padding horizontal interno da pill (% da largura do card)
PILL_PAD_Y_PCT = 0.010   # padding vertical interno
PILL_FONT_PCT = 0.025    # tamanho da fonte (% da largura do card)
PILL_BORDER_PX = 3       # borda branca
PILL_BG_RGBA = (0, 95, 115, 230)  # teal escuro NTICS (#005F73) translucido


def aplicar_branding(card_path: Path, out_path: Path):
    card = Image.open(card_path).convert("RGBA")
    W, H = card.size

    # ===== LOGO NTICS no topo esquerdo =====
    logo = Image.open(LOGO_PATH).convert("RGBA")
    logo_w = int(W * LOGO_WIDTH_PCT)
    logo_h = int(logo.height * (logo_w / logo.width))
    logo_resized = logo.resize((logo_w, logo_h), Image.Resampling.LANCZOS)
    logo_x = int(W * LOGO_LEFT_PCT)
    logo_y = int(H * LOGO_TOP_PCT)
    card.paste(logo_resized, (logo_x, logo_y), logo_resized)

    # ===== PILL ntics.com.br no canto inferior direito =====
    draw = ImageDraw.Draw(card)
    font_size = int(W * PILL_FONT_PCT)
    try:
        font = ImageFont.truetype(FONT_PATH, font_size)
    except OSError:
        font = ImageFont.load_default()

    # Medir texto
    bbox = font.getbbox(PILL_TEXT)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    pad_x = int(W * PILL_PAD_X_PCT)
    pad_y = int(W * PILL_PAD_Y_PCT)
    pill_w = text_w + pad_x * 2
    pill_h = text_h + pad_y * 2 + bbox[1]  # bbox[1] e o offset do topo da fonte

    # Posicao da pill: subir um pouco para nao colidir com a barra gradiente (~2% do bottom)
    pill_x_right = int(W * (1 - PILL_RIGHT_PCT))
    pill_y_bottom = int(H * (1 - PILL_BOTTOM_PCT))
    pill_x = pill_x_right - pill_w
    pill_y = pill_y_bottom - pill_h

    # Pill com borda branca arredondada
    radius = pill_h // 2
    draw.rounded_rectangle(
        [(pill_x, pill_y), (pill_x + pill_w, pill_y + pill_h)],
        radius=radius,
        fill=PILL_BG_RGBA,
        outline=(255, 255, 255, 255),
        width=PILL_BORDER_PX,
    )
    # Texto centralizado verticalmente na pill
    text_x = pill_x + pad_x
    text_y = pill_y + pad_y - bbox[1] // 2
    draw.text((text_x, text_y), PILL_TEXT, fill=(255, 255, 255, 255), font=font)

    # Salvar como JPG (descartar canal alpha)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    card.convert("RGB").save(out_path, "JPEG", quality=92)
    print(f"  Salvo: {out_path}")


def main():
    if len(sys.argv) < 2:
        print("Uso: python aplicar_branding_ntics.py <slug>")
        print("Ex:  python aplicar_branding_ntics.py cultura-na-comunidade-rabobank")
        sys.exit(1)

    slug = sys.argv[1]
    cards_dir = ROOT / "output/marketing/carrosseis/cases" / slug
    out_dir = cards_dir / "branded"
    out_dir.mkdir(parents=True, exist_ok=True)

    if not cards_dir.exists():
        print(f"ERRO: pasta nao encontrada: {cards_dir}")
        sys.exit(1)

    # Aplica em cards 01-07 (conteudo). Pula CTA (08) que ja tem logo NTICS centralizada.
    aplicados = 0
    for card_file in sorted(cards_dir.glob("0[1-7]-*.jpg")):
        out_path = out_dir / card_file.name
        try:
            aplicar_branding(card_file, out_path)
            aplicados += 1
        except Exception as e:
            print(f"  ERRO em {card_file.name}: {e}")

    # CTA: copiar direto (sem modificar)
    cta = cards_dir / "08-cta.jpg"
    if cta.exists():
        import shutil
        shutil.copy2(cta, out_dir / "08-cta.jpg")
        print(f"  Copiado (sem branding): 08-cta.jpg")

    print(f"\nConcluido: {aplicados} cards com branding NTICS em {out_dir}")


if __name__ == "__main__":
    main()
