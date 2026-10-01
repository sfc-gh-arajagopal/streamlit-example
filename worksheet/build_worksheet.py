#!/usr/bin/env python3
"""Build a printable identity-shifting worksheet PDF.

Uses the system Cairo library (no third-party Python packages).
Output: identity-shifting-worksheet.pdf next to this script.
"""

from __future__ import annotations

import argparse
import ctypes
from pathlib import Path

lib = ctypes.CDLL("libcairo.so.2")

CAIRO_FONT_SLANT_NORMAL = 0
CAIRO_FONT_SLANT_ITALIC = 1
CAIRO_FONT_WEIGHT_NORMAL = 0
CAIRO_FONT_WEIGHT_BOLD = 1
CAIRO_FORMAT_RGB24 = 1

CAIRO_PDF_METADATA_TITLE = 0
CAIRO_PDF_METADATA_AUTHOR = 1
CAIRO_PDF_METADATA_SUBJECT = 2
CAIRO_PDF_METADATA_CREATOR = 4

PAGE_W = 612.0
PAGE_H = 792.0
MARGIN_L = 54.0
MARGIN_R = 50.0
CONTENT_W = PAGE_W - MARGIN_L - MARGIN_R
CONTENT_TOP = 64.0
CONTENT_BOTTOM = 734.0

INK = (0.13, 0.13, 0.14)
NAVY = (0.14, 0.25, 0.40)
MUTED = (0.33, 0.35, 0.38)
RULE = (0.70, 0.70, 0.71)
HAIR = (0.82, 0.82, 0.83)
CARD_FILL = (0.975, 0.973, 0.968)
CARD_STROKE = (0.78, 0.76, 0.73)
CALLOUT_FILL = (0.957, 0.945, 0.918)
CALLOUT_STROKE = (0.84, 0.80, 0.72)
WHITE = (1, 1, 1)

SANS = "Inter"
SERIF = "Liberation Serif"


class Extents(ctypes.Structure):
    _fields_ = [
        ("x_bearing", ctypes.c_double),
        ("y_bearing", ctypes.c_double),
        ("width", ctypes.c_double),
        ("height", ctypes.c_double),
        ("x_advance", ctypes.c_double),
        ("y_advance", ctypes.c_double),
    ]


def _bind(name, restype, argtypes):
    fn = getattr(lib, name)
    fn.restype = restype
    fn.argtypes = argtypes
    return fn


_c_void = ctypes.c_void_p
_c_char = ctypes.c_char_p
_c_double = ctypes.c_double
_c_int = ctypes.c_int

cairo_pdf_surface_create = _bind(
    "cairo_pdf_surface_create", _c_void, [_c_char, _c_double, _c_double]
)
cairo_image_surface_create = _bind(
    "cairo_image_surface_create", _c_void, [_c_int, _c_int, _c_int]
)
cairo_create = _bind("cairo_create", _c_void, [_c_void])
cairo_destroy = _bind("cairo_destroy", None, [_c_void])
cairo_surface_destroy = _bind("cairo_surface_destroy", None, [_c_void])
cairo_surface_write_to_png = _bind(
    "cairo_surface_write_to_png", _c_int, [_c_void, _c_char]
)
cairo_status = _bind("cairo_status", _c_int, [_c_void])
cairo_surface_status = _bind("cairo_surface_status", _c_int, [_c_void])
cairo_status_to_string = _bind("cairo_status_to_string", _c_char, [_c_int])
cairo_select_font_face = _bind(
    "cairo_select_font_face", None, [_c_void, _c_char, _c_int, _c_int]
)
cairo_set_font_size = _bind("cairo_set_font_size", None, [_c_void, _c_double])
cairo_text_extents = _bind(
    "cairo_text_extents", None, [_c_void, _c_char, ctypes.POINTER(Extents)]
)
cairo_show_text = _bind("cairo_show_text", None, [_c_void, _c_char])
cairo_move_to = _bind("cairo_move_to", None, [_c_void, _c_double, _c_double])
cairo_line_to = _bind("cairo_line_to", None, [_c_void, _c_double, _c_double])
cairo_rectangle = _bind(
    "cairo_rectangle", None, [_c_void, _c_double, _c_double, _c_double, _c_double]
)
cairo_stroke = _bind("cairo_stroke", None, [_c_void])
cairo_fill = _bind("cairo_fill", None, [_c_void])
cairo_fill_preserve = _bind("cairo_fill_preserve", None, [_c_void])
cairo_set_source_rgb = _bind(
    "cairo_set_source_rgb", None, [_c_void, _c_double, _c_double, _c_double]
)
cairo_set_line_width = _bind("cairo_set_line_width", None, [_c_void, _c_double])
cairo_new_path = _bind("cairo_new_path", None, [_c_void])
cairo_show_page = _bind("cairo_show_page", None, [_c_void])
cairo_scale = _bind("cairo_scale", None, [_c_void, _c_double, _c_double])
cairo_paint = _bind("cairo_paint", None, [_c_void])
cairo_pdf_surface_set_metadata = _bind(
    "cairo_pdf_surface_set_metadata", None, [_c_void, _c_int, _c_char]
)

