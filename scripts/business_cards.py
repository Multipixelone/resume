"""Render the three shared business cards, independently of resume mappings.

Name and contact geometry is taken from
proofs/business-cards/performance/proof.py; the role and pronoun lines under
the name, and the back, were redrawn after it. The proof is not a runtime input
and is never modified. Sabon conversion stays in memory, not in a font asset.

Requires Python 3.11+, reportlab, PyMuPDF, Pillow, fonttools[woff], zxing-cpp.
No browser, Typst, external font converter, or image-generation service is used.
"""

import argparse
import hashlib
from io import BytesIO
import json
from pathlib import Path
import tomllib
from typing import Any

import fitz
from fontTools.pens.cu2quPen import Cu2QuPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.ttLib import TTFont as Font, newTable
from PIL import Image, ImageChops, ImageOps, PngImagePlugin
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas
import zxingcpp


ROOT = Path(__file__).resolve().parents[1]
SABON_RELATIVE = Path('blog/static/fonts/sabon/Sabon Next Regular.woff2')
INK = '#2b2520'
RUST = '#b54a00'
PAPER = '#f7f4ed'
TRIM = (252, 144)
BLEED = 9
MEDIA_BOX = (0, 0, 270, 162)
TRIM_BOX = (9, 9, 261, 153)
MARGIN = 18
NAME = 40
CONTACT = 10
URL = 7
ROW = 24
NAME_CAP = 1434 / 2000
CONTACT_CAP = 685 / 1000
SIDES = ('front', 'back')
# This is a card-content schema, not a second resume variant registry.
PROFILE_FIELDS = {
    'performance': ('email', 'phone', 'instagram'),
    'technology': ('email', 'github'),
    'work': ('email', 'phone'),
}
# A profile may print one role line, in Finn's words. Under the name, the role
# (true small caps, letterspaced to span the name) and the pronouns (italic, in
# Faded Ink) form one quiet Sabon tier. A missing role prints only the pronouns.
# A headshot, a repository path, prints on that profile's back beside the QR.
OPTIONAL_FIELDS = ('role', 'headshot')
MUTED = '#6f6456'
ROLE = 8
PRONOUNS = 8.5
UNDER_NAME = 9  # From the surname baseline to the first small line's x-height.
LINE_STEP = 11
SMALL_CAP = 457 / 1000
ITALIC_X = 454 / 1000
SURNAME_RSB = 50 / 2000  # Cooper Black "s": the role ends on the surname's ink.
ROLE_TRACKING = (0.04, 0.14)  # em
SMALL_CAPS_SUFFIX = 'SC'
# The QR is 25 modules inside a four-module quiet zone. The address under it
# keeps two of those modules clear, the source PNG's own quiet zone, so it
# reads as the code's caption; the other three sides keep all four.
QR_SIZE = 96
MODULE = QR_SIZE / 33
SYMBOL = 25 * MODULE
CAPTION_GAP = 2 * MODULE
URL_TOP = 1647 / 2048  # PragmataPro "i" dot, the address's tallest ink.
# A theatre 8x10 (4:5) at the full safe height, standing at the margins.
HEADSHOT = (MARGIN, MARGIN, 0.8 * (TRIM[1] - 2 * MARGIN), TRIM[1] - 2 * MARGIN)
HEADSHOT_PPI = 600


def require(condition, message):
    """Production checks must still run under python -O."""
    if not condition:
        raise ValueError(message)


def text_table(value, keys, context):
    require(isinstance(value, dict) and set(value) == set(keys),
            f'{context}: expected exactly {", ".join(keys)}')
    for key, text in value.items():
        require(isinstance(text, str) and bool(text) and text == text.strip()
                and all(32 <= ord(c) < 127 for c in text),
                f'{context}.{key}: expected nonempty, single-line ASCII text')


def load_profiles(path):
    with Path(path).open('rb') as source:
        data = tomllib.load(source)
    require(set(data) == {'identity', 'back', 'profiles'},
            'profiles.toml: expected identity, back, and profiles tables only')
    text_table(data['identity'], ('first_name', 'last_name', 'pronouns'), 'identity')
    text_table(data['back'], ('address', 'destination'), 'back')
    require(data['back']['destination'] == 'https://finnrut.is',
            'back.destination must be the approved https://finnrut.is')
    profiles = data['profiles']
    require(isinstance(profiles, dict) and set(profiles) == set(PROFILE_FIELDS),
            'expected exactly performance, technology, and work card profiles')
    for name, fields in PROFILE_FIELDS.items():
        profile = profiles[name]
        require(isinstance(profile, dict), f'profiles.{name}: expected a table')
        optional = tuple(key for key in OPTIONAL_FIELDS if key in profile)
        text_table(profile, fields + optional, f'profiles.{name}')
    return data


