#!/usr/bin/env python3
"""Render the portfolio's social card (static/social-card.png).

The design is the album graph viewer's card (beets-plugins,
plugins/embed/viewer/scripts/gen_social_card.py), itself adapted from the
blog's Open Graph cards (scripts/gen_og_cards.py in the blog repo): same
2400x1260 canvas, paper ground, accent band, Cooper faces, muted meta line,
and a hostname wordmark bottom-right. Where the album card draws a
constellation from its map, this one pins the header's torn theatre ticket
in the top corner, so the card quotes the site the same way. No photos or
resume content appear on the card.

Fonts are the committed Cooper TTF faces in fonts/cooper/ (SIL OFL 1.1, see
fonts/cooper/LICENSE.md), converted once from the blog's woff2 with
woff2_decompress because Pillow cannot read woff2. Everything else is stock
Pillow, which the repository dev shell provides:

    cd website
    python3 scripts/gen_social_card.py

Layout is deterministic: re-running with the same Pillow version reproduces
the card byte for byte.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

# Palette: the site's own light chrome (src/styles/site.css :root), which is
# the blog's light theme. The portfolio has no dark theme, so neither does
# its card.
PAPER = (247, 244, 237)   # --paper   #f7f4ed
ACCENT = (181, 74, 0)     # --accent  #b54a00
INK = (43, 37, 32)        # --ink     #2b2520
MUTED = (111, 100, 86)    # --muted   #6f6456
BORDER = (221, 214, 198)  # --border  #ddd6c6
CARD_STOCK = (252, 250, 245)  # .ticket-card #fcfaf5

# Canvas. 1200x630 is the Open Graph minimum; render at 2x so the card is
# natively sharp on high-density timelines, and declare the true size in
# PageHead.svelte's og:image dimensions.
SCALE = 2
BASE_W, BASE_H = 1200, 630
W, H = BASE_W * SCALE, BASE_H * SCALE
MARGIN = 80 * SCALE
BAND_H = 18 * SCALE       # accent band thickness across the top
CONTENT_W = W - 2 * MARGIN

TITLE_MAX = 148 * SCALE   # short name: start at display size, shrink to fit
TITLE_MIN = 50 * SCALE
TITLE_STEP = 2 * SCALE
TITLE_LINE_RATIO = 1.12

DESC_SIZE = 34 * SCALE
DESC_MAX_LINES = 2
DESC_LINE_RATIO = 1.30
DESC_GAP = 30 * SCALE

META_SIZE = 34 * SCALE
SITE_SIZE = 32 * SCALE
BODY_BOTTOM_GAP = 32 * SCALE

# Card copy. The title is the name the site carries, the subtitle the
# resume's own header line, and the meta line the site's navigation, so a
# reshared card still says what is behind the link.
TITLE = "Finn Rutis"
DESCRIPTION = "Musical theatre performer and voiceover artist in New York City"
META = "Resume  ·  Performance reel  ·  Contact"
SITE = "finnrut.is"

# The header's ticket stub (.ticket-card in site.css), scaled up from its
# 2.75rem height. Every other measure below is that rule's rem value as a
# fraction of the height, so the stub keeps the header's proportions.
TICKET_H = 92 * SCALE
TICKET_SEAT = "ORCH · ROW F"
TICKET_MARK = "Rutis"
TICKET_TILT = 4           # degrees counterclockwise: CSS rotate(-4deg)
TICKET_TOP = BAND_H + 52 * SCALE
TICKET_SUPERSAMPLE = 3    # draw large, then downsample, for a clean tear
# The torn right edge, verbatim from the clip-path: (x%, y%) down the tear.
TICKET_TEAR = [
    (88, 0), (90.5, 4), (88.5, 8), (91, 12), (89, 17), (92, 21), (89.5, 26),
    (91, 31), (88, 35), (90.5, 40), (89, 45), (92, 49), (89.5, 54),
    (91.5, 59), (88.5, 63), (91, 68), (89, 73), (92, 77), (89.5, 82),
    (91, 87), (88.5, 92), (90.5, 96), (89, 100),
]

FONT_DIR = Path(__file__).parent / "fonts" / "cooper"
OUT = Path(__file__).parents[1] / "static" / "social-card.png"

# Flat color plus antialiased text palette-quantizes losslessly to the eye;
# only cross the threshold into quantization when a render grows past it.
MAX_BYTES = 600 * 1024
QUANTIZE_COLORS = 64


def lerp(a, b, t):
    """Blend two RGB tuples; used to derive quiet colors from the palette."""
    return tuple(round(x + (y - x) * t) for x, y in zip(a, b))


SECONDARY = lerp(MUTED, INK, 0.4)


def load_font(name, size):
    return ImageFont.truetype(str(FONT_DIR / name), size)


def text_w(draw, text, font):
    return draw.textlength(text, font=font)


def wrap(draw, text, font, max_w):
    """Greedy word wrap to max_w pixels. Returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = f"{cur} {word}".strip()
        if text_w(draw, trial, font) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_title(draw, text, avail_w, avail_h):
    """Shrink the unwrapped title until its measured bounds fit the space."""
    for size in range(TITLE_MAX, TITLE_MIN - 1, -TITLE_STEP):
        font = load_font("Cooper-Black.ttf", size)
        left, _, right, _ = draw.textbbox((0, 0), text, font=font, anchor="la")
        block_h = int(size * TITLE_LINE_RATIO)
        if (0 <= left and right <= avail_w
                and text_w(draw, text, font) <= avail_w and block_h <= avail_h):
            return font, [text]
    raise ValueError("Title cannot fit on one line within the available space")