_scratch_surface = cairo_image_surface_create(CAIRO_FORMAT_RGB24, 8, 8)
_measure_ctx = cairo_create(_scratch_surface)


def _check(status, where):
    if status != 0:
        message = cairo_status_to_string(status).decode()
        raise RuntimeError(f"{where}: {message}")


def measure(text, font, size, weight, slant):
    cairo_select_font_face(_measure_ctx, font.encode(), slant, weight)
    cairo_set_font_size(_measure_ctx, float(size))
    ext = Extents()
    cairo_text_extents(_measure_ctx, text.encode("utf-8"), ctypes.byref(ext))
    return ext.x_advance


def wrap_text(text, width, font, size, weight, slant):
    words = text.split()
    if not words:
        return []
    lines = []
    current = words[0]
    for word in words[1:]:
        trial = f"{current} {word}"
        if measure(trial, font, size, weight, slant) <= width:
            current = trial
        else:
            lines.append(current)
            current = word
    lines.append(current)
    for line in lines:
        used = measure(line, font, size, weight, slant)
        if used > width + 0.6:
            raise RuntimeError(f"Line is wider than the page: {line!r} ({used:.1f} > {width:.1f})")
    return lines


def _shift(op, dx, dy):
    kind = op[0]
    if kind == "text":
        return (kind, op[1] + dx, op[2] + dy, *op[3:])
    if kind == "hline":
        return (kind, op[1] + dx, op[2] + dx, op[3] + dy, *op[4:])
    if kind == "rect":
        return (kind, op[1] + dx, op[2] + dy, *op[3:])
    if kind == "spaced":
        return (kind, op[1] + dx, op[2] + dy, *op[3:])
    raise RuntimeError(f"Unknown op {kind}")


class Block:
    """Drawing commands in coordinates relative to the block's top."""

    def __init__(self):
        self.ops = []
        self.y = 0.0

    def paragraph(
        self,
        text,
        size=10,
        bold=False,
        italic=False,
        font=SANS,
        color=INK,
        width=CONTENT_W,
        line_h=None,
        x=0,
        gap_after=0,
    ):
        weight = CAIRO_FONT_WEIGHT_BOLD if bold else CAIRO_FONT_WEIGHT_NORMAL
        slant = CAIRO_FONT_SLANT_ITALIC if italic else CAIRO_FONT_SLANT_NORMAL
        if line_h is None:
            line_h = size * 1.38
        lines = wrap_text(text, width - x, font, size, weight, slant)
        if not lines:
            self.y += line_h
        for line in lines:
            baseline = self.y + size * 0.80
            self.ops.append(("text", x, baseline, line, font, size, weight, slant, color))
            self.y += line_h
        self.y += gap_after

    def spacer(self, height):
        self.y += height

    def rule_field(self, label, lines, hint=None, width=CONTENT_W, x=0, pitch=15, after=7):
        self.paragraph(label, size=9.5, bold=True, line_h=12, width=width, x=x)
        if hint:
            self.paragraph(
                hint, size=8.5, color=MUTED, line_h=11, width=width, x=x, gap_after=1
            )
        else:
            self.spacer(2)
        for _ in range(lines):
            self.y += pitch
            self.ops.append(("hline", x, x + width, self.y, RULE, 0.7))
            self.y += 3
        self.spacer(after)

    def single_line(self, label, width=CONTENT_W):
        label_w = measure(label, SANS, 9.5, 1, 0) + 8
        baseline = 12
        self.ops.append(
            ("text", 0, baseline, label, SANS, 9.5, 1, 0, INK)
        )
        self.ops.append(("hline", label_w, width, baseline + 2, RULE, 0.7))
        self.y = 22