def contacts_for(profile):
    # The explicit order is independent of TOML key order.
    return tuple(('mail' if key == 'email' else key, profile[key])
                 for key in ('email', 'phone', 'instagram', 'github') if key in profile)


def contact_baselines(count):
    require(count in (2, 3), 'expected two or three contact rows')
    middle = (TRIM[1] - CONTACT_CAP * CONTACT) / 2
    return tuple(middle + ((count - 1) / 2 - i) * ROW for i in range(count))


def truetype(source):
    """The proof's CFF-to-quadratic conversion, entirely in memory.

    Also accept a supplied TTF or TrueType WOFF2 without converting its outlines.
    """
    with Font(source) as font:
        if 'CFF ' in font:
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
        require('glyf' in font, 'Sabon font must have CFF or TrueType outlines')
        font.sfntVersion, font.flavor = '\0\1\0\0', None
        data = BytesIO()
        font.save(data)
    data.seek(0)
    return data


def font_paths(root, sabon):
    paths = {
        'Cooper': root / 'website/scripts/fonts/cooper/Cooper-Black.ttf',
        'Contacts': sabon,
        # The role uses the regular file's own small caps; pronouns use the
        # italic beside it.
        'SmallCaps': sabon,
        'Italic': sabon.with_name('Sabon Next Italic.woff2'),
        'Labels': root / 'src/fonts/PragmataPro_Mono_Regular_ligatures_0827.ttf',
    }
    require(sabon.is_file(), f'Sabon Next not found at {sabon}. Supply --sabon FONT_PATH '
            '(a licensed local font file). The renderer does not download or copy it.')
    for name, path in paths.items():
        require(path.is_file(), f'{name} font not found at {path}')
    return paths


def small_caps(source):
    """Map a-z to the font's true small caps, in memory like truetype().

    Runs before truetype(), whose TrueType output has no glyph names. PDF text
    still extracts as the original lowercase string.
    """
    with Font(source) as font:
        caps = {code: f'{chr(code)}.sc' for code in range(ord('a'), ord('z') + 1)}
        require(set(caps.values()) <= set(font.getGlyphOrder()),
                'Sabon font must include true small caps (a.sc to z.sc)')
        for table in font['cmap'].tables:
            if table.isUnicode():
                table.cmap.update(caps)
        # ReportLab treats fonts with one face name as one font, so rename it.
        for record in font['name'].names:
            if record.nameID == 6:
                record.string = record.toUnicode() + SMALL_CAPS_SUFFIX
        font.flavor = None
        data = BytesIO()
        font.save(data)
    data.seek(0)
    return data


def register_fonts(paths):
    loaders = {'Contacts': truetype, 'Italic': truetype,
               'SmallCaps': lambda path: truetype(small_caps(path))}
    for name, path in paths.items():
        pdfmetrics.registerFont(TTFont(name, loaders[name](path) if name in loaders else str(path)))
    return {name: hashlib.sha256(path.read_bytes()).hexdigest() for name, path in paths.items()}


def rust_qr(path, destination):
    with Image.open(path) as image:
        source = image.convert('L')
    decoded = zxingcpp.read_barcode(source)
    require(decoded is not None and decoded.text == destination,
            f'Original QR must decode to {destination}')
    # Preserve the approved pixel pattern and add the same two-module padding.
    # 29 source modules (25 + 2 each side), 53 px per module; 33 padded modules.
    require(source.size == (1537, 1537), 'QR source size changed; review its module geometry')
    quiet_border = Image.new('L', source.size, 255)
    quiet_border.paste(source.crop((106, 106, 1431, 1431)), (106, 106))
    require(ImageChops.difference(source, quiet_border).getbbox() is None,
            'QR source two-module quiet zone is not white')
    padded = ImageOps.expand(source, border=106, fill=255)
    rgba = Image.new('RGBA', padded.size, RUST)
    rgba.putalpha(ImageOps.invert(padded))
    return rgba


