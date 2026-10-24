"""Renderer unit tests, without a proprietary font or a full card render.

Run in the renderer's Python environment, with typst on PATH:
    python -m unittest discover -s tests -p test_business_cards.py

Layout tests compile cards/card.typ with Typst's bundled Libertinus Serif
standing in for Sabon (it has an italic and true small caps), so the geometry
is checked on real shaped text. The full three-profile render, artifact
validation, and visual review are separate validation-owner tasks.
"""

import copy
import importlib.util
from io import BytesIO
import math
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import Mock, patch

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]


def import_file(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


CARDS = import_file('business_cards', ROOT / 'scripts/business_cards.py')
TYPST = shutil.which('typst')
needs_typst = unittest.skipUnless(TYPST, 'typst is not on PATH; run in the business-cards environment')

# Approved geometry from proofs/business-cards/performance/proof.py and the
# later role, pronoun and back redraws, in points from the trim's bottom left.
MARGIN = 18
NAME = 40
NAME_CAP = 1434 / 2000
CONTACT_CAP = 685 / 1000
ROW = 24
LINE_STEP = 11
ROLE_TRACKING = (0.04 * 8, 0.14 * 8)
SURNAME_RSB = 50 / 2000 * NAME
URL_TOP = 1647 / 2048 * 7
SYMBOL = 25 * CARDS.MODULE
STAND_INS = dict(CARDS.FAMILIES, body='Libertinus Serif')


class Card:
    """One compiled card, with text and images in trim coordinates (y up)."""

    def __init__(self, doc):
        self.doc = doc
        self.pages = [self.read(page) for page in doc]

    @staticmethod
    def read(page):
        top = CARDS.MEDIA_BOX[3] - CARDS.BLEED
        spans = {}
        for block in page.get_text('rawdict')['blocks']:
            for line in block.get('lines', []):
                for span in line['spans']:
                    chars = span['chars']
                    text = ''.join(c['c'] for c in chars)
                    spans[text] = {'x': span['origin'][0] - CARDS.BLEED,
                                   'end': chars[-1]['bbox'][2] - CARDS.BLEED,
                                   'base': top - span['origin'][1], 'chars': chars}
        images = [(i['bbox'][0] - CARDS.BLEED, top - i['bbox'][3], i['bbox'][2] - i['bbox'][0],
                   i['bbox'][3] - i['bbox'][1]) for i in page.get_image_info()]
        return {'spans': spans, 'images': images, 'drawings': page.get_drawings()}

    @property
    def front(self):
        return self.pages[0]

    @property
    def back(self):
        return self.pages[1]


def dashed(drawing):
    """The perforation is the only dashed stroke; icons report an empty pattern."""
    return (drawing.get('dashes') or '[] 0') != '[] 0'


def headshot_bytes():
    buffer = BytesIO()
    CARDS.print_image(Image.new('RGB', CARDS.PHOTO_PIXELS, '#a0522d')).save(buffer, format='PNG')
    return buffer.getvalue()


class CompiledCardTest(unittest.TestCase):
    """Compile card.typ through the renderer's own staging and Typst call."""

    @classmethod
    def setUpClass(cls):
        cls.data = CARDS.load_profiles(ROOT / 'cards/profiles.toml')
        cls.stage = Path(cls.enterClassContext(tempfile.TemporaryDirectory()))
        fonts = {'Cooper': ROOT / 'website/scripts/fonts/cooper/Cooper-Black.ttf',
                 'Labels': ROOT / 'src/fonts/PragmataPro_Mono_Regular_ligatures_0827.ttf'}
        # Sabon is replaced by the Typst-bundled serif, so allow bundled faces.
        cls.enterClassContext(patch.object(CARDS, 'FAMILIES', STAND_INS))
        cls.enterClassContext(patch.object(CARDS, 'TYPST_FONT_FLAGS', ('--ignore-system-fonts',)))
        CARDS.stage_card(ROOT, cls.stage, fonts, Image.new('RGBA', (33, 33), CARDS.RUST))

    def render(self, profile, headshot=None, back=None):
        path = self.stage / 'out.pdf'
        CARDS.render_pdf(path, self.stage, self.data['identity'], profile,
                         back or self.data['back'], headshot)
        doc = CARDS.fitz.open(path)
        self.addCleanup(doc.close)
        return Card(doc)

    def profile(self, name, **changes):
        profile = dict(self.data['profiles'][name], **changes)
        return {k: v for k, v in profile.items() if v is not None}


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

    def test_role_is_optional_text(self):
        with self.assertRaises(ValueError):
            self.load_mutation(lambda d: d['profiles']['performance'].update(role=''))
        self.load_mutation(lambda d: d['profiles']['work'].update(role='a role'))


@needs_typst
class FrontTests(CompiledCardTest):
    def test_new_profiles_print_only_approved_fields(self):
        for name in ('technology', 'work'):
            with self.subTest(name=name):
                card = self.render(self.profile(name))
                text = card.doc[0].get_text().splitlines()
                self.assertEqual(text, ['Finn', 'Rutis', 'they / them',
                                        *(v for _, v in CARDS.contacts_for(self.data['profiles'][name]))])
                self.assertNotIn(name, text)

    def test_name_rule_and_contacts_keep_the_proof_geometry(self):
        front = self.render(self.profile('performance', role=None)).front
        spans = front['spans']
        self.assertAlmostEqual(spans['Finn']['x'], MARGIN, places=3)
        self.assertAlmostEqual(spans['Rutis']['x'], MARGIN + 0.19 * NAME, places=3)
        self.assertAlmostEqual(spans['Finn']['base'] - spans['Rutis']['base'], 0.87 * NAME, places=3)
        contacts = [spans[v] for v in ('me@finnrut.is', '503-267-5052', '@finnrutis')]
        # Rows at the approved pitch, centred on the trim, right-aligned to the margin.
        for a, b in zip(contacts, contacts[1:]):
            self.assertAlmostEqual(a['base'] - b['base'], ROW, places=2)
        self.assertAlmostEqual((contacts[0]['base'] + CONTACT_CAP * 10 + contacts[-1]['base']) / 2,
                               CARDS.TRIM[1] / 2, places=2)
        self.assertAlmostEqual(min(c['x'] for c in contacts), CARDS.TRIM[0] - MARGIN
                               - max(c['end'] - c['x'] for c in contacts), places=2)
        self.assertAlmostEqual(max(c['end'] for c in contacts), CARDS.TRIM[0] - MARGIN, places=2)
        # The dashed rule runs from the top of "Finn" to the pronoun baseline,
        # midway between the surname and the icons, 1.5 * CONTACT before the text.
        rule, = [d for d in front['drawings'] if dashed(d)]
        x = rule['rect'].x0 - CARDS.BLEED
        icon_x = contacts[0]['x'] - 15
        # Extracted glyph ends carry the PDF widths' 1/1000 em rounding (0.04pt at 40pt).
        self.assertAlmostEqual(x, (spans['Rutis']['end'] + icon_x) / 2, places=1)
        top = CARDS.MEDIA_BOX[3] - CARDS.BLEED
        self.assertAlmostEqual(top - rule['rect'].y0, spans['Finn']['base'] + NAME_CAP * NAME, places=2)
        self.assertAlmostEqual(top - rule['rect'].y1, spans['they / them']['base'], places=2)

    def test_role_spans_the_name_above_the_pronouns_and_recenters_block(self):
        role = 'musical theatre performer'
        before = self.render(self.profile('performance', role=None)).front['spans']
        after = self.render(self.profile('performance')).front['spans']
        self.assertEqual(list(after)[:4], ['Finn', 'Rutis', role, 'they / them'])
        self.assertAlmostEqual(after[role]['x'], MARGIN)
        self.assertAlmostEqual(after['they / them']['x'], MARGIN)
        self.assertAlmostEqual(after[role]['base'] - after['they / them']['base'], LINE_STEP, places=2)
        # Letterspacing carries the small caps from the margin to the surname's last ink.
        self.assertAlmostEqual(after[role]['end'], after['Rutis']['end'] - SURNAME_RSB, places=1)
        # The block grows by the role line and stays centered on the trim.
        top = lambda d: d['Finn']['base'] + NAME_CAP * NAME
        for d in (before, after):
            self.assertAlmostEqual(top(d) + d['they / them']['base'], CARDS.TRIM[1], places=2)
        self.assertGreater(top(after), top(before))
        self.assertLess(after['they / them']['base'], before['they / them']['base'])
        for text in ('me@finnrut.is', '503-267-5052', '@finnrutis'):
            self.assertEqual((after[text]['x'], after[text]['base']), (before[text]['x'], before[text]['base']))

    def test_role_is_true_small_caps(self):
        card = self.render(self.profile('performance'))
        evidence = CARDS.small_caps_evidence(card.doc[0], 'musical theatre performer')
        self.assertTrue(evidence['role_small_caps_checked_letters'])

    def test_role_must_fit_the_name_and_a_short_role_is_not_stretched(self):
        with self.assertRaisesRegex(ValueError, 'wider than the name'):
            self.render(self.profile('performance', role='x' * 40))
        chars = self.render(self.profile('performance', role='actor')).front['spans']['actor']['chars']
        # A short role keeps the widest readable spacing rather than stretching.
        # Kerning pairs only ever tighten a gap below the tracking.
        gaps = [b['bbox'][0] - a['bbox'][2] for a, b in zip(chars, chars[1:])]
        self.assertAlmostEqual(max(gaps), ROLE_TRACKING[1], places=3)

    def test_contact_overlap_is_rejected_not_silently_shrunk(self):
        with self.assertRaisesRegex(ValueError, 'overlaps the name'):
            self.render(self.profile('technology', github='x' * 40))

    def test_contacts_are_shaped_with_ligatures(self):
        chars = self.render(self.profile('performance')).front['spans']['me@finnrut.is']['chars']
        f, i = next((a, b) for a, b in zip(chars, chars[1:]) if (a['c'], b['c']) == ('f', 'i'))
        # One fi glyph carries both letters; the i gets no advance of its own.
        self.assertAlmostEqual(i['bbox'][2] - i['bbox'][0], 0)
        self.assertGreater(f['bbox'][2] - f['bbox'][0], 0)

    def test_github_icon_is_distinct_and_unknown_icons_fail(self):
        drawn = lambda name: [d['items'] for d in self.render(self.profile(name)).front['drawings']
                              if not dashed(d)]
        self.assertNotEqual(drawn('technology'), drawn('performance'))
        with patch.object(CARDS, 'contacts_for', return_value=(('fax', '555'), ('mail', 'me@finnrut.is'))):
            with self.assertRaisesRegex(ValueError, 'Unknown contact icon'):
                self.render(self.profile('work'))

    def test_unknown_font_family_fails_instead_of_falling_back(self):
        with patch.object(CARDS, 'FAMILIES', dict(STAND_INS, body='Not A Font')):
            with self.assertRaisesRegex(ValueError, 'Typst could not render'):
                self.render(self.profile('work'))


@needs_typst
class BackTests(CompiledCardTest):
    """The back was redrawn after the proof: the address moved up under the
    code, and the Performance back added a headshot print in two inks."""

    def test_address_is_captioned_two_modules_under_the_centred_code(self):
        back = self.render(self.profile('work')).back
        (x, y, width, height), = back['images']
        url = back['spans']['www.finnrut.is']
        self.assertAlmostEqual(width, 96)
        self.assertAlmostEqual(height, 96)
        self.assertAlmostEqual(x + 48, 126)
        self.assertAlmostEqual((url['x'] + url['end']) / 2, 126, places=2)
        symbol_bottom = y + 4 * CARDS.MODULE
        self.assertAlmostEqual(symbol_bottom - (url['base'] + URL_TOP), 2 * CARDS.MODULE, places=2)
        # The code and its address are centred together on the card's height.
        self.assertAlmostEqual(symbol_bottom + SYMBOL + url['base'], CARDS.TRIM[1], places=2)

    def test_headshot_print_rests_turned_with_the_code_beside_it(self):
        plain = self.render(self.profile('performance', headshot=None)).back
        card = self.render(self.profile('performance'), headshot_bytes())
        back = card.back
        _, (x, y, _, _) = back['images']
        # card.typ and the renderer agree on the print's size, turned
        # counterclockwise, and the photograph inside it is a 4:5 print.
        turn = CARDS.fitz.Matrix(card.doc[1].get_image_info()[0]['transform'])
        self.assertAlmostEqual(math.degrees(math.atan2(-turn.b, turn.a)), CARDS.HEADSHOT_TILT, places=3)
        self.assertAlmostEqual(math.hypot(turn.a, turn.b), CARDS.PRINT_SIZE[0], places=3)
        self.assertAlmostEqual(math.hypot(turn.c, turn.d), CARDS.PRINT_SIZE[1], places=3)
        self.assertAlmostEqual(CARDS.PHOTO_SIZE[0] / CARDS.PHOTO_SIZE[1], 0.8)

        def trim(u, v):
            """A photograph point (points from its top left) on the trim, y up."""
            page = CARDS.fitz.Point((CARDS.PRINT_ROOM + u) / CARDS.PRINT_SIZE[0],
                                    (CARDS.PRINT_ROOM + v) / CARDS.PRINT_SIZE[1]) * turn
            return page.x - CARDS.BLEED, CARDS.MEDIA_BOX[3] - CARDS.BLEED - page.y

        w, h = CARDS.PHOTO_SIZE
        corners = [trim(u, v) for u in (0, w) for v in (0, h)]
        # The turned photograph fills the safe height exactly.
        self.assertAlmostEqual(min(y for _, y in corners), 18, places=3)
        self.assertAlmostEqual(max(y for _, y in corners), CARDS.TRIM[1] - 18, places=3)
        # The top-left corner's tip rests on the margin; the bottom-right one's
        # is the print's far reach.
        over = CARDS.MOUNT_OVERHANG
        self.assertAlmostEqual(trim(-over, -over)[0], 18, places=3)
        reach = trim(w + over, h + over)[0]
        # The corners and shadows belong to the print; nothing else is drawn.
        self.assertEqual([d for d in back['drawings'] if d['fill'] is not None], [])
        # The code sits midway between the print and the card's right edge,
        # with far more than its quiet zone clear of the print.
        symbol_left = x + 4 * CARDS.MODULE
        symbol_right = symbol_left + SYMBOL
        self.assertAlmostEqual(symbol_left - reach, CARDS.TRIM[0] - symbol_right, places=2)
        self.assertGreater(symbol_left - reach, 4 * CARDS.MODULE)
        url = back['spans']['www.finnrut.is']
        self.assertAlmostEqual((url['x'] + url['end']) / 2, (symbol_left + symbol_right) / 2, places=2)
        # Only the horizontal position changes: the caption keeps its height.
        self.assertAlmostEqual(y, plain['images'][0][1])

    def test_headshot_prints_once_with_its_stock_mask_where_the_profile_names_one(self):
        named = self.render(self.profile('performance'), headshot_bytes())
        self.assertEqual(CARDS.headshot_evidence(named.doc[1], {'headshot': 'src/headshot.jpg'})['headshot_pixels'],
                         list(CARDS.PRINT_PIXELS))
        with self.assertRaisesRegex(ValueError, 'headshot print must appear once'):
            CARDS.headshot_evidence(named.doc[1], {})


class HeadshotTests(unittest.TestCase):
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
                cropped = CARDS.headshot_crop(root, 'headshot.png')
                self.assertEqual((cropped.mode, cropped.size), ('RGB', CARDS.PHOTO_PIXELS))
                red, _, blue = cropped.split()
                # No red edge band survives the crop, through resampling.
                self.assertLess(CARDS.ImageChops.subtract(red, blue).getextrema()[1], 64)

    def test_print_tucks_the_photograph_into_paper_corners_over_its_shadow(self):
        shirt = (70, 98, 121)
        printed = CARDS.print_image(Image.new('RGB', CARDS.PHOTO_PIXELS, shirt))
        self.assertEqual((printed.mode, printed.size), ('RGBA', CARDS.PRINT_PIXELS))
        alpha = printed.getchannel('A')
        width, height = printed.size
        # Nothing reaches the image's edge, so no shadow is clipped.
        ring = [alpha.getpixel((x, y)) for x in range(width) for y in (0, height - 1)]
        ring += [alpha.getpixel((x, y)) for y in range(height) for x in (0, width - 1)]
        self.assertEqual(max(ring), 0)
        (x0, y0), (pw, ph) = CARDS.PHOTO_OFFSET, CARDS.PHOTO_PIXELS

        def photo(x, y):  # Points from the photograph's top left.
            return round(x0 + x * CARDS.PT), round(y0 + y * CARDS.PT)

        w, h = CARDS.PHOTO_SIZE
        self.assertEqual(printed.getpixel(photo(w / 2, h / 2)), (*shirt, 255))
        # Inside each corner, away from its fold, its paper covers the
        # photograph: a light Rule Line tint over the stock.
        paper = (221, 214, 198, round(255 * CARDS.MOUNT_PAPER[1]))
        self.assertEqual(printed.getpixel(photo(2, 2)), paper)
        self.assertEqual(printed.getpixel(photo(w - 2, h - 2)), paper)
        # The top-left corner's long edge crosses the diagonal here. Just inside
        # it, the fold prints solid Rule Line; just past it, the corner's shadow
        # darkens the photograph.
        edge = CARDS.MOUNT_LEG / 2 - CARDS.MOUNT_OVERHANG
        across = [printed.getpixel(photo(edge + t / 100, edge + t / 100)) for t in range(-40, 1, 2)]
        self.assertIn((221, 214, 198, 255), across)
        shaded = printed.getpixel(photo(edge + 0.2, edge + 0.2))
        self.assertEqual(shaded[3], 255)
        self.assertTrue(all(s < p for s, p in zip(shaded[:3], shirt)))
        # The print's shadow falls below it, in Program Ink, more than above.
        below = printed.getpixel(photo(w / 2, h + 1))
        above = printed.getpixel(photo(w / 2, -1))
        self.assertEqual(below[:3], (43, 37, 32))
        self.assertTrue(above[3] < below[3] < 128)

    def test_headshot_under_300_ppi_or_outside_the_repository_fails(self):
        root = self.headshot_fixture((300, 375), (0, 0, 255))
        with self.assertRaisesRegex(ValueError, 'under 300 ppi'):
            CARDS.headshot_image(root, 'headshot.png')
        for path in ('../headshot.png', '/etc/hosts', 'missing.jpg'):
            with self.subTest(path=path), self.assertRaisesRegex(ValueError, 'not found in the repository'):
                CARDS.headshot_image(root, path)

    def test_repository_headshot_meets_the_print_resolution(self):
        with Image.open(BytesIO(CARDS.headshot_image(ROOT, 'src/headshot.jpg'))) as photo:
            self.assertEqual((photo.format, photo.mode, photo.size), ('PNG', 'RGBA', CARDS.PRINT_PIXELS))

    def test_headshot_prints_only_where_the_profile_names_one(self):
        # get_images rows: xref, soft-mask xref, width, height, ...
        qr = (5, 6, 1749, 1749, 8, 'ICCBased', '', 'x1', 'FlateDecode', 0)
        photo = (7, 8, *CARDS.PRINT_PIXELS, 8, 'ICCBased', '', 'x0', 'FlateDecode', 0)
        unmasked = photo[:1] + (0,) + photo[2:]
        small = photo[:2] + (348, 435) + photo[4:]
        named, plain = {'headshot': 'src/headshot.jpg'}, {}
        for images, profile, ok in (([qr, photo], named, True), ([qr], plain, True),
                                    ([qr], named, False), ([qr, photo], plain, False),
                                    ([qr, small], named, False), ([qr, unmasked], named, False),
                                    ([qr, photo, photo], named, False)):
            page = Mock()
            page.get_images.return_value = images
            with self.subTest(images=images, profile=profile):
                if ok:
                    evidence = CARDS.headshot_evidence(page, profile)
                    self.assertEqual(evidence.get('headshot_pixels'),
                                     list(CARDS.PRINT_PIXELS) if profile else None)
                else:
                    with self.assertRaisesRegex(ValueError, 'headshot print must appear once'):
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

    def test_small_caps_check_rejects_the_contacts_lowercase(self):
        trace = lambda text, glyphs: {'font': 'Sabon', 'chars': [(ord(c), g) for c, g in zip(text, glyphs)]}
        page = Mock()
        page.get_texttrace.return_value = [trace('actor', [1, 2, 3, 4, 5]), trace('me@cat.is', [6, 7, 8, 9, 10, 11, 12, 13, 14])]
        self.assertEqual(CARDS.small_caps_evidence(page, 'actor'), {'role_small_caps_checked_letters': 'act'})
        page.get_texttrace.return_value[1] = trace('me@cat.is', [6, 7, 8, 9, 1, 11, 12, 13, 14])
        with self.assertRaisesRegex(ValueError, 'true small caps'):
            CARDS.small_caps_evidence(page, 'actor')

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
            root = Path(temp).resolve() / 'resume'
            CARDS.main(['--root', str(root)])
            render.assert_called_once_with(root, root / 'build/business-cards', root.parent / CARDS.SABON_RELATIVE)

    def test_explicit_cli_paths(self):
        with patch.object(CARDS, 'render_all') as render:
            CARDS.main(['--root', str(ROOT), '--output', '/tmp/cards', '--sabon', '/tmp/Sabon Next.woff2'])
            render.assert_called_once_with(ROOT, Path('/tmp/cards'), Path('/tmp/Sabon Next.woff2'))

    def test_missing_font_has_actionable_error(self):
        with self.assertRaisesRegex(ValueError, 'Supply --sabon FONT_PATH'):
            CARDS.font_paths(ROOT, ROOT / 'missing-sabon.woff2')

    def test_fonts_are_staged_as_plain_opentype(self):
        # Cooper is a local OFL fixture, not a proprietary font. Sabon's CFF
        # staging is covered by the validation owner's real artifact run.
        with tempfile.TemporaryDirectory() as temp:
            woff2 = ROOT / 'website/static/fonts/cooper/Cooper-Black.woff2'
            hashes = CARDS.stage_fonts({'Cooper': woff2}, Path(temp) / 'fonts')
            with CARDS.Font(Path(temp) / 'fonts/Cooper.ttf') as font:
                self.assertIsNone(font.flavor)
                self.assertIn('glyf', font)
            self.assertEqual(hashes, {'Cooper': CARDS.hashlib.sha256(woff2.read_bytes()).hexdigest()})

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
                    patch.object(CARDS, 'stage_card', return_value={}), \
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