class Document:
    def __init__(self):
        self.pages = []
        self.ops = []
        self.y = CONTENT_TOP
        self._open_page()

    def _open_page(self):
        self.ops = []
        self.y = CONTENT_TOP
        self._header()

    def _header(self):
        self.ops.append(
            (
                "spaced",
                MARGIN_L,
                36,
                "IDENTITY-SHIFTING WORKSHEET",
                0.65,
                SANS,
                8,
                1,
                0,
                NAVY,
            )
        )
        right = "Print and write in the lines"
        right_w = measure(right, SANS, 8, 0, 0)
        self.ops.append(
            (
                "text",
                PAGE_W - MARGIN_R - right_w,
                36,
                right,
                SANS,
                8,
                0,
                0,
                MUTED,
            )
        )
        self.ops.append(("hline", MARGIN_L, PAGE_W - MARGIN_R, 46, HAIR, 0.6))

    def _close_page(self):
        self.ops.append(("footer",))
        self.pages.append(self.ops)
        self.ops = []

    def page_break(self):
        self._close_page()
        self._open_page()

    def finish(self):
        if self.ops:
            self._close_page()

    def place(self, block: Block):
        if block.y > (CONTENT_BOTTOM - CONTENT_TOP):
            raise RuntimeError(f"Block is taller than a page ({block.y:.1f})")
        if self.y + block.y > CONTENT_BOTTOM:
            self.page_break()
        for op in block.ops:
            self.ops.append(_shift(op, MARGIN_L, self.y))
        self.y += block.y

    def fill_notes(self):
        remain = CONTENT_BOTTOM - self.y
        if remain < 56:
            return
        label = Block()
        label.paragraph("Notes", size=9.5, bold=True, line_h=12)
        label.spacer(2)
        self.place(label)
        while self.y + 18 <= CONTENT_BOTTOM:
            self.ops.append(
                ("hline", MARGIN_L, MARGIN_L + CONTENT_W, self.y + 14, RULE, 0.7)
            )
            self.y += 18


def section(doc: Document, number: str, title: str):
    block = Block()
    block.ops.append(("rect", 0, 1, 18, 16, NAVY, None, 0))
    number_w = measure(number, SANS, 8, 1, 0)
    block.ops.append(("text", (18 - number_w) / 2, 12.5, number, SANS, 8, 1, 0, WHITE))
    block.ops.append(("text", 26, 13.2, title, SANS, 13, 1, 0, NAVY))
    block.y = 26
    doc.place(block)


def body(doc: Document, text, **kwargs):
    block = Block()
    block.paragraph(text, **kwargs)
    doc.place(block)


def spacer(doc: Document, height):
    block = Block()
    block.spacer(height)
    doc.place(block)


def field(doc: Document, label, lines, hint=None, pitch=15, after=7):
    block = Block()
    block.rule_field(label, lines, hint=hint, pitch=pitch, after=after)
    doc.place(block)


