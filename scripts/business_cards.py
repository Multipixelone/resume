"""Render the three shared business cards, independently of resume mappings.

Name and contact geometry is taken from
proofs/business-cards/performance/proof.py; the role and pronoun lines under
the name, and the back, were redrawn after it. The proof is not a runtime input
and is never modified. cards/card.typ draws the artwork; this script stages it
with the fonts, the rust QR and any headshot in a temporary directory, runs
Typst, then stamps the print boxes and validates what comes back. Typst shapes
the text, so Sabon gets its kerning, ligatures and true small caps.

Requires Python 3.11+, Typst, PyMuPDF, Pillow, fonttools[woff], zxing-cpp.
No browser, external font converter, or image-generation service is used.
"""

import argparse
import hashlib
from io import BytesIO
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import tomllib
from typing import Any

import fitz
from fontTools.ttLib import TTFont as Font
from PIL import Image, ImageChops, ImageOps, PngImagePlugin
import zxingcpp


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = Path('cards/card.typ')
SABON_RELATIVE = Path('blog/static/fonts/sabon/Sabon Next Regular.woff2')
# Family names as Typst reports them. An unknown family is a Typst warning,
# which fails the render rather than falling back to another face.
FAMILIES = {'name': 'Cooper*', 'body': 'Sabon Next LT Pro', 'mono': 'PragmataPro Mono Liga'}
# Only the staged fonts may be used, never a system or Typst-bundled face.
TYPST_FONT_FLAGS = ('--ignore-system-fonts', '--ignore-embedded-fonts')
RUST = '#b54a00'
INK = '#2b2520'
PAPER = '#f7f4ed'
TRIM = (252, 144)
BLEED = 9
MEDIA_BOX = (0, 0, 270, 162)
TRIM_BOX = (9, 9, 261, 153)
MARGIN = 18
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
# The QR is 25 modules inside a four-module quiet zone, two of them above the
# address. card.typ owns the placement; these feed the validation evidence.
QR_SIZE = 96
MODULE = QR_SIZE / 33
CAPTION_GAP = 2 * MODULE
# A theatre 8x10 (4:5) at the full safe height, standing at the margins, as in
# card.typ. The JPEG is cut to this size at HEADSHOT_PPI.
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


def font_paths(root, sabon):
    paths = {
        'Cooper': root / 'website/scripts/fonts/cooper/Cooper-Black.ttf',
        # The role uses the regular file's own small caps; pronouns use the
        # italic beside it.
        'Sabon': sabon,
        'Italic': sabon.with_name('Sabon Next Italic.woff2'),
        'Labels': root / 'src/fonts/PragmataPro_Mono_Regular_ligatures_0827.ttf',
    }
    require(sabon.is_file(), f'Sabon Next not found at {sabon}. Supply --sabon FONT_PATH '
            '(a licensed local font file). The renderer does not download or copy it.')
    for name, path in paths.items():
        require(path.is_file(), f'{name} font not found at {path}')
    return paths