def headshot_image(root, relative):
    """Crop the headshot to its 4:5 print and embed it as a 600 ppi JPEG.

    The sides are trimmed evenly to keep the photographer's framing, and the
    top is kept so the hair is never cut. Under 300 ppi at card size fails.
    """
    root = Path(root).resolve()
    path = (root / relative).resolve()
    require(path.is_relative_to(root) and path.is_file(), f'Headshot not found in the repository: {relative}')
    with Image.open(path) as source:
        photo = ImageOps.exif_transpose(source).convert('RGB')
    width, height = HEADSHOT[2:]
    crop_width = min(photo.width, photo.height * width / height)
    crop_height = crop_width * height / width
    pixels = (round(width / 72 * HEADSHOT_PPI), round(height / 72 * HEADSHOT_PPI))
    require(crop_width >= pixels[0] / 2 and crop_height >= pixels[1] / 2,
            f'Headshot is under 300 ppi at card size: {relative}')
    left = (photo.width - crop_width) / 2
    photo = photo.crop((round(left), 0, round(left + crop_width), round(crop_height)))
    buffer = BytesIO()
    photo.resize(pixels, Image.Resampling.LANCZOS).save(buffer, format='JPEG', quality=92, subsampling=0)
    buffer.seek(0)
    # ReportLab embeds a JPEG reader's bytes as they are, without recompressing.
    return ImageReader(buffer)


def lettering(canvas, value, font, size, x, y, color=INK, centered=False, tracking=0):
    canvas.setFillColor(HexColor(color))
    canvas.setFont(font, size)
    if centered:
        canvas.drawCentredString(x, y, value)
    elif tracking:
        canvas.drawString(x, y, value, charSpace=tracking)
    else:
        canvas.drawString(x, y, value)


def contact_icon(canvas, kind, x, y):
    """Approved ten-point marks, plus a matching original GitHub cat outline."""
    require(kind in ('mail', 'phone', 'instagram', 'github'), f'Unknown contact icon: {kind}')
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
    elif kind == 'instagram':
        canvas.roundRect(3.2, 3.2, 17.6, 17.6, 5, stroke=1, fill=0)
        canvas.circle(12, 12, 4.1, stroke=1, fill=0)
        canvas.setFillColor(HexColor(RUST))
        canvas.circle(17.2, 6.8, 1.15, stroke=0, fill=1)
    else:
        # Cat ears, broad head, neck/legs and curling tail distinguish this from
        # Instagram's rounded camera. Drawn here rather than loading a new asset.
        path = canvas.beginPath()
        path.moveTo(9, 21)
        path.lineTo(9, 18)
        path.curveTo(9, 16.6, 9.6, 15.8, 10.1, 15.5)
        path.curveTo(5.2, 15.2, 3.2, 13.5, 3.2, 9.8)
        path.curveTo(3.2, 8.3, 3.8, 7.1, 4.8, 6.1)
        path.curveTo(4.4, 5, 4.5, 3.4, 5, 2.5)
        path.curveTo(6.8, 2.5, 8.5, 3.6, 9.1, 4.1)
        path.curveTo(11, 3.6, 13, 3.6, 14.9, 4.1)
        path.curveTo(15.5, 3.6, 17.2, 2.5, 19, 2.5)
        path.curveTo(19.5, 3.4, 19.6, 5, 19.2, 6.1)
        path.curveTo(20.2, 7.1, 20.8, 8.3, 20.8, 9.8)
        path.curveTo(20.8, 13.5, 18.8, 15.2, 13.9, 15.5)
        path.curveTo(14.4, 15.8, 15, 16.6, 15, 18)
        path.lineTo(15, 21)
        path.moveTo(9, 18.7)
        path.curveTo(5.7, 19.6, 4.6, 18.4, 3.8, 16.7)
        path.curveTo(3.2, 15.5, 2.3, 15.3, 1.8, 15.3)
        canvas.drawPath(path)
    canvas.restoreState()


def role_tracking(role, span):
    """Letterspace the small caps role so it runs from the margin to `span`."""
    natural = pdfmetrics.stringWidth(role, 'SmallCaps', ROLE)
    tracking = (span - MARGIN - natural) / max(len(role) - 1, 1)
    require(tracking >= ROLE_TRACKING[0] * ROLE, 'Role line is wider than the name; shorten it')
    # A short role stays at the widest readable spacing and ends before the name.
    return min(tracking, ROLE_TRACKING[1] * ROLE)