def build_story(doc: Document):
    title = Block()
    title.paragraph("Identity-shifting worksheet", size=22, bold=True, line_h=26)
    title.spacer(2)
    accent = measure("Identity", SANS, 22, 1, 0)
    title.ops.append(("hline", 0, accent, title.y, NAVY, 1.4))
    title.spacer(8)
    title.paragraph(
        "Write what you want, name the identity that is chasing it, and practice the version of you who already has it.",
        size=10.5,
        color=MUTED,
        line_h=14.5,
    )
    title.spacer(8)
    doc.place(title)

    name = Block()
    name.single_line("Name", width=330)
    # Date sits on the same row. single_line already set y; redraw date into the same block.
    date_label = "Date"
    date_x = 348
    name.ops.append(("text", date_x, 12, date_label, SANS, 9.5, 1, 0, INK))
    date_w = measure(date_label, SANS, 9.5, 1, 0) + 8
    name.ops.append(("hline", date_x + date_w, CONTENT_W, 14, RULE, 0.7))
    doc.place(name)
    spacer(doc, 8)

    howto = Block()

    def howto_inner(inner: Block):
        inner.paragraph("How to use this", size=10, bold=True, line_h=14, width=CONTENT_W - 20)
        inner.spacer(3)
        steps = [
            "Write five to seven goals.",
            "Choose one goal for this sitting.",
            "List the beliefs, thoughts, feelings, and habits that work against it.",
            "Describe the version of you who has already achieved it.",
            "Practice one behavior that version of you can do today.",
        ]
        inner_w = CONTENT_W - 20
        for index, step in enumerate(steps, start=1):
            label = f"{index}."
            label_w = measure(label, SANS, 10, 1, 0) + 8
            lines = wrap_text(step, inner_w - label_w, SANS, 10, 0, 0)
            for line_index, line in enumerate(lines):
                baseline = inner.y + 8
                if line_index == 0:
                    inner.ops.append(("text", 0, baseline, label, SANS, 10, 1, 0, NAVY))
                inner.ops.append(("text", label_w, baseline, line, SANS, 10, 0, 0, INK))
                inner.y += 15
        inner.spacer(4)
        inner.paragraph(
            "Based on the three-step exercise in The Most Misunderstood Book Ever Written About Reality.",
            size=8,
            color=MUTED,
            line_h=11,
            width=inner_w,
        )

    howto_inner(howto)
    pad = 9
    boxed = Block()
    boxed.ops.append(("rect", 0, 0, CONTENT_W, howto.y + pad * 2, CALLOUT_FILL, CALLOUT_STROKE, 0.7))
    for op in howto.ops:
        boxed.ops.append(_shift(op, pad, pad))
    boxed.y = howto.y + pad * 2
    doc.place(boxed)
    spacer(doc, 12)

    section(doc, "01", "What you want")
    body(
        doc,
        "Write five to seven major goals. A goal might be financial freedom, a business result, a relationship, clarity of purpose, or health.",
        size=9.5,
        color=INK,
        line_h=13,
        gap_after=6,
    )
    for number in range(1, 8):
        row = Block()
        label = f"{number}."
        row.ops.append(("text", 0, 13, label, SANS, 10, 1, 0, NAVY))
        row.ops.append(("hline", 18, CONTENT_W, 15, RULE, 0.7))
        row.y = 24
        doc.place(row)
    spacer(doc, 4)
    field(doc, "The one goal I will work through today", 2)
    field(doc, "What done looks like", 3)
    field(doc, "Why this matters to me", 2)
    doc.fill_notes()
    doc.page_break()

    section(doc, "02", "The identity currently trying to produce this")
    field(doc, "Today's goal", 1, after=12)
    body(
        doc,
        "Describe the version of you that is trying to reach this goal. Write the beliefs, thoughts, feelings, and habits that are out of alignment with the result.",
        size=9.5,
        line_h=13,
        gap_after=6,
    )
    field(doc, "Beliefs", 3)
    field(doc, "Thoughts", 3)
    field(doc, "Feelings", 2)
    field(doc, "Habits", 3)
    body(
        doc,
        "Active patterns. Mark any that apply, then describe them in your own words above.",
        size=9,
        bold=True,
        line_h=12,
        gap_after=4,
    )
    patterns = [
        "Procrastinating",
        "Too much time on my phone",
        "Using alcohol or other substances to cope",
        "People-pleasing",
        "Needing control",
        "Worry, anxiety, or overwhelm",
        "I have to work extremely hard to make money.",
        "I have to do things perfectly and never make a mistake.",
    ]
    _checks(doc, patterns, columns=2)
    spacer(doc, 6)
    field(doc, "What I will do less", 2)
    field(doc, "What I will do more", 2)
    doc.fill_notes()
    doc.page_break()

    section(doc, "03", "Bad plays")
    field(doc, "Today's goal", 1, after=12)
    body(
        doc,
        "A bad play is a habit, belief, or feeling you keep because some part of you thinks it will help you succeed. Name the play, the payoff you expect, and what it actually produces.",
        size=9.5,
        line_h=13,
        gap_after=3,
    )
    body(
        doc,
        "Example: the play is worry. The expected payoff is that worry will catch problems in time. What it produces is avoidance, distraction, and more worry.",
        size=8.5,
        color=MUTED,
        line_h=11.5,
        gap_after=8,
    )
    for _ in range(3):
        _play_card(doc)
    field(doc, "The one play I am working with today", 2)
    field(
        doc,
        "If I keep being this person, I am likely to keep producing",
        2,
    )
    doc.fill_notes()
    doc.page_break()

    section(doc, "04", "Assume it is already done")
    body(
        doc,
        "The goal is already accomplished. Write how that version of you thinks, feels, and decides inside your real life and your real budget.",
        size=9.5,
        line_h=13,
        gap_after=8,
    )
    for label in ("Beliefs", "Thoughts", "Feelings", "Habits"):
        field(doc, label, 2, pitch=15, after=5)
    questions = [
        "If this were already done, who would I be?",
        "How would I think differently?",
        "What would I believe differently?",
        "How would I feel differently?",
        "How would that person approach a problem?",
        "What decisions would that person make?",
        "How would that person show up today?",
    ]
    for question in questions:
        field(doc, question, 2, pitch=15, after=5)
    doc.fill_notes()
    doc.page_break()

    section(doc, "05", "Practice today")
    body(
        doc,
        "The person who already has the result is available in how you think, what you allow yourself to feel, the decisions you make, and the way you show up.",
        size=9.5,
        line_h=13,
        gap_after=6,
    )
    note = Block()

    def note_inner(inner: Block):
        inner.paragraph(
            "Choose a behavior that fits your real circumstances and your real budget. A calmer decision, an honest conversation, or a generous action you can already afford is the practice.",
            size=9,
            line_h=12.4,
            width=CONTENT_W - 22,
        )

    note_inner(note)
    pad = 8
    boxed = Block()
    boxed.ops.append(
        ("rect", 0, 0, CONTENT_W, note.y + pad * 2, CALLOUT_FILL, CALLOUT_STROKE, 0.7)
    )
    boxed.ops.append(("rect", 0, 0, 3.5, note.y + pad * 2, NAVY, None, 0))
    for op in note.ops:
        boxed.ops.append(_shift(op, 12, pad))
    boxed.y = note.y + pad * 2
    doc.place(boxed)
    spacer(doc, 8)
    field(doc, "Today's goal", 1, after=10)
    field(doc, "The old play I am setting down", 2, after=6)
    field(doc, "If this were already done, who would I be today?", 2, after=6)
    field(doc, "What I will stop doing", 2, after=6)
    field(doc, "What I will start doing", 2, after=6)
    field(doc, "Today I will practice", 2, after=6)
    field(doc, "When and where", 1, after=10)

    body(doc, "Before I close the day", size=9.5, bold=True, line_h=12, gap_after=2)
    _end_of_day(doc, "I practiced it. What I noticed")
    _end_of_day(doc, "Still to practice. What got in the way")
    spacer(doc, 3)
    body(doc, "Checklist", size=9.5, bold=True, line_h=12, gap_after=2)
    _checks(
        doc,
        [
            "I chose one goal.",
            "I named the old play.",
            "I know who I would be today.",
            "I picked a behavior for today.",
            "It fits my real life and my budget.",
            "I will practice that person today.",
        ],
        columns=2,
    )
    spacer(doc, 6)
    quote = Block()
    quote_text = "You create the result by becoming that person first."
    quote_size = 11
    quote_w = measure(quote_text, SERIF, quote_size, 0, 1)
    quote.ops.append(
        (
            "text",
            (CONTENT_W - quote_w) / 2,
            12,
            quote_text,
            SERIF,
            quote_size,
            0,
            1,
            NAVY,
        )
    )
    quote.y = 18
    doc.place(quote)