def stage_fonts(paths, directory):
    """Write each font as a plain OpenType file, which is all Typst reads.

    WOFF2 is only decompressed; CFF outlines stay CFF. The copies live in the
    caller's temporary directory, never in the repository.
    """
    directory.mkdir()
    for name, path in paths.items():
        with Font(path) as font:
            font.flavor = None
            font.save(directory / f'{name}.{"otf" if "CFF " in font else "ttf"}')
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
    """Crop the headshot to its 4:5 print and return it as 600 ppi JPEG bytes.

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
    # Typst embeds JPEG bytes as they are, without recompressing.
    return buffer.getvalue()


def png_metadata(profile, side, kind, headshot=None):
    metadata = PngImagePlugin.PngInfo()
    metadata.add_text('Title', f'Finn Rutis {profile} card, {side}, {kind}')
    metadata.add_text('Source', 'scripts/business_cards.py; cards/card.typ; cards/profiles.toml; '
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


def card_data(identity, profile, back, headshot):
    """The JSON card.typ reads from sys.inputs.data."""
    return {**identity, 'role': profile.get('role'), 'contacts': contacts_for(profile),
            'address': back['address'], 'headshot': headshot is not None, 'fonts': FAMILIES}


def typst(stage, data, output):
    result = subprocess.run(
        ['typst', 'compile', '--root', stage, '--font-path', stage / 'fonts', *TYPST_FONT_FLAGS,
         '--input', f'data={json.dumps(data)}', stage / 'card.typ', output],
        capture_output=True, text=True, check=False)
    # Warnings fail too: an unknown font family would otherwise fall back silently.
    require(result.returncode == 0 and not result.stderr.strip(),
            f'Typst could not render the card:\n{result.stderr.strip()}')


def render_pdf(path, stage, identity, profile, back, headshot=None):
    """Render one profile in a staged directory holding card.typ, fonts/ and qr.png."""
    photo = stage / 'headshot.jpg'
    if headshot is None:
        photo.unlink(missing_ok=True)
    else:
        photo.write_bytes(headshot)
    raw_pdf = stage / 'card.pdf'
    typst(stage, card_data(identity, profile, back, headshot), raw_pdf)
    with fitz.open(raw_pdf) as doc:
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
    # The QR is a Flate image; only a headshot is embedded as JPEG. Read each
    # image's whole filter, which may be a name or a chain.
    photos = [image[2:4] for image in page.get_images(full=True)
              if '/DCTDecode' in page.parent.xref_get_key(image[0], 'Filter')[1]]
    pixels = tuple(round(n / 72 * HEADSHOT_PPI) for n in HEADSHOT[2:])
    require(photos == ([pixels] if 'headshot' in profile else []),
            'back: a headshot must print once, at 600 ppi, exactly where the profile names one')
    if not photos:
        return {}
    return {'headshot': profile['headshot'], 'headshot_pixels': list(pixels), 'headshot_ppi': HEADSHOT_PPI}


def small_caps_evidence(page, role):
    """The role must use other glyphs than the same letters in the contacts.

    Typst embeds Sabon as a CID subset without glyph names, so compare glyph
    ids: true small caps are separate glyphs, while a missing smcp feature
    would reuse the contacts' lowercase.
    """
    spans = [(span['font'], ''.join(chr(c[0]) for c in span['chars']), span['chars'])
             for span in page.get_texttrace()]
    roles = [(font, chars) for font, text, chars in spans if text == role]
    require(len(roles) == 1, 'front: role line not found')
    font, role_chars = roles[0]
    lowercase = {chr(c[0]): c[1] for f, text, chars in spans if f == font and text != role
                 for c in chars if chr(c[0]).islower()}
    shared = sorted({chr(c[0]) for c in role_chars} & set(lowercase))
    require(bool(shared), 'front: no contact letters to compare with the role line')
    require(all(c[1] != lowercase[chr(c[0])] for c in role_chars if chr(c[0]) in lowercase),
            'front: role line is not set in true small caps')
    return {'role_small_caps_checked_letters': ''.join(shared)}


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
                evidence.update(small_caps_evidence(page, profile['role']))
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


def stage_card(root, directory, paths, qr):
    """Lay out the Typst project: template, plain fonts and the rust QR."""
    shutil.copyfile(root / TEMPLATE, directory / 'card.typ')
    qr.save(directory / 'qr.png')
    return stage_fonts(paths, directory / 'fonts')


def render_all(root, output, sabon):
    root, output, sabon = (Path(path).expanduser().resolve() for path in (root, output, sabon))
    data = load_profiles(root / 'cards/profiles.toml')
    paths = font_paths(root, sabon)
    check_output(root, output, data['profiles'])
    qr_path = root / 'metadata/qr-code.png'
    qr = rust_qr(qr_path, data['back']['destination'])
    with tempfile.TemporaryDirectory(prefix='business-cards-') as temp:
        stage = Path(temp)
        hashes = stage_card(root, stage, paths, qr)
        # All profiles are emitted once. No registry lookup, variant aliases, or labels.
        for name, profile in data['profiles'].items():
            directory = output / name
            directory.mkdir(parents=True, exist_ok=True)
            report = directory / 'validation.json'
            report.unlink(missing_ok=True)  # Do not leave a stale success report after a failed rerender.
            pdf = directory / f'{name}.pdf'
            headshot = headshot_image(root, profile['headshot']) if 'headshot' in profile else None
            render_pdf(pdf, stage, data['identity'], profile, data['back'], headshot)
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