def draw_front(canvas, identity, profile):
    # The name keeps the approved proof geometry. Below it, the role and the
    # pronouns share the margin; the block is centred from the top of "Finn"
    # to the pronoun baseline.
    leading = 0.87 * NAME
    role = profile.get('role')
    under = UNDER_NAME + (SMALL_CAP * ROLE + LINE_STEP if role else ITALIC_X * PRONOUNS)
    top = (TRIM[1] + NAME_CAP * NAME + leading + under) / 2
    finn = top - NAME_CAP * NAME
    bottom = finn - leading - under
    surname_x = MARGIN + 0.19 * NAME
    surname_end = surname_x + pdfmetrics.stringWidth(identity['last_name'], 'Cooper', NAME)
    lettering(canvas, identity['first_name'], 'Cooper', NAME, MARGIN, finn)
    lettering(canvas, identity['last_name'], 'Cooper', NAME, surname_x, finn - leading, RUST)
    if role:
        tracking = role_tracking(role, surname_end - SURNAME_RSB * NAME)
        lettering(canvas, role, 'SmallCaps', ROLE, MARGIN, bottom + LINE_STEP, tracking=tracking)
    lettering(canvas, identity['pronouns'], 'Italic', PRONOUNS, MARGIN, bottom, MUTED)
    contacts = contacts_for(profile)
    text_x = TRIM[0] - MARGIN - max(pdfmetrics.stringWidth(value, 'Contacts', CONTACT)
                                   for _, value in contacts)
    icon_x = text_x - 1.5 * CONTACT
    require(icon_x > surname_end + 2, 'Contact column overlaps the name; review layout')
    rule_x = (surname_end + icon_x) / 2
    dashes = round((top - bottom + 2.7) / 4.2)
    canvas.setStrokeColor(HexColor(RUST))
    canvas.setLineWidth(0.45)
    canvas.setDash([1.5, (top - bottom - 1.5 * dashes) / (dashes - 1)])
    canvas.line(rule_x, bottom, rule_x, top)
    canvas.setDash()
    for (kind, value), baseline in zip(contacts, contact_baselines(len(contacts))):
        contact_icon(canvas, kind, icon_x, baseline + 8)
        lettering(canvas, value, 'Contacts', CONTACT, text_x, baseline)


def draw_back(canvas, qr, back, headshot=None):
    # The code and its address are centred together on the card's height. A
    # headshot stands at the safe margins, and the code then sits midway
    # between the print and the card's right edge.
    url_y = (TRIM[1] - (SYMBOL + CAPTION_GAP + URL_TOP * URL)) / 2
    middle = TRIM[0] / 2
    if headshot is not None:
        x, y, width, height = HEADSHOT
        canvas.drawImage(headshot, x, y, width=width, height=height)
        middle = (x + width + TRIM[0]) / 2
    buffer = BytesIO()
    qr.save(buffer, format='PNG')
    canvas.drawImage(ImageReader(buffer), middle - QR_SIZE / 2,
                     url_y + URL_TOP * URL + CAPTION_GAP - 4 * MODULE,
                     width=QR_SIZE, height=QR_SIZE, mask='auto')
    lettering(canvas, back['address'], 'Labels', URL, middle, url_y, centered=True)


def png_metadata(profile, side, kind, headshot=None):
    metadata = PngImagePlugin.PngInfo()
    metadata.add_text('Title', f'Finn Rutis {profile} card, {side}, {kind}')
    metadata.add_text('Source', 'scripts/business_cards.py; cards/profiles.toml; '
                      'proofs/business-cards/performance/proof.py; REFERENCE.md; DESIGN.md'
                      + (f'; {headshot}' if headshot else ''))
    description = ('Code-rendered artwork, not AI-generated imagery. Stacked-name front. '
                   + (f'Back: the photographed headshot from {headshot}, cropped to 4:5, beside the QR. '
                      if headshot else 'Back: centered QR. ')
                   + 'QR pixels from metadata/qr-code.png; rust recolor with four-module quiet zone, '
                   'two above the website address. '
                   'Cooper Black, Sabon Next, PragmataPro. Cream is preview-only.')
    metadata.add_text('Description', description)
    metadata.add_text('impeccable:prompt', f'{side} {kind}: {description}')
    return metadata