def _checks(doc: Document, items, columns):
    gap = 14
    col_w = (CONTENT_W - gap * (columns - 1)) / columns
    rows = [items[i : i + columns] for i in range(0, len(items), columns)]
    for row_items in rows:
        block = Block()
        row_h = 0
        for col, item in enumerate(row_items):
            x = col * (col_w + gap)
            text_w = col_w - 16
            lines = wrap_text(item, text_w, SANS, 9, 0, 0)
            line_h = 12
            block.ops.append(("rect", x, 1.5, 8.5, 8.5, None, INK, 0.8))
            for line_index, line in enumerate(lines):
                block.ops.append(
                    ("text", x + 14, 8.2 + line_index * line_h, line, SANS, 9, 0, 0, INK)
                )
            row_h = max(row_h, 8 + len(lines) * line_h)
        block.y = row_h + 4
        doc.place(block)


def _play_card(doc: Document):
    labels = [
        "Play",
        "The payoff I think it gives me",
        "What it actually produces",
    ]
    pad_x = 10
    y = 8
    inner_ops = []
    for label in labels:
        inner_ops.append(("text", pad_x, y + 9, label, SANS, 8.5, 1, 0, NAVY))
        rule_y = y + 28
        inner_ops.append(("hline", pad_x, CONTENT_W - pad_x, rule_y, RULE, 0.7))
        y = rule_y + 7
    height = y + 2
    block = Block()
    block.ops.append(("rect", 0, 0, CONTENT_W, height, CARD_FILL, CARD_STROKE, 0.8))
    block.ops.extend(inner_ops)
    block.y = height + 8
    doc.place(block)


