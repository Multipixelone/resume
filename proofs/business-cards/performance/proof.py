"""Render this one Performance proof. No registry or application integration."""

from io import BytesIO
import hashlib
import json
from pathlib import Path
from typing import Any

import fitz
from fontTools.pens.cu2quPen import Cu2QuPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.ttLib import TTFont as Font, newTable
from PIL import Image, ImageOps, PngImagePlugin
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas
import zxingcpp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
# Proprietary and gitignored in the blog checkout; read in place, never copied here.
SABON = ROOT.parent / 'blog/static/fonts/sabon/Sabon Next Regular.woff2'
INK = '#2b2520'
RUST = '#b54a00'
PAPER = '#f7f4ed'
TRIM = (252, 144)
BLEED = 9
MARGIN = 18  # 0.25 inch, both sides of the front
# Type scale. The name is four times the contact size; PragmataPro at 8pt has
# the same x-height as Sabon Next at 10pt (4.4pt), so pronouns and contacts read as one size.
NAME = 40
CONTACT = 10
LABEL = 8
URL = 7  # the back's website address, a step under the pronouns
ROW = 24  # contact row pitch
NAME_CAP = 1434 / 2000  # Cooper Black "F" ink top, in em
CONTACT_CAP = 685 / 1000  # Sabon Next cap height, in em
LABEL_ASCENT = 1526 / 2048  # PragmataPro ascender, in em


def truetype(source):
    """ReportLab reads only TrueType outlines, so redraw Sabon's CFF glyphs as quadratics."""
    font = Font(source)
    glyphs = font.getGlyphSet()
    font['loca'] = newTable('loca')
    font['glyf'] = glyf = newTable('glyf')
    glyf.glyphOrder, glyf.glyphs = font.getGlyphOrder(), {}
    for name in glyf.glyphOrder:
        pen = TTGlyphPen(glyphs)
        glyphs[name].draw(Cu2QuPen(pen, 1, reverse_direction=True))
        glyf[name] = pen.glyph()
    del font['CFF ']
    font['maxp'].tableVersion = 0x00010000
    for field in ('maxZones', 'maxTwilightPoints', 'maxStorage', 'maxFunctionDefs',
                  'maxInstructionDefs', 'maxStackElements', 'maxSizeOfInstructions'):
        setattr(font['maxp'], field, int(field == 'maxZones'))
    font.sfntVersion, font.flavor = '\0\1\0\0', None
    data = BytesIO()
    font.save(data)
    data.seek(0)
    return data


def fonts():
    paths = {
        'Cooper': ROOT / 'website/scripts/fonts/cooper/Cooper-Black.ttf',
        'Contacts': SABON,
        'Labels': ROOT / 'src/fonts/PragmataPro_Mono_Regular_ligatures_0827.ttf',
    }
    assert SABON.exists(), f'Sabon Next not found at {SABON}'
    for name, path in paths.items():
        pdfmetrics.registerFont(TTFont(name, truetype(path) if path == SABON else str(path)))
    return {name: hashlib.sha256(path.read_bytes()).hexdigest() for name, path in paths.items()}


def rust_qr():
    source = Image.open(ROOT / 'metadata/qr-code.png').convert('L')
    decoded = zxingcpp.read_barcode(source)
    assert decoded is not None, 'Original QR could not be decoded'
    # Preserve every source pixel. The source has only a two-module margin;
    # extend it by two more modules to provide a full four-module quiet zone.
    assert source.size == (1537, 1537)
    padded = ImageOps.expand(source, border=106, fill=255)
    rgba = Image.new('RGBA', padded.size, RUST)
    rgba.putalpha(ImageOps.invert(padded))
    return rgba, decoded.text


def lettering(canvas, value, font, size, x, y, color=INK, centered=False):
    canvas.setFillColor(HexColor(color))
    canvas.setFont(font, size)
    if centered:
        canvas.drawCentredString(x, y, value)
    else:
        canvas.drawString(x, y, value)


def contact_icon(canvas, kind, x, y):
    """Ten-point outline marks; mail and Instagram follow the site's icon set."""
    canvas.saveState()
    canvas.translate(x, y)
    canvas.scale(10 / 24, -10 / 24)
    canvas.setStrokeColor(HexColor(RUST))
    canvas.setLineWidth(1.7)
    canvas.setLineCap(1)
    canvas.setLineJoin(1)
    if kind == 'mail':
        canvas.roundRect(2.8, 4.8, 18.4, 14.4, 2.2, stroke=1, fill=0)
        path = canvas.beginPath()
        path.moveTo(3.4, 6.4)
        path.lineTo(12, 12.5)
        path.lineTo(20.6, 6.4)
        canvas.drawPath(path)
    elif kind == 'phone':
        path = canvas.beginPath()
        path.moveTo(21, 16.5)
        path.lineTo(16, 14)
        path.lineTo(13.5, 16.5)
        path.curveTo(10.5, 15, 9, 13.5, 7.5, 10.5)
        path.lineTo(10, 8)
        path.lineTo(7.5, 3)
        path.lineTo(4, 3)
        path.curveTo(1, 3, 4, 12, 8, 16)
        path.curveTo(12, 20, 21, 23, 21, 20)
        path.close()
        canvas.drawPath(path)
    else:
        canvas.roundRect(3.2, 3.2, 17.6, 17.6, 5, stroke=1, fill=0)
        canvas.circle(12, 12, 4.1, stroke=1, fill=0)
        canvas.setFillColor(HexColor(RUST))
        canvas.circle(17.2, 6.8, 1.15, stroke=0, fill=1)
    canvas.restoreState()


