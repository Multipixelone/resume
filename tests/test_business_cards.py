"""Renderer unit tests, without a proprietary font or a full card render.

Run in the renderer's Python environment:
    python -m unittest discover -s tests -p test_business_cards.py

The full three-profile render, artifact validation, and visual review are separate
validation-owner tasks. Proof-operation regression tests use the approved proof
when it is present in the checkout, not the obsolete fonts/proofs location.
"""

import copy
import importlib.util
from io import BytesIO
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch

from fontTools.fontBuilder import FontBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]


def import_file(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


CARDS = import_file('business_cards', ROOT / 'scripts/business_cards.py')
PROOF = ROOT / 'proofs/business-cards/performance/proof.py'


class Recorder:
    """Record drawing operations without fonts, PDF generation, or rasterization."""

    def __init__(self):
        self.calls = []

    def beginPath(self):
        return Recorder()

    def __getattr__(self, name):
        def record(*args, **kwargs):
            normalized = []
            for arg in args:
                if isinstance(arg, Recorder):
                    normalized.append(arg.calls)
                elif isinstance(arg, CARDS.ImageReader):
                    normalized.append((arg.getSize(), arg.getRGBData()))
                else:
                    normalized.append(arg)
            self.calls.append((name, tuple(normalized), kwargs))
        return record


class ProfileTests(unittest.TestCase):
    def setUp(self):
        self.data = CARDS.load_profiles(ROOT / 'cards/profiles.toml')

    def test_approved_identity_and_contacts(self):
        self.assertEqual(self.data, {
            'identity': {'first_name': 'Finn', 'last_name': 'Rutis', 'pronouns': 'they / them'},
            'back': {'address': 'www.finnrut.is', 'destination': 'https://finnrut.is'},
            'profiles': {
                'performance': {'role': 'musical theatre performer', 'headshot': 'src/headshot.jpg',
                                'email': 'me@finnrut.is', 'phone': '503-267-5052', 'instagram': '@finnrutis'},
                'technology': {'email': 'tech@finnrut.is', 'github': 'Multipixelone'},
                'work': {'email': 'work@finnrut.is', 'phone': '503-267-5052'},
            },
        })

    def load_mutation(self, change):
        data = copy.deepcopy(self.data)
        change(data)
        with patch.object(CARDS.tomllib, 'load', return_value=data):
            return CARDS.load_profiles(ROOT / 'cards/profiles.toml')

    def test_extra_profile_and_missing_profile_rejected(self):
        with self.assertRaisesRegex(ValueError, 'exactly performance'):
            self.load_mutation(lambda d: d['profiles'].update({'fourth': {}}))
        with self.assertRaisesRegex(ValueError, 'exactly performance'):
            self.load_mutation(lambda d: d['profiles'].pop('work'))

    def test_unapproved_fields_rejected(self):
        mutations = [
            lambda d: d['profiles']['technology'].update(phone='503-267-5052'),
            lambda d: d['profiles']['work'].update(instagram='@finnrutis'),
            lambda d: d['profiles']['performance'].update(tagline='A new claim'),
            lambda d: d['identity'].update(label='Performance'),
            lambda d: d.update(variants={}),
        ]
        for mutation in mutations:
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                self.load_mutation(mutation)

    def test_bad_shapes_and_text_rejected(self):
        for value in (None, [], 'technology'):
            with self.subTest(value=value), self.assertRaises(ValueError):
                self.load_mutation(lambda d: d.update(profiles=value))
        for value in ('', ' me@finnrut.is', 'me@finnrut.is\nextra', 'é', 42, True):
            with self.subTest(value=value), self.assertRaises(ValueError):
                self.load_mutation(lambda d: d['profiles']['performance'].update(email=value))

    def test_wrong_qr_destination_rejected(self):
        with self.assertRaisesRegex(ValueError, 'approved https'):
            self.load_mutation(lambda d: d['back'].update(destination='https://example.com'))

    def test_contacts_have_fixed_order_not_toml_order(self):
        self.assertEqual(CARDS.contacts_for({'instagram': '@finnrutis', 'phone': '503-267-5052',
                                             'email': 'me@finnrut.is'}),
                         (('mail', 'me@finnrut.is'), ('phone', '503-267-5052'), ('instagram', '@finnrutis')))

    def test_two_rows_are_balanced_at_approved_pitch(self):
        for count in (2, 3):
            rows = CARDS.contact_baselines(count)
            self.assertEqual(len(rows), count)
            self.assertAlmostEqual((rows[0] + CARDS.CONTACT_CAP * CARDS.CONTACT + rows[-1]) / 2, 72)
            for a, b in zip(rows, rows[1:]):
                self.assertAlmostEqual(a - b, 24)
        with self.assertRaises(ValueError):
            CARDS.contact_baselines(4)

    def test_new_profiles_print_only_approved_fields(self):
        with patch.object(CARDS.pdfmetrics, 'stringWidth', return_value=50):
            for name in ('technology', 'work'):
                canvas = Recorder()
                profile = self.data['profiles'][name]
                CARDS.draw_front(canvas, self.data['identity'], profile)
                strings = [args[2] for operation, args, _ in canvas.calls if operation == 'drawString']
                self.assertEqual(strings, ['Finn', 'Rutis', 'they / them',
                                           *(v for _, v in CARDS.contacts_for(profile))])
                self.assertNotIn(name, strings)

    def test_role_spans_the_name_above_the_pronouns_and_recenters_block(self):
        metrics = lambda s, f, z: len(s) * z * (0.5 if f == 'Cooper' else 0.45)
        with patch.object(CARDS.pdfmetrics, 'stringWidth', side_effect=metrics):
            plain, roled = Recorder(), Recorder()
            profile = self.data['profiles']['performance']
            CARDS.draw_front(plain, self.data['identity'], {k: v for k, v in profile.items() if k != 'role'})
            CARDS.draw_front(roled, self.data['identity'], profile)
        draws = lambda r: {args[2]: (args[:2], kwargs) for op, args, kwargs in r.calls if op == 'drawString'}
        before, after = draws(plain), draws(roled)
        role = 'musical theatre performer'
        self.assertEqual(list(after)[:4], ['Finn', 'Rutis', role, 'they / them'])
        (role_x, role_y), spacing = after[role]
        self.assertEqual(after['they / them'], ((18, role_y - CARDS.LINE_STEP), {}))
        # Letterspacing carries the small caps from the margin to the surname's last ink.
        role_end = role_x + metrics(role, 'SmallCaps', CARDS.ROLE) + spacing['charSpace'] * (len(role) - 1)
        surname_end = CARDS.MARGIN + 0.19 * CARDS.NAME + metrics('Rutis', 'Cooper', CARDS.NAME)
        self.assertEqual(role_x, CARDS.MARGIN)
        self.assertAlmostEqual(role_end, surname_end - CARDS.SURNAME_RSB * CARDS.NAME)
        fonts = [args[0] for op, args, _ in roled.calls if op == 'setFont']
        self.assertEqual(fonts[2:4], ['SmallCaps', 'Italic'])
        # The block grows by the role line and stays centered on the trim.
        top = lambda d: d['Finn'][0][1] + CARDS.NAME_CAP * CARDS.NAME
        for d in (before, after):
            self.assertAlmostEqual(top(d) + d['they / them'][0][1], CARDS.TRIM[1])
        self.assertGreater(top(after), top(before))
        self.assertLess(after['they / them'][0][1], before['they / them'][0][1])
        for text in ('me@finnrut.is', '503-267-5052', '@finnrutis'):
            self.assertEqual(after[text], before[text])

    def test_role_is_optional_text_and_must_fit_the_name(self):
        with self.assertRaises(ValueError):
            self.load_mutation(lambda d: d['profiles']['performance'].update(role=''))
        self.load_mutation(lambda d: d['profiles']['work'].update(role='a role'))
        roled = lambda role: dict(self.data['profiles']['performance'], role=role)
        short = Recorder()
        with patch.object(CARDS.pdfmetrics, 'stringWidth', side_effect=lambda s, f, z: len(s) * z * 0.5):
            with self.assertRaisesRegex(ValueError, 'wider than the name'):
                CARDS.draw_front(Recorder(), self.data['identity'], roled('x' * 40))
            CARDS.draw_front(short, self.data['identity'], roled('actor'))
        # A short role keeps the widest readable spacing rather than stretching.
        spacing = next(kwargs for op, args, kwargs in short.calls if op == 'drawString' and args[2] == 'actor')
        self.assertAlmostEqual(spacing['charSpace'], CARDS.ROLE_TRACKING[1] * CARDS.ROLE)

    def test_contact_overlap_is_rejected_not_silently_shrunk(self):
        with patch.object(CARDS.pdfmetrics, 'stringWidth', return_value=200):
            with self.assertRaisesRegex(ValueError, 'overlaps the name'):
                CARDS.draw_front(Recorder(), self.data['identity'], self.data['profiles']['technology'])


class BackTests(unittest.TestCase):
    """The back was redrawn after the proof: the address moved up under the
    code, and the Performance back added a headshot."""

    qr = Image.new('RGBA', (33, 33), CARDS.RUST)
    back = {'address': 'www.finnrut.is'}

    def draws(self, headshot=None):
        canvas = Recorder()
        CARDS.draw_back(canvas, self.qr, self.back, headshot)
        images = [(args[1:3], kwargs) for op, args, kwargs in canvas.calls if op == 'drawImage']
        address, = [args for op, args, _ in canvas.calls if op == 'drawCentredString']
        return images, address

    def test_address_is_captioned_two_modules_under_the_centred_code(self):
        images, (url_x, url_y, text) = self.draws()
        ((x, y), size), = images
        self.assertEqual(text, 'www.finnrut.is')
        self.assertEqual(size, {'width': 96, 'height': 96, 'mask': 'auto'})
        self.assertAlmostEqual(x + 48, 126)
        self.assertAlmostEqual(url_x, 126)
        symbol_bottom = y + 4 * CARDS.MODULE
        self.assertAlmostEqual(symbol_bottom - (url_y + CARDS.URL_TOP * CARDS.URL), 2 * CARDS.MODULE)
        # The code and its address are centred together on the card's height.
        self.assertAlmostEqual(symbol_bottom + CARDS.SYMBOL + url_y, CARDS.TRIM[1])

    def test_headshot_stands_at_the_margins_with_the_code_beside_it(self):
        photo = Image.new('RGB', (72, 90), '#a0522d')
        plain, _ = self.draws()
        images, (url_x, url_y, _) = self.draws(CARDS.ImageReader(photo))
        ((px, py), print_size), ((x, y), _) = images
        self.assertEqual((px, py), (18, 18))
        self.assertAlmostEqual(print_size['height'], CARDS.TRIM[1] - 36)
        self.assertAlmostEqual(print_size['width'] / print_size['height'], 0.8)
        # The code sits midway between the print and the card's right edge,
        # with far more than its four-module quiet zone clear of the photo.
        symbol_left = x + 4 * CARDS.MODULE
        symbol_right = symbol_left + CARDS.SYMBOL
        photo_right = px + print_size['width']
        self.assertAlmostEqual(symbol_left - photo_right, CARDS.TRIM[0] - symbol_right)
        self.assertGreater(symbol_left - photo_right, 4 * CARDS.MODULE)
        self.assertAlmostEqual(url_x, (symbol_left + symbol_right) / 2)
        # Only the horizontal position changes: the caption keeps its height.
        self.assertEqual(y, plain[0][0][1])

    def headshot_fixture(self, size, fill, sides=0, bottom=0):
        root = Path(self.enterContext(tempfile.TemporaryDirectory())).resolve()
        image = Image.new('RGB', size, fill)
        for box in ((0, 0, sides, size[1]), (size[0] - sides, 0, *size), (0, size[1] - bottom, *size)):
            if box[2] > box[0] and box[3] > box[1]:
                image.paste((255, 0, 0), box)
        image.save(root / 'headshot.png')
        return root

    def test_headshot_crop_keeps_the_top_and_trims_evenly_at_600_ppi(self):
        # Wider than 4:5 trims both sides evenly; taller drops the bottom.
        for size, sides, bottom in (((1200, 1400), 40, 0), ((800, 1200), 0, 200)):
            with self.subTest(size=size):
                root = self.headshot_fixture(size, (0, 0, 255), sides, bottom)
                reader = CARDS.headshot_image(root, 'headshot.png')
                self.assertEqual(reader.getSize(), (720, 900))
                self.assertIsNotNone(reader.jpeg_fh())
                with Image.open(reader.fp) as cropped:
                    red, _, blue = cropped.convert('RGB').split()
                # No red edge band survives the crop, through JPEG noise.
                self.assertLess(CARDS.ImageChops.subtract(red, blue).getextrema()[1], 64)

    def test_headshot_under_300_ppi_or_outside_the_repository_fails(self):
        root = self.headshot_fixture((300, 375), (0, 0, 255))
        with self.assertRaisesRegex(ValueError, 'under 300 ppi'):
            CARDS.headshot_image(root, 'headshot.png')
        for path in ('../headshot.png', '/etc/hosts', 'missing.jpg'):
            with self.subTest(path=path), self.assertRaisesRegex(ValueError, 'not found in the repository'):
                CARDS.headshot_image(root, path)

    def test_repository_headshot_meets_the_print_resolution(self):
        self.assertEqual(CARDS.headshot_image(ROOT, 'src/headshot.jpg').getSize(), (720, 900))

    def test_headshot_prints_only_where_the_profile_names_one(self):
        # PyMuPDF names only the first filter, ASCII85, as ReportLab writes them.
        qr = (5, 6, 1749, 1749, 8, 'DeviceRGB', '', 'Im1', 'ASCII85Decode', 0)
        photo = (7, 0, 720, 900, 8, 'DeviceRGB', '', 'Im2', 'ASCII85Decode', 0)
        filters = {5: '[/ASCII85Decode/FlateDecode]', 7: '[/ASCII85Decode/DCTDecode]'}
        named, plain = {'headshot': 'src/headshot.jpg'}, {}
        for images, profile, ok in (([qr, photo], named, True), ([qr], plain, True),
                                    ([qr], named, False), ([qr, photo], plain, False),
                                    ([qr, photo[:2] + (360, 450) + photo[4:]], named, False)):
            page = Mock()
            page.get_images.return_value = images
            page.parent.xref_get_key.side_effect = lambda xref, key: ('array', filters[xref])
            with self.subTest(images=images, profile=profile):
                if ok:
                    evidence = CARDS.headshot_evidence(page, profile)
                    self.assertEqual(evidence.get('headshot_pixels'), [720, 900] if profile else None)
                else:
                    with self.assertRaisesRegex(ValueError, 'headshot must print once'):
                        CARDS.headshot_evidence(page, profile)

    def test_headshot_is_optional_profile_text(self):
        data = CARDS.load_profiles(ROOT / 'cards/profiles.toml')
        for name in ('technology', 'work'):
            self.assertNotIn('headshot', data['profiles'][name])
        changed = copy.deepcopy(data)
        changed['profiles']['work']['headshot'] = 'src/headshot.jpg'
        with patch.object(CARDS.tomllib, 'load', return_value=changed):
            CARDS.load_profiles(ROOT / 'cards/profiles.toml')
        changed['profiles']['work']['headshot'] = ''
        with patch.object(CARDS.tomllib, 'load', return_value=changed), self.assertRaises(ValueError):
            CARDS.load_profiles(ROOT / 'cards/profiles.toml')


class ProofRegressionTests(unittest.TestCase):
    @unittest.skipUnless(PROOF.is_file(), 'approved local proof is not included in this source tree')
    def test_performance_front_name_and_contacts_match_current_proof(self):
        proof = import_file('approved_card_proof_front', PROOF)
        data = CARDS.load_profiles(ROOT / 'cards/profiles.toml')
        expected, actual = Recorder(), Recorder()
        # Both call the same metrics service. No proprietary font is needed to
        # establish that the name, perforation and contact column are unchanged.
        # The lines under the name were redrawn after the proof and move the
        # block's vertical centre; they have their own tests.
        with patch.object(CARDS.pdfmetrics, 'stringWidth', side_effect=lambda s, f, z: len(s) * z * 0.45):
            proof.draw_front(expected)
            approved = {k: v for k, v in data['profiles']['performance'].items() if k != 'role'}
            CARDS.draw_front(actual, data['identity'], approved)
        contacts = lambda r: r.calls[next(i for i, (op, _, _) in enumerate(r.calls) if op == 'saveState'):]
        self.assertEqual(contacts(actual), contacts(expected))
        x = lambda r, operation: [args[0] for op, args, _ in r.calls if op == operation]
        self.assertEqual(x(actual, 'drawString')[:3], x(expected, 'drawString')[:3])
        self.assertEqual(x(actual, 'line'), x(expected, 'line'))
        pronouns = next(args for op, args, _ in actual.calls if op == 'drawString' and args[2] == 'they / them')
        self.assertEqual(pronouns[0], 18)

    def test_github_icon_is_distinct_and_unknown_icons_fail(self):
        github, instagram = Recorder(), Recorder()
        CARDS.contact_icon(github, 'github', 0, 0)
        CARDS.contact_icon(instagram, 'instagram', 0, 0)
        self.assertNotEqual(github.calls, instagram.calls)
        self.assertEqual(github.calls[0][0], 'saveState')
        self.assertEqual(github.calls[-1][0], 'restoreState')
        with self.assertRaisesRegex(ValueError, 'Unknown contact icon'):
            CARDS.contact_icon(Recorder(), 'unknown', 0, 0)


class ArtifactValidationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def ink_image(self):
        image = Image.new('RGBA', (1050, 600))
        image.paste(CARDS.INK, (75, 100, 975, 500))
        return image

    def test_ink_alpha_and_safe_margin(self):
        bounds, margin = CARDS.validate_ink(self.ink_image(), 'front')
        self.assertEqual(bounds, (75, 100, 975, 500))
        self.assertEqual(margin, 0.25)
        for image in (Image.new('RGBA', (1050, 600)),
                      Image.new('RGBA', (1050, 600), CARDS.PAPER)):
            with self.assertRaisesRegex(ValueError, 'transparent and opaque'):
                CARDS.validate_ink(image, 'front')
        image = self.ink_image()
        image.putpixel((59, 100), (0, 0, 0, 255))
        with self.assertRaisesRegex(ValueError, '0.2 inches'):
            CARDS.validate_ink(image, 'front')

    def test_preview_is_cream_only_after_compositing(self):
        ink = self.ink_image()
        preview = CARDS.paper_preview(ink)
        self.assertEqual(preview.mode, 'RGB')
        self.assertEqual(preview.getpixel((0, 0)), (247, 244, 237))
        self.assertEqual(ink.getpixel((0, 0))[3], 0)
        with self.assertRaisesRegex(ValueError, 'pixels differ'):
            CARDS.same_pixels(preview, Image.new('RGB', preview.size, 'white'), 'pixels differ')

    def test_saved_png_size_mode_resolution_and_provenance(self):
        path = self.root / 'front-ink.png'
        ink = self.ink_image()
        ink.save(path, dpi=(300, 300), pnginfo=CARDS.png_metadata('performance', 'front', 'ink'))
        actual = CARDS.read_png(path, 'RGBA', (1050, 600), 300)
        CARDS.same_pixels(actual, ink, 'roundtrip changed')
        for mode, size, dpi in (('RGB', ink.size, 300), ('RGBA', (336, 192), 300),
                                 ('RGBA', ink.size, 96)):
            with self.subTest(mode=mode, size=size, dpi=dpi), self.assertRaises(ValueError):
                CARDS.read_png(path, mode, size, dpi)
        ink.save(path, dpi=(300, 300))
        with self.assertRaisesRegex(ValueError, 'provenance'):
            CARDS.read_png(path, 'RGBA', ink.size, 300)

    def pdf_fixture(self):
        image = Image.new('RGBA', (270, 162))
        image.paste(CARDS.INK, (40, 40, 230, 120))
        buffer = BytesIO()
        image.save(buffer, format='PNG')
        page = Mock()
        page.mediabox = page.bleedbox = page.cropbox = CARDS.MEDIA_BOX
        page.trimbox = CARDS.TRIM_BOX
        page.rotation = 0
        page.get_text.return_value = 'Finn\nRutis\n'
        page.get_drawings.return_value = []
        page.get_fonts.return_value = [(1, 'ttf', 'TrueType', 'Cooper-Black')]
        page.get_pixmap.return_value.tobytes.return_value = buffer.getvalue()
        doc = Mock()
        doc.extract_font.return_value = ('Cooper-Black', 'ttf', 'TrueType', b'embedded')
        return doc, page

    def test_pdf_structure_and_embedding(self):
        doc, page = self.pdf_fixture()
        evidence = CARDS.validate_pdf_page(doc, page, ['Finn', 'Rutis'], 'front')
        self.assertEqual(evidence['embedded_fonts'], ['Cooper-Black'])
        for attr, value in (('mediabox', (0, 0, 252, 144)), ('trimbox', CARDS.MEDIA_BOX),
                            ('bleedbox', CARDS.TRIM_BOX), ('cropbox', CARDS.TRIM_BOX), ('rotation', 90)):
            doc, page = self.pdf_fixture()
            setattr(page, attr, value)
            with self.subTest(attr=attr), self.assertRaises(ValueError):
                CARDS.validate_pdf_page(doc, page, ['Finn', 'Rutis'], 'front')
        doc, page = self.pdf_fixture()
        doc.extract_font.return_value = ('Cooper', 'ttf', 'TrueType', b'')
        with self.assertRaisesRegex(ValueError, 'unembedded'):
            CARDS.validate_pdf_page(doc, page, ['Finn', 'Rutis'], 'front')

    def test_pdf_extra_text_background_and_crop_marks_rejected(self):
        doc, page = self.pdf_fixture()
        with self.assertRaisesRegex(ValueError, 'text/order'):
            CARDS.validate_pdf_page(doc, page, ['Finn'], 'front')
        page.get_drawings.return_value = [{'fill': (1, 1, 1), 'rect': CARDS.fitz.Rect(CARDS.MEDIA_BOX)}]
        with self.assertRaisesRegex(ValueError, 'background fill'):
            CARDS.validate_pdf_page(doc, page, ['Finn', 'Rutis'], 'front')
        doc, page = self.pdf_fixture()
        full = Image.new('RGBA', (270, 162), CARDS.PAPER)
        buffer = BytesIO()
        full.save(buffer, format='PNG')
        page.get_pixmap.return_value.tobytes.return_value = buffer.getvalue()
        with self.assertRaisesRegex(ValueError, 'safe area'):
            CARDS.validate_pdf_page(doc, page, ['Finn', 'Rutis'], 'front')

    def test_qr_decoder_rejects_wrong_destination_and_failure(self):
        image = Image.new('RGB', (10, 10))
        for decoded in (None, Mock(text='https://example.com')):
            with patch.object(CARDS.zxingcpp, 'read_barcode', return_value=decoded):
                with self.assertRaisesRegex(ValueError, 'did not decode'):
                    CARDS.decode_qr(image, 'https://finnrut.is', '96 DPI')
        with patch.object(CARDS.zxingcpp, 'read_barcode', return_value=Mock(text='https://finnrut.is')):
            self.assertEqual(CARDS.decode_qr(image, 'https://finnrut.is', '300 DPI'), 'https://finnrut.is')

    def test_qr_recolor_preserves_pixels_and_extends_quiet_zone(self):
        source = Image.new('L', (1537, 1537), 255)
        source.paste(0, (106, 106, 1431, 1431))
        path = self.root / 'qr.png'
        source.save(path)
        with patch.object(CARDS.zxingcpp, 'read_barcode', return_value=Mock(text='https://finnrut.is')):
            qr = CARDS.rust_qr(path, 'https://finnrut.is')
            self.assertEqual(qr.size, (1749, 1749))
            self.assertEqual(qr.getchannel('A').getbbox(), (212, 212, 1537, 1537))
            self.assertEqual(qr.getpixel((212, 212)), (181, 74, 0, 255))
            self.assertEqual(qr.getchannel('A').crop((106, 106, 1643, 1643)).tobytes(),
                             CARDS.ImageOps.invert(source).tobytes())
            source.putpixel((0, 0), 0)
            source.save(path)
            with self.assertRaisesRegex(ValueError, 'quiet zone'):
                CARDS.rust_qr(path, 'https://finnrut.is')
            Image.new('L', (100, 100)).save(path)
            with self.assertRaisesRegex(ValueError, 'size changed'):
                CARDS.rust_qr(path, 'https://finnrut.is')

    def test_artifact_contract_has_exactly_eight_files_per_profile(self):
        expected_pngs = {f'{side}-{kind}.png' for side in ('front', 'back')
                         for kind in ('ink', 'preview', 'actual-size')}
        for profile in ('performance', 'technology', 'work'):
            self.assertEqual(CARDS.artifact_names(profile), expected_pngs | {f'{profile}.pdf', 'validation.json'})
        with self.assertRaisesRegex(ValueError, 'missing output files'):
            CARDS.validate_artifacts(self.root, 'performance', {}, {}, {})

    def test_pdf_page_count_checked_before_page_validation(self):
        data = CARDS.load_profiles(ROOT / 'cards/profiles.toml')
        for name in CARDS.artifact_names('performance') - {'validation.json'}:
            (self.root / name).touch()
        for pages in ([], [None], [None, None, None]):
            with patch.object(CARDS.fitz, 'open') as opened:
                opened.return_value.__enter__.return_value = pages
                with self.assertRaisesRegex(ValueError, 'exactly two pages'):
                    CARDS.validate_artifacts(self.root, 'performance', data['identity'],
                                             data['profiles']['performance'], data['back'])


class InterfaceTests(unittest.TestCase):
    def test_default_paths_follow_explicit_root_not_working_directory(self):
        with tempfile.TemporaryDirectory() as temp, patch.object(CARDS, 'render_all') as render:
            root = Path(temp) / 'resume'
            CARDS.main(['--root', str(root)])
            render.assert_called_once_with(root, root / 'build/business-cards', root.parent / CARDS.SABON_RELATIVE)

    def test_explicit_cli_paths(self):
        with patch.object(CARDS, 'render_all') as render:
            CARDS.main(['--root', str(ROOT), '--output', '/tmp/cards', '--sabon', '/tmp/Sabon Next.woff2'])
            render.assert_called_once_with(ROOT, Path('/tmp/cards'), Path('/tmp/Sabon Next.woff2'))

    def test_missing_font_has_actionable_error(self):
        with self.assertRaisesRegex(ValueError, 'Supply --sabon FONT_PATH'):
            CARDS.font_paths(ROOT, ROOT / 'missing-sabon.woff2')

    def test_truetype_font_input_is_returned_in_memory(self):
        # Cooper is a local OFL fixture, not a proprietary font. Full Sabon CFF
        # conversion is covered by the validation owner's real artifact run.
        converted = CARDS.truetype(ROOT / 'website/scripts/fonts/cooper/Cooper-Black.ttf')
        self.assertIsInstance(converted, BytesIO)
        self.assertEqual(converted.tell(), 0)
        with CARDS.Font(converted) as font:
            self.assertIn('glyf', font)
            self.assertIsNone(font.flavor)

    def small_caps_fixture(self, with_small_caps=True):
        letters = [chr(code) for code in range(ord('a'), ord('z') + 1)]
        names = ['.notdef', *letters, *(f'{letter}.sc' for letter in letters if with_small_caps)]
        builder = FontBuilder(1000, isTTF=True)
        builder.setupGlyphOrder(names)
        builder.setupCharacterMap({ord(letter): letter for letter in letters})
        builder.setupGlyf({name: TTGlyphPen(None).glyph() for name in names})
        builder.setupHorizontalMetrics({name: (500, 0) for name in names})
        builder.setupHorizontalHeader(ascent=800, descent=-200)
        builder.setupNameTable({'familyName': 'Fixture', 'styleName': 'Regular', 'psName': 'Fixture-Regular'})
        builder.setupOS2()
        builder.setupPost()
        data = BytesIO()
        builder.save(data)
        data.seek(0)
        return data

    def test_small_caps_remap_lowercase_and_rename_the_face(self):
        # TrueType output has no glyph names, and ReportLab merges fonts that
        # share a face name, so the remap runs first and renames the face.
        with CARDS.Font(CARDS.truetype(CARDS.small_caps(self.small_caps_fixture()))) as font:
            regular = CARDS.Font(self.small_caps_fixture())
            self.assertEqual(font.getGlyphID(font.getBestCmap()[ord('m')]), regular.getGlyphID('m.sc'))
            self.assertEqual(font['name'].getDebugName(6), 'Fixture-RegularSC')
        with self.assertRaisesRegex(ValueError, 'true small caps'):
            CARDS.small_caps(self.small_caps_fixture(with_small_caps=False))

    def test_proof_and_unrelated_outputs_protected(self):
        for output in (ROOT, ROOT.parent, ROOT / 'proofs/business-cards', ROOT / 'fonts/proofs'):
            with self.subTest(output=output), self.assertRaises(ValueError):
                CARDS.check_output(ROOT, output, ['performance'])
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp)
            profile = output / 'performance'
            profile.mkdir()
            (profile / 'user-notes.txt').write_text('Do not overwrite me')
            with self.assertRaisesRegex(ValueError, 'unrelated files'):
                CARDS.check_output(ROOT, output, ['performance'])

    def test_all_profiles_emitted_once_without_registry_input(self):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / 'cards'
            with patch.object(CARDS, 'font_paths', return_value={}), \
                    patch.object(CARDS, 'register_fonts', return_value={}), \
                    patch.object(CARDS, 'rust_qr'), \
                    patch.object(CARDS, 'headshot_image') as headshot, \
                    patch.object(CARDS, 'render_pdf') as pdf, \
                    patch.object(CARDS, 'export_pngs') as png, \
                    patch.object(CARDS, 'validate_artifacts', return_value={}) as validate:
                CARDS.render_all(ROOT, output, Path(temp) / 'sabon.woff2')
            # Only the Performance back carries the headshot.
            headshot.assert_called_once_with(ROOT, 'src/headshot.jpg')
            self.assertEqual([call.args[5] for call in pdf.call_args_list],
                             [headshot.return_value, None, None])
            self.assertEqual(pdf.call_count, 3)
            self.assertEqual(png.call_count, 3)
            self.assertEqual(validate.call_count, 3)
            self.assertEqual({p.name for p in output.iterdir()}, {'performance', 'technology', 'work'})
            for name in ('performance', 'technology', 'work'):
                self.assertTrue((output / name / 'validation.json').is_file())


if __name__ == '__main__':
    unittest.main()