def render_pdf(path, identity, profile, back, qr, headshot=None):
    raw_pdf = BytesIO()
    canvas = Canvas(raw_pdf, pagesize=(270, 162), initialFontName='Cooper',  # type: ignore[arg-type]
                    initialFontSize=NAME, pageCompression=1, invariant=1)
    canvas.setTitle('Finn Rutis - business card')
    canvas.setAuthor('Finn Rutis')
    canvas.setSubject('Front then back; unprinted stock; 3.5 x 2 inch trim; 1/8 inch bleed')
    for draw in (lambda c: draw_front(c, identity, profile), lambda c: draw_back(c, qr, back, headshot)):
        canvas.saveState()
        canvas.translate(BLEED, BLEED)
        draw(canvas)
        canvas.restoreState()
        canvas.showPage()
    canvas.save()
    with fitz.open(stream=raw_pdf.getvalue(), filetype='pdf') as doc:
        for page in doc:
            page.set_trimbox(fitz.Rect(TRIM_BOX))
            page.set_bleedbox(fitz.Rect(MEDIA_BOX))
        doc.save(path, garbage=4, deflate=True)


def page_ink(page):
    # Crop only the in-memory render, never the saved PDF's bleed.
    page.set_cropbox(page.trimbox)
    pixels = page.get_pixmap(dpi=300, alpha=True)
    # MuPDF has premultiplied alpha; its PNG encoder unpremultiplies it.
    return Image.open(BytesIO(pixels.tobytes('png'))).convert('RGBA')


def paper_preview(ink):
    preview = Image.new('RGBA', ink.size, PAPER)
    preview.alpha_composite(ink)
    return preview.convert('RGB')


def export_pngs(pdf, directory, profile, headshot=None):
    with fitz.open(pdf) as doc:
        for page, side in zip(doc, SIDES):
            ink = page_ink(page)
            preview = paper_preview(ink)
            small = preview.resize((336, 192), Image.Resampling.LANCZOS)
            for kind, image, dpi in (('ink', ink, 300), ('preview', preview, 300),
                                     ('actual-size', small, 96)):
                image.save(directory / f'{side}-{kind}.png', dpi=(dpi, dpi),
                           pnginfo=png_metadata(profile, side, kind, headshot))


def validate_pdf_page(doc, page, expected, side) -> dict[str, Any]:
    for box, expected_box in (('mediabox', MEDIA_BOX), ('trimbox', TRIM_BOX),
                              ('bleedbox', MEDIA_BOX), ('cropbox', MEDIA_BOX)):
        require(tuple(getattr(page, box)) == expected_box, f'{side}: incorrect PDF {box}')
    require(page.rotation == 0, f'{side}: unexpected PDF rotation')
    require(page.get_text().splitlines() == expected, f'{side}: PDF text/order differs from profile')
    # Small icon dots are filled. Large filled shapes would paint the stock.
    require(not any(d['fill'] is not None and d['rect'].get_area() > 100
                    for d in page.get_drawings()), f'{side}: unexpected PDF background fill')
    used_fonts = page.get_fonts(full=True)
    require(bool(used_fonts), f'{side}: missing PDF fonts')
    for font in used_fonts:
        require(bool(doc.extract_font(font[0])[3]), f'{side}: unembedded font {font[3]}')
    # No crop marks, stray vectors, or hidden artwork may sit outside the safe area.
    full = page.get_pixmap(dpi=72, alpha=True)
    full_ink = Image.open(BytesIO(full.tobytes('png'))).convert('RGBA').getchannel('A').getbbox()
    require(full_ink is not None and min(full_ink[0] - BLEED, full_ink[1] - BLEED,
            270 - BLEED - full_ink[2], 162 - BLEED - full_ink[3]) >= 14,
            f'{side}: ink outside safe area or marks in bleed')
    return {'side': side, 'media_pt': list(page.mediabox), 'trim_pt': list(page.trimbox),
            'bleed_pt': list(page.bleedbox), 'text': expected,
            'embedded_fonts': [f[3] for f in used_fonts]}