def draw_front(canvas):
    # Website name proportions: 0.87em baseline spacing, surname inset 0.19em.
    # The pronouns sit the same distance under "Rutis" as "Rutis" sits under "Finn".
    leading = 0.87 * NAME
    drop = leading - NAME_CAP * NAME + LABEL_ASCENT * LABEL
    # Centre the block from the top of "Finn" to the last baseline.
    top = (TRIM[1] + NAME_CAP * NAME + leading + drop) / 2
    finn = top - NAME_CAP * NAME
    bottom = finn - leading - drop
    surname_x = MARGIN + 0.19 * NAME
    lettering(canvas, 'Finn', 'Cooper', NAME, MARGIN, finn)
    lettering(canvas, 'Rutis', 'Cooper', NAME, surname_x, finn - leading, RUST)
    lettering(canvas, 'they / them', 'Labels', LABEL, MARGIN, bottom)
    contacts = ('me@finnrut.is', '503-267-5052', '@finnrutis')
    text_x = TRIM[0] - MARGIN - max(pdfmetrics.stringWidth(c, 'Contacts', CONTACT) for c in contacts)
    icon_x = text_x - 1.5 * CONTACT
    # The perforation runs from the top of "Finn" to the pronoun baseline,
    # centred in the gutter, and starts and ends on a whole dash.
    rule_x = (surname_x + pdfmetrics.stringWidth('Rutis', 'Cooper', NAME) + icon_x) / 2
    dashes = round((top - bottom + 2.7) / 4.2)
    canvas.setStrokeColor(HexColor(RUST))
    canvas.setLineWidth(0.45)
    canvas.setDash([1.5, (top - bottom - 1.5 * dashes) / (dashes - 1)])
    canvas.line(rule_x, bottom, rule_x, top)
    canvas.setDash()
    # The contact rows are centred on the same line as the name block,
    # from the first row's cap height to the last baseline.
    middle = (TRIM[1] - CONTACT_CAP * CONTACT) / 2
    for kind, value, baseline in zip(('mail', 'phone', 'instagram'), contacts,
                                     (middle + ROW, middle, middle - ROW)):
        contact_icon(canvas, kind, icon_x, baseline + 8)
        lettering(canvas, value, 'Contacts', CONTACT, text_x, baseline)


def draw_back(canvas, qr):
    # 25 modules plus a four-module quiet zone each side. The website address's
    # tallest ink, the "i" dot, meets the quiet zone's edge without entering it;
    # the code and address are centred together.
    size = 96
    quiet = 4 * size / 33
    url_top = 1647 / 2048 * URL
    url_y = (TRIM[1] - (size - quiet + url_top)) / 2
    buffer = BytesIO()
    qr.save(buffer, format='PNG')
    canvas.drawImage(ImageReader(buffer), (TRIM[0] - size) / 2, url_y + url_top,
                     width=size, height=size, mask='auto')
    lettering(canvas, 'www.finnrut.is', 'Labels', URL, TRIM[0] / 2, url_y, centered=True)


def png_metadata(side, kind):
    metadata = PngImagePlugin.PngInfo()
    metadata.add_text('Title', f'Finn Rutis Performance card, {side}, {kind}')
    metadata.add_text('Source', 'proof.py; docs/business-cards.md; REFERENCE.md:9-18; DESIGN.md')
    metadata.add_text('Description', 'Code-rendered proof, not AI-generated imagery. '
                      'QR pixel pattern from metadata/qr-code.png; rust recolor with extended quiet zone. '
                      'Cooper*, Sabon Next, PragmataPro. Cream is preview-only.')
    metadata.add_text('impeccable:prompt',
                      f'Code-rendered {side} {kind} from proof.py, using the user-pinned '
                      'stacked-name front and centered-QR back. Text: REFERENCE.md:9-18 '
                      'and docs/business-cards.md. QR source: metadata/qr-code.png, '
                      'preserved pixel pattern recolored rust with four-module quiet zone. '
                      'Cooper Black, Sabon Next and PragmataPro. No image-generation model.')
    return metadata