def _end_of_day(doc: Document, label):
    block = Block()
    block.ops.append(("rect", 0, 1.5, 8.5, 8.5, None, INK, 0.8))
    block.ops.append(("text", 14, 9, label, SANS, 9.5, 0, 0, INK))
    block.y = 12
    block.y += 16
    block.ops.append(("hline", 14, CONTENT_W, block.y, RULE, 0.7))
    block.spacer(8)
    doc.place(block)


def _cy(y, y_up):
    return (PAGE_H - y) if y_up else y


def paint(ctx, ops, page_number, page_count, y_up=True):
    for op in ops:
        kind = op[0]
        if kind == "footer":
            _paint_footer(ctx, page_number, page_count, y_up)
            continue
        if kind == "text":
            _, x, baseline, text, font, size, weight, slant, color = op
            _paint_text(ctx, x, baseline, text, font, size, weight, slant, color, y_up)
        elif kind == "spaced":
            _, x, baseline, text, spacing, font, size, weight, slant, color = op
            _paint_spaced(
                ctx, x, baseline, text, spacing, font, size, weight, slant, color, y_up
            )
        elif kind == "hline":
            _, x1, x2, y, color, width = op
            cairo_set_source_rgb(ctx, *color)
            cairo_set_line_width(ctx, width)
            cairo_new_path(ctx)
            cairo_move_to(ctx, x1, _cy(y, y_up))
            cairo_line_to(ctx, x2, _cy(y, y_up))
            cairo_stroke(ctx)
        elif kind == "rect":
            _, x, y, w, h, fill, stroke, sw = op
            _paint_rect(ctx, x, y, w, h, fill, stroke, sw, y_up)
        else:
            raise RuntimeError(f"Unknown op {kind}")


def _paint_text(ctx, x, baseline, text, font, size, weight, slant, color, y_up):
    cairo_select_font_face(ctx, font.encode(), slant, weight)
    cairo_set_font_size(ctx, float(size))
    cairo_set_source_rgb(ctx, *color)
    cairo_move_to(ctx, x, _cy(baseline, y_up))
    cairo_show_text(ctx, text.encode("utf-8"))


def _paint_spaced(ctx, x, baseline, text, spacing, font, size, weight, slant, color, y_up):
    cairo_select_font_face(ctx, font.encode(), slant, weight)
    cairo_set_font_size(ctx, float(size))
    cairo_set_source_rgb(ctx, *color)
    cursor = x
    for char in text:
        cairo_move_to(ctx, cursor, _cy(baseline, y_up))
        cairo_show_text(ctx, char.encode("utf-8"))
        cursor += measure(char, font, size, weight, slant) + spacing


def _paint_rect(ctx, x, y, w, h, fill, stroke, sw, y_up):
    cairo_new_path(ctx)
    if y_up:
        cairo_rectangle(ctx, x, PAGE_H - (y + h), w, h)
    else:
        cairo_rectangle(ctx, x, y, w, h)
    if fill is not None:
        cairo_set_source_rgb(ctx, *fill)
        if stroke is not None:
            cairo_fill_preserve(ctx)
        else:
            cairo_fill(ctx)
    if stroke is not None:
        cairo_set_source_rgb(ctx, *stroke)
        cairo_set_line_width(ctx, sw)
        cairo_stroke(ctx)