def read_png(path, mode, size, dpi):
    with Image.open(path) as source:
        require(source.format == 'PNG' and source.mode == mode and source.size == size,
                f'{path.name}: expected {mode} PNG at {size}')
        resolution = source.info.get('dpi', ())
        require(len(resolution) == 2 and all(abs(v - dpi) < 0.02 for v in resolution),
                f'{path.name}: expected {dpi} DPI metadata')
        require(all(source.info.get(key) for key in ('Title', 'Source', 'Description', 'impeccable:prompt')),
                f'{path.name}: missing provenance metadata')
        return source.copy()


def same_pixels(actual, expected, message):
    require(actual.mode == expected.mode and actual.size == expected.size
            and actual.tobytes() == expected.tobytes(), message)


def validate_ink(ink, side):
    alpha = ink.getchannel('A')
    require(alpha.getextrema() == (0, 255), f'{side}: ink must contain transparent and opaque pixels')
    bbox = alpha.getbbox()
    margin = min(bbox[0], bbox[1], ink.width - bbox[2], ink.height - bbox[3])
    require(margin >= 60, f'{side}: visible ink must be at least 0.2 inches inside trim')
    return bbox, margin / 300


def headshot_evidence(page, profile):
    # The QR is a Flate image; only a headshot is embedded as JPEG. ReportLab
    # wraps both in ASCII85, so read each image's whole filter chain.
    photos = [image[2:4] for image in page.get_images(full=True)
              if '/DCTDecode' in page.parent.xref_get_key(image[0], 'Filter')[1]]
    pixels = tuple(round(n / 72 * HEADSHOT_PPI) for n in HEADSHOT[2:])
    require(photos == ([pixels] if 'headshot' in profile else []),
            'back: a headshot must print once, at 600 ppi, exactly where the profile names one')
    if not photos:
        return {}
    return {'headshot': profile['headshot'], 'headshot_pixels': list(pixels), 'headshot_ppi': HEADSHOT_PPI}


def decode_qr(image, destination, context):
    decoded = zxingcpp.read_barcode(image)
    if decoded is None or decoded.text != destination:
        raise ValueError(f'{context}: rust QR did not decode to {destination}')
    return decoded.text


def artifact_names(profile):
    return {f'{profile}.pdf', 'validation.json'} | {
        f'{side}-{kind}.png' for side in SIDES for kind in ('ink', 'preview', 'actual-size')}


def validate_artifacts(directory, profile_name, identity, profile, back):
    """Reopen the delivered files, fail closed, and return measured evidence.

    This validates structure and digital QR decoding, not press compliance or
    physical-stock readability. The caller writes validation.json only on success.
    """
    actual_files = {p.name for p in directory.iterdir()}
    required = artifact_names(profile_name) - {'validation.json'}
    require(required <= actual_files <= artifact_names(profile_name),
            f'{profile_name}: unexpected or missing output files')
    expected = [[identity['first_name'], identity['last_name'],
                 *((profile['role'],) if 'role' in profile else ()), identity['pronouns'],
                 *(value for _, value in contacts_for(profile))], [back['address']]]
    checks: dict[str, Any] = {'profile': profile_name, 'pdf': [], 'png': [], 'qr': {}}
    with fitz.open(directory / f'{profile_name}.pdf') as doc:
        require(len(doc) == 2, f'{profile_name}: PDF must have exactly two pages')
        for i, side in enumerate(SIDES):
            page = doc[i]
            evidence = validate_pdf_page(doc, page, expected[i], side)
            ink = read_png(directory / f'{side}-ink.png', 'RGBA', (1050, 600), 300)
            preview = read_png(directory / f'{side}-preview.png', 'RGB', (1050, 600), 300)
            small = read_png(directory / f'{side}-actual-size.png', 'RGB', (336, 192), 96)
            same_pixels(ink, page_ink(page), f'{side}: ink PNG differs from PDF')
            same_pixels(preview, paper_preview(ink), f'{side}: preview differs from ink on cream')
            same_pixels(small, preview.resize((336, 192), Image.Resampling.LANCZOS),
                        f'{side}: actual-size proxy differs from preview')
            if side == 'front' and 'role' in profile:
                require(any(font.endswith(SMALL_CAPS_SUFFIX) for font in evidence['embedded_fonts']),
                        'front: role line is not set in the small caps face')
            if side == 'back':
                evidence.update(headshot_evidence(page, profile))
            bbox, margin = validate_ink(ink, side)
            evidence.update(page=i + 1, visible_ink_bounds_300dpi=bbox, minimum_ink_margin_in=margin)
            checks['pdf'].append(evidence)
            for kind, image, dpi in (('ink', ink, 300), ('preview', preview, 300),
                                     ('actual-size', small, 96)):
                checks['png'].append({'file': f'{side}-{kind}.png', 'pixels': image.size,
                                      'mode': image.mode, 'dpi': dpi})
            if side == 'back':
                for dpi, image in ((300, preview), (96, small)):
                    checks['qr'][str(dpi)] = decode_qr(image, back['destination'], f'{dpi} DPI')
    checks['qr'].update(source_destination=back['destination'], quiet_zone_modules=4,
                        address_clearance_modules=CAPTION_GAP / MODULE,
                        qr_width_including_quiet_zone_in=QR_SIZE / 72,
                        physical_stock_scan='Pending user print test; digital decode is not print certification.')
    checks['pdf_background'] = 'No page-sized fill; transparent QR whites; unprinted stock.'
    checks['print_compliance'] = 'RGB artwork, not PDF/X or CMYK certification; confirm printer specifications.'
    return checks


