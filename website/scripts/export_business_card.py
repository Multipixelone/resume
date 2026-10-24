"""Export the contact-page card without a public phone number.

Requires PyMuPDF. Pass the generated performance.pdf; the approved proof predates
the redrawn back and its headshot. Fonts are already embedded, so no local font
files are needed.
The site ships these two static textures and never runs the print renderer.
The print PDF stays unchanged. Its existing email and Instagram rows are
recentered as vectors for the web front, preserving the embedded typography.
"""

import argparse
from pathlib import Path

import pymupdf


def web_front(document):
    source = document[0]
    trim = source.trimbox
    email, = source.search_for("me@finnrut.is")
    instagram, = source.search_for("@finnrutis")
    row_height = (instagram.y0 - email.y0) / 2
    # The source places each icon 15pt before its text. Split in the blank
    # gutter between the perforation and icons, keeping the identity intact.
    split = email.x0 - 20
    web = pymupdf.open()
    page = web.new_page(width=trim.width, height=trim.height)
    identity = pymupdf.Rect(trim.x0, trim.y0, split, trim.y1)
    page.show_pdf_page(pymupdf.Rect(0, 0, identity.width, identity.height),
                       document, 0, clip=identity)
    for text, shift in ((email, row_height / 2), (instagram, -row_height / 2)):
        band = pymupdf.Rect(split, text.y0 - row_height / 4,
                           trim.x1, text.y0 + row_height * 3 / 4)
        target = band + (-trim.x0, shift - trim.y0, -trim.x0, shift - trim.y0)
        page.show_pdf_page(target, document, 0, clip=band)
    return web


def export(pdf: Path, output: Path):
    with pymupdf.open(pdf) as document:
        if len(document) != 2:
            raise ValueError("Expected the approved two-page Performance card")
        expected = (
            ["Finn", "Rutis", "musical theatre performer", "they / them", "me@finnrut.is", "503-267-5052", "@finnrutis"],
            ["www.finnrut.is"],
        )
        for page, text in zip(document, expected):
            if page.get_text().splitlines() != text:
                raise ValueError("Card content does not match the Performance profile")
            if tuple(page.trimbox) != (9, 9, 261, 153):
                raise ValueError("Expected 3.5 x 2-inch trim with 1/8-inch bleed")
        output.mkdir(parents=True, exist_ok=True)
        # MuPDF's PNG encoder unpremultiplies alpha. Paper and lighting remain
        # renderer properties. Only these phone-free images ship to the site.
        with web_front(document) as web:
            web[0].get_pixmap(dpi=300, alpha=True).save(output / "front-web-ink.png")
        back = document[1]
        back.set_cropbox(back.trimbox)
        # MuPDF draws image edges unsmoothed, so the turned headshot print
        # would step along its edges and shimmer as the card moves. Render at
        # four times the size and box-filter down in premultiplied alpha.
        texture = back.get_pixmap(dpi=1200, alpha=True)
        texture.shrink(2)
        texture.set_dpi(300, 300)
        texture.save(output / "back-ink.png")
        # Retire the earlier public texture so it cannot ship alongside the
        # phone-free edition when refreshing an existing output directory.
        (output / "front-ink.png").unlink(missing_ok=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pdf", required=True, type=Path)
    parser.add_argument("--output", type=Path,
                        default=Path(__file__).resolve().parents[1] / "static/cards/performance")
    args = parser.parse_args()
    export(args.pdf, args.output)