def fit_description(draw, text, font, max_lines):
    """Wrap to at most max_lines, ellipsising the last line if it overflows."""
    lines = wrap(draw, text, font, CONTENT_W)
    if len(lines) <= max_lines:
        return lines
    lines = lines[:max_lines]
    last = lines[-1]
    while last and text_w(draw, last + "…", font) > CONTENT_W:
        last = last.rsplit(" ", 1)[0] if " " in last else last[:-1]
    lines[-1] = last.rstrip(" ,;:.") + "…"
    return lines


def draw_tracked(draw, xy, text, font, fill, tracking):
    """Draw text with letter-spacing, which Pillow has no option for."""
    x, y = xy
    for char in text:
        draw.text((x, y), char, font=font, fill=fill, anchor="ls")
        x += text_w(draw, char, font) + tracking


def tracked_w(draw, text, font, tracking):
    return sum(text_w(draw, char, font) for char in text) + tracking * (len(text) - 1)


def render_ticket():
    """The header's ticket stub as a tilted RGBA sprite with its shadow.

    Drawn at TICKET_SUPERSAMPLE times its size so the torn edge and the
    rotation antialias, then reduced. The shadow is the CSS drop-shadow
    (0 2px 3px, ink at 14%) scaled by the same factor as the stub.
    """
    ss = TICKET_SUPERSAMPLE
    h = TICKET_H * ss
    em = h / 2.75             # one site rem at this size
    seat_font = load_font("Cooper-Regular.ttf", round(0.5 * em))
    mark_font = load_font("Cooper-Black.ttf", round(1.15 * em))
    tracking = 0.08 * seat_font.size

    probe = ImageDraw.Draw(Image.new("L", (1, 1)))
    pad_left, pad_right = 0.85 * em, 1.1 * em
    text_box = max(tracked_w(probe, TICKET_SEAT, seat_font, tracking),
                   text_w(probe, TICKET_MARK, mark_font))
    w = round(pad_left + text_box + pad_right)

    card = Image.new("RGBA", (w, h), CARD_STOCK + (255,))
    draw = ImageDraw.Draw(card)
    draw.rectangle([0, 0, round(0.3 * em), h], fill=ACCENT)
    draw.rectangle([0, 0, w - 1, h - 1], outline=BORDER, width=max(1, round(em / 16)))

    # Seat line over mark, the pair centered as the grid's align-content does.
    gap = 0.15 * em
    seat_asc, _ = seat_font.getmetrics()
    mark_asc, _ = mark_font.getmetrics()
    seat_cap = -probe.textbbox((0, 0), "O", font=seat_font, anchor="ls")[1]
    mark_cap = -probe.textbbox((0, 0), "R", font=mark_font, anchor="ls")[1]
    block = seat_cap + gap + mark_cap
    seat_base = (h - block) / 2 + seat_cap
    mark_base = seat_base + gap + mark_cap
    draw_tracked(draw, (pad_left, seat_base), TICKET_SEAT, seat_font, MUTED, tracking)
    draw.text((pad_left, mark_base), TICKET_MARK, font=mark_font, fill=INK, anchor="ls")

    mask = Image.new("L", (w, h), 0)
    outline = [(0, 0)] + [(w * x / 100, h * y / 100) for x, y in TICKET_TEAR] + [(0, h)]
    ImageDraw.Draw(mask).polygon(outline, fill=255)
    card.putalpha(mask)

    card = card.rotate(TICKET_TILT, resample=Image.BICUBIC, expand=True)
    card = card.resize((card.width // ss, card.height // ss), Image.LANCZOS)

    # Pad for the blur, then lay the shadow under the stub.
    px = TICKET_H / 44        # one site px at the card's size
    offset, blur = round(2 * px), round(3 * px)
    pad = blur * 3
    sprite = Image.new("RGBA", (card.width + 2 * pad, card.height + 2 * pad + offset), (0, 0, 0, 0))
    alpha = Image.new("L", sprite.size, 0)
    alpha.paste(card.getchannel("A"), (pad, pad + offset))
    alpha = alpha.filter(ImageFilter.GaussianBlur(blur)).point(lambda a: round(a * 0.14))
    sprite.paste(Image.new("RGBA", sprite.size, INK + (255,)), (0, 0), alpha)
    sprite.alpha_composite(card, (pad, pad))
    return sprite, pad


def render_card(out_path):
    img = Image.new("RGBA", (W, H), PAPER + (255,))
    draw = ImageDraw.Draw(img)

    # Accent band across the top.
    draw.rectangle([0, 0, W, BAND_H], fill=ACCENT)

    # The stub hangs in the top corner, its tilted bounds flush with the
    # right margin. Its box is off-limits to the title.
    ticket, pad = render_ticket()
    ticket_left = W - MARGIN - (ticket.width - 2 * pad)
    img.alpha_composite(ticket, (ticket_left - pad, TICKET_TOP - pad))
    ticket_bottom = TICKET_TOP + ticket.height - 2 * pad

    meta_font = load_font("Cooper-Regular.ttf", META_SIZE)
    desc_font = load_font("Cooper-Regular.ttf", DESC_SIZE)

    # Bottom row first: whatever it claims is off-limits to the title block.
    meta_zone_top = H - MARGIN - META_SIZE
    body_top = BAND_H + MARGIN
    body_bottom = meta_zone_top - BODY_BOTTOM_GAP
    body_h = body_bottom - body_top

    title_font, lines = fit_title(draw, TITLE, CONTENT_W, body_h)
    line_h = int(title_font.size * TITLE_LINE_RATIO)
    block_h = line_h * len(lines)

    # Description fills the empty middle that the short title leaves behind.
    desc_lines = []
    desc_line_h = int(DESC_SIZE * DESC_LINE_RATIO)
    if DESCRIPTION:
        room = body_h - block_h - DESC_GAP
        allowed = min(DESC_MAX_LINES, room // desc_line_h)
        if allowed >= 1:
            desc_lines = fit_description(draw, DESCRIPTION, desc_font, int(allowed))
            block_h += DESC_GAP + desc_line_h * len(desc_lines)

    y = body_top + max(0, (body_h - block_h) // 2)
    title_right = MARGIN + max(text_w(draw, line, title_font) for line in lines)
    title_top = y + draw.textbbox((0, 0), lines[0], font=title_font, anchor="la")[1]
    if title_right > ticket_left and title_top < ticket_bottom:
        raise ValueError("Title runs into the ticket stub; lower TICKET_TOP or shorten TITLE")
    for line in lines:
        draw.text((MARGIN, y), line, font=title_font, fill=ACCENT, anchor="la")
        y += line_h
    if desc_lines:
        y += DESC_GAP
        for line in desc_lines:
            draw.text((MARGIN, y), line, font=desc_font, fill=SECONDARY, anchor="la")
            y += desc_line_h

    # Meta line and site identity share a baseline at the bottom margin, so the
    # attribution travels with a card that gets reshared without its link.
    baseline = H - MARGIN
    draw.text((MARGIN, baseline), META, font=meta_font, fill=SECONDARY, anchor="ls")
    site_font = load_font("Cooper-Bold.ttf", SITE_SIZE)
    draw.text((W - MARGIN, baseline), SITE, font=site_font, fill=ACCENT, anchor="rs")

    img = img.convert("RGB")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(out_path, "PNG", optimize=True)
    if out_path.stat().st_size > MAX_BYTES:
        img.quantize(colors=QUANTIZE_COLORS).save(out_path, "PNG", optimize=True)
    print(f"{out_path}  {out_path.stat().st_size / 1024:.1f} KiB")


if __name__ == "__main__":
    render_card(OUT)