def check_output(root, output, names):
    require(output != root and output not in root.parents, 'Output must be a dedicated artifact directory')
    for protected in (root / 'proofs', root / 'fonts'):
        require(not output.is_relative_to(protected), 'Output must not overwrite original proofs or fonts')
    for name in names:
        directory = output / name
        require(not directory.is_symlink(), f'Refusing symlink output directory: {directory}')
        if directory.exists():
            require(directory.is_dir(), f'Output is not a directory: {directory}')
            require({p.name for p in directory.iterdir()} <= artifact_names(name),
                    f'Refusing unrelated files in {directory}')
            for path in directory.iterdir():
                require(path.is_file() and not path.is_symlink(), f'Refusing non-file or symlink output: {path}')


def render_all(root, output, sabon):
    root, output, sabon = (Path(path).expanduser().resolve() for path in (root, output, sabon))
    data = load_profiles(root / 'cards/profiles.toml')
    paths = font_paths(root, sabon)
    check_output(root, output, data['profiles'])
    hashes = register_fonts(paths)
    qr_path = root / 'metadata/qr-code.png'
    qr = rust_qr(qr_path, data['back']['destination'])
    # All profiles are emitted once. No registry lookup, variant aliases, or labels.
    for name, profile in data['profiles'].items():
        directory = output / name
        directory.mkdir(parents=True, exist_ok=True)
        report = directory / 'validation.json'
        report.unlink(missing_ok=True)  # Do not leave a stale success report after a failed rerender.
        pdf = directory / f'{name}.pdf'
        headshot = headshot_image(root, profile['headshot']) if 'headshot' in profile else None
        render_pdf(pdf, data['identity'], profile, data['back'], qr, headshot)
        export_pngs(pdf, directory, name, profile.get('headshot'))
        checks = validate_artifacts(directory, name, data['identity'], profile, data['back'])
        checks['font_sha256'] = hashes
        checks['qr_source_sha256'] = hashlib.sha256(qr_path.read_bytes()).hexdigest()
        if 'headshot' in profile:
            checks['headshot_source_sha256'] = hashlib.sha256((root / profile['headshot']).read_bytes()).hexdigest()
        checks['profiles_sha256'] = hashlib.sha256((root / 'cards/profiles.toml').read_bytes()).hexdigest()
        report.write_text(json.dumps(checks, indent=2) + '\n', encoding='utf-8')
        print(f'{name}: {pdf} (structural and digital QR checks passed)')


def argument_parser():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT, help='Repository root (default: this script\'s repository)')
    parser.add_argument('--output', type=Path, help='Artifact directory (default: ROOT/build/business-cards)')
    parser.add_argument('--sabon', type=Path, help='Licensed Sabon Next font; default: sibling blog WOFF2')
    return parser


def main(argv=None):
    parser = argument_parser()
    args = parser.parse_args(argv)
    root = args.root.expanduser().resolve()
    output = args.output if args.output is not None else root / 'build/business-cards'
    sabon = args.sabon if args.sabon is not None else root.parent / SABON_RELATIVE
    try:
        render_all(root, output, sabon)
    except (OSError, ValueError) as error:
        parser.exit(1, f'business_cards: {error}\n')


if __name__ == '__main__':
    main()