def _paint_footer(ctx, page_number, page_count, y_up):
    cairo_set_source_rgb(ctx, *HAIR)
    cairo_set_line_width(ctx, 0.6)
    cairo_new_path(ctx)
    cairo_move_to(ctx, MARGIN_L, _cy(748, y_up))
    cairo_line_to(ctx, PAGE_W - MARGIN_R, _cy(748, y_up))
    cairo_stroke(ctx)
    _paint_text(
        ctx,
        MARGIN_L,
        764,
        "Who would I be if I already had it?",
        SERIF,
        8.5,
        0,
        1,
        MUTED,
        y_up,
    )
    label = f"{page_number}  /  {page_count}"
    label_w = measure(label, SANS, 8.5, 0, 0)
    _paint_text(
        ctx,
        PAGE_W - MARGIN_R - label_w,
        764,
        label,
        SANS,
        8.5,
        0,
        0,
        MUTED,
        y_up,
    )


def render_pdf(doc: Document, path: Path):
    surface = cairo_pdf_surface_create(str(path).encode(), PAGE_W, PAGE_H)
    _check(cairo_surface_status(surface), "pdf surface")
    cairo_pdf_surface_set_metadata(surface, CAIRO_PDF_METADATA_TITLE, b"Identity-Shifting Worksheet")
    cairo_pdf_surface_set_metadata(
        surface,
        CAIRO_PDF_METADATA_SUBJECT,
        b"Printable checklist for the three-step identity exercise",
    )
    cairo_pdf_surface_set_metadata(surface, CAIRO_PDF_METADATA_CREATOR, b"Identity-Shifting Worksheet")
    ctx = cairo_create(surface)
    _check(cairo_status(ctx), "pdf context")
    total = len(doc.pages)
    for index, ops in enumerate(doc.pages, start=1):
        paint(ctx, ops, index, total)
        cairo_show_page(ctx)
        _check(cairo_status(ctx), f"page {index}")
    cairo_destroy(ctx)
    cairo_surface_destroy(surface)


def render_previews(doc: Document, directory: Path, scale: float):
    directory.mkdir(parents=True, exist_ok=True)
    width = int(PAGE_W * scale)
    height = int(PAGE_H * scale)
    total = len(doc.pages)
    paths = []
    for index, ops in enumerate(doc.pages, start=1):
        surface = cairo_image_surface_create(CAIRO_FORMAT_RGB24, width, height)
        ctx = cairo_create(surface)
        cairo_set_source_rgb(ctx, 1, 1, 1)
        cairo_paint(ctx)
        cairo_scale(ctx, scale, scale)
        paint(ctx, ops, index, total, y_up=False)
        _check(cairo_status(ctx), f"preview {index}")
        out = directory / f"page-{index}.png"
        status = cairo_surface_write_to_png(surface, str(out).encode())
        _check(status, f"png {index}")
        cairo_destroy(ctx)
        cairo_surface_destroy(surface)
        paths.append(out)
    return paths


def build(output: Path, preview_dir: Path | None = None):
    doc = Document()
    build_story(doc)
    doc.finish()
    output.parent.mkdir(parents=True, exist_ok=True)
    render_pdf(doc, output)
    if not output.exists() or output.stat().st_size < 1000:
        raise RuntimeError("PDF was not written")
    if output.read_bytes()[:5] != b"%PDF-":
        raise RuntimeError("Output is not a PDF")
    previews = []
    if preview_dir is not None:
        previews = render_previews(doc, preview_dir, scale=2)
    return len(doc.pages), previews


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    default_out = Path(__file__).resolve().parent / "identity-shifting-worksheet.pdf"
    parser.add_argument("--output", type=Path, default=default_out)
    parser.add_argument("--preview", type=Path, default=None, help="Directory for page PNGs")
    args = parser.parse_args()
    count, previews = build(args.output, args.preview)
    print(f"Wrote {args.output} ({count} pages)")
    for path in previews:
        print(f"Preview {path}")


if __name__ == "__main__":
    main()