def main():
    font_hashes = fonts()
    qr, destination = rust_qr()
    raw_pdf = BytesIO()
    page_size = (TRIM[0] + 2 * BLEED, TRIM[1] + 2 * BLEED)
    canvas = Canvas(raw_pdf, pagesize=page_size, initialFontName='Cooper',  # type: ignore[arg-type]
                    initialFontSize=NAME, pageCompression=1, invariant=1)
    canvas.setTitle('Finn Rutis - Performance business card proof')
    canvas.setAuthor('Finn Rutis')
    canvas.setSubject('Front then back; unprinted stock; 3.5 x 2 inch trim; 1/8 inch bleed')
    for draw in (draw_front, lambda c: draw_back(c, qr)):
        canvas.saveState()
        canvas.translate(BLEED, BLEED)
        draw(canvas)
        canvas.restoreState()
        canvas.showPage()
    canvas.save()
    doc = fitz.open(stream=raw_pdf.getvalue(), filetype='pdf')
    for page in doc:
        page.set_trimbox(fitz.Rect(9, 9, 261, 153))
        page.set_bleedbox(fitz.Rect(0, 0, 270, 162))
    output = HERE / 'performance-proof.pdf'
    doc.save(output, garbage=4, deflate=True)
    doc.close()
    doc = fitz.open(output)
    checks: dict[str, Any] = {'pdf': [], 'png': [], 'qr': {}, 'font_sha256': font_hashes,
              'sabon_source': str(SABON.relative_to(ROOT.parent))}
    expected = [
        ['Finn', 'Rutis', 'they / them', 'me@finnrut.is', '503-267-5052', '@finnrutis'],
        ['www.finnrut.is'],
    ]
    for i, side in enumerate(('front', 'back')):
        page = doc[i]
        assert tuple(page.mediabox) == (0, 0, 270, 162)
        assert tuple(page.trimbox) == (9, 9, 261, 153)
        assert tuple(page.bleedbox) == (0, 0, 270, 162)
        # Small icon dots may be filled; the stock must remain unpainted.
        assert not any(d['fill'] is not None and d['rect'].get_area() > 100
                       for d in page.get_drawings())
        assert page.get_text().splitlines() == expected[i]
        used_fonts = page.get_fonts(full=True)
        for font in used_fonts:
            assert doc.extract_font(font[0])[3], f'Unembedded font: {font}'
        # Crop only the render, keeping the saved PDF's bleed intact.
        page.set_cropbox(page.trimbox)
        pixels = page.get_pixmap(dpi=300, alpha=True)
        assert (pixels.width, pixels.height) == (1050, 600)
        # MuPDF uses premultiplied alpha. Its PNG encoder unpremultiplies it.
        transparent = Image.open(BytesIO(pixels.tobytes('png'))).convert('RGBA')
        assert transparent.getpixel((0, 0))[3] == 0
        assert transparent.getextrema()[3] == (0, 255)
        preview = Image.new('RGBA', transparent.size, PAPER)
        preview.alpha_composite(transparent)
        preview = preview.convert('RGB')
        for kind, image in [('ink', transparent), ('preview', preview)]:
            name = f'{side}-{kind}.png'
            image.save(HERE / name, dpi=(300, 300), pnginfo=png_metadata(side, kind))
            checks['png'].append({'file': name, 'pixels': image.size, 'mode': image.mode,
                                  'dpi': 300})
        small = preview.resize((336, 192), Image.Resampling.LANCZOS)
        small.save(HERE / f'{side}-actual-size.png', dpi=(96, 96),
                   pnginfo=png_metadata(side, '96 DPI actual-size inspection proxy'))
        # All visible ink, including the QR, must stay within 0.2 inches of trim.
        bbox = transparent.getbbox()
        safe_px = 60
        assert min(bbox[0], bbox[1], 1050 - bbox[2], 600 - bbox[3]) >= safe_px
        if side == 'back':
            for dpi, image in [(300, preview), (96, small)]:
                decoded = zxingcpp.read_barcode(image)
                assert decoded is not None, f'Rust QR failed at {dpi} DPI'
                assert decoded.text == destination
                checks['qr'][str(dpi)] = decoded.text
        checks['pdf'].append({'page': i + 1, 'side': side,
                              'media_pt': list(page.mediabox), 'trim_pt': list(page.trimbox),
                              'bleed_pt': list(page.bleedbox),
                              'text': expected[i], 'embedded_fonts': [f[3] for f in used_fonts],
                              'visible_ink_bounds_300dpi': bbox,
                              'minimum_ink_margin_in': min(bbox[0], bbox[1], 1050-bbox[2], 600-bbox[3])/300})
    assert len(doc) == 2
    checks['qr']['source_destination'] = destination
    checks['qr']['quiet_zone_modules'] = 4
    checks['qr']['qr_width_including_quiet_zone_in'] = 96 / 72
    checks['qr']['physical_stock_scan'] = 'Pending user print test; digital decode is not print certification.'
    checks['pdf_background'] = 'No page-sized fill; transparent QR whites; unprinted stock.'
    (HERE / 'validation.json').write_text(json.dumps(checks, indent=2) + '\n')
    print(json.dumps(checks, indent=2))


if __name__ == '__main__':
    main()
