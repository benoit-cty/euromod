"""Build the two client charts of docs/jrc_models_benchmark.md (§10.9–10.11).

    python docs/jrc_summary_charts.py      # writes jrc_summary_simple.svg, jrc_summary_by_country.svg

Counts come from `nomokrisis-eval benchmark-report <run>`: ready to accept,
wrong proposals and left to the analyst, over the legislation-based cases.
"""

from html import escape
from pathlib import Path

HERE = Path(__file__).parent
BLUE, RED, GREY = "#2a78d6", "#d03b3b", "#c3c2b7"
INK, MUTED, FAINT, RULE, BG = "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#fcfcfb"
FONT = "system-ui, -apple-system, 'Segoe UI', Helvetica, Arial, sans-serif"

MODELS = [
    ("GPT (baseline)", "Reference. Not usable at JRC."),
    ("MiniMax M2.7", "JRC's current model."),
    ("DeepSeek V4 Flash", "Candidate. MIT licence, smaller."),
]

# (ready, wrong, total) per model; None = not run. Runs 238–246 for the four
# countries (17–19 Nov); runs 260 (GPT, 24 Nov) and 264 (DeepSeek, 25 Nov) for
# the Netherlands. MiniMax (run 263) is unfinished: 13 cases rate-limited.
COUNTRIES = [
    ("Lithuania", "Consolidated law in the corpus", [(42, 0, 47), (36, 0, 47), (37, 0, 47)]),
    ("France", "Consolidated codes in the corpus", [(41, 4, 49), (35, 4, 49), (38, 5, 49)]),
    ("Netherlands", "Indexed amounts as editors' notes", [(33, 3, 50), None, (32, 4, 50)]),
    ("Spain", "Regional texts only in part", [(28, 4, 49), (29, 2, 49), (27, 2, 49)]),
    ("Ireland", "Regulations added, held as made", [(15, 3, 47), (27, 6, 47), (23, 4, 47)]),
]
FOUR = ("Lithuania", "France", "Spain", "Ireland")


def totals(names):
    out = []
    for m in range(len(MODELS)):
        rows = [c[2][m] for c in COUNTRIES if c[0] in names]
        out.append(None if any(r is None for r in rows) else tuple(map(sum, zip(*rows))))
    return out


def pct(n, total):
    return round(100 * n / total)


def bar(x0, width, y, h, counts, label, *, big, rx):
    """Three stacked segments, 2 px apart, ending at x0 + width."""
    ready, wrong, total = counts
    left = total - ready - wrong
    parts, x = [], x0
    segs = [
        (ready, BLUE, "ready to accept", "#ffffff"),
        (wrong, RED, "wrong", "#ffffff"),
        (left, GREY, "left to the analyst", INK),
    ]
    for i, (n, colour, what, ink) in enumerate(segs):
        if not n:
            continue
        w = n / total * width - (2 if i else 0)
        if i:
            x += 2
        parts.append(
            f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="{h}" rx="{rx}" fill="{colour}">'
            f"<title>{escape(label)}: {n} of {total} {what}</title></rect>"
        )
        if w > 22:
            first = i == 0
            size = (26 if first else 15) if big else 11.5
            weight = (700 if first else 400) if big else (600 if first else 400)
            ty = y + (h / 2 + (9.4 if first else 5.4) if big else 13.5)
            parts.append(
                f'<text x="{x + w / 2:.1f}" y="{ty:.1f}" font-size="{size}" font-weight="{weight}" '
                f'fill="{ink}" text-anchor="middle">{pct(n, total)}</text>'
            )
        x += w
    return parts


def svg(w, h, title, desc, body):
    return (
        "\n".join(
            [
                f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
                f'font-family="{FONT}" role="img" aria-labelledby="t d">',
                f'<title id="t">{escape(title)}</title>',
                f'<desc id="d">{escape(desc)}</desc>',
                f'<rect width="{w}" height="{h}" fill="{BG}"/>',
                *body,
                "</svg>",
            ]
        )
        + "\n"
    )


def legend(y, size, sq, xs, third):
    items = [(BLUE, "Ready to accept: right value with its legal quote"), (RED, "Wrong proposal"), (GREY, third)]
    return [
        f'<rect x="{x}" y="{y}" width="{sq}" height="{sq}" rx="2" fill="{c}"/>'
        f'<text x="{x + sq + 7}" y="{y + sq - 1.5}" font-size="{size}" fill="{MUTED}">{escape(t)}</text>'
        for x, (c, t) in zip(xs, items)
    ]


def simple():
    body = [
        f'<text x="24" y="40" font-size="22" font-weight="600" fill="{INK}">Models JRC can host do as well as GPT</text>',
        f'<text x="24" y="66" font-size="14" fill="{MUTED}">Out of 100 EUROMOD parameters set by legislation, '
        "how many can the agent update on its own?</text>",
        f'<text x="24" y="86" font-size="14" fill="{MUTED}">Panel of 200 parameters from France, Spain, Ireland and '
        "Lithuania · update from 2024 to 2025 · 17–19 Nov 2026</text>",
        *legend(110, 13, 13, (24, 408, 550), "Left to the analyst"),
    ]
    y = 150
    for (name, note), counts in zip(MODELS, totals(FOUR)):
        body += [
            f'<text x="24" y="{y + 20}" font-size="16" font-weight="600" fill="{INK}">{escape(name)}</text>',
            f'<text x="24" y="{y + 39}" font-size="12.5" fill="{MUTED}">{escape(note)}</text>',
            *bar(300, 600, y, 46, counts, name, big=True, rx=4),
        ]
        y += 78
    # The Netherlands joined after the three-model runs, on a newer prompt: kept apart.
    nl = next(c for c in COUNTRIES if c[0] == "Netherlands")[2]
    done = [(m, c) for m, c in zip(MODELS, nl) if c]
    body += [
        f'<line x1="24" y1="{y + 6}" x2="916" y2="{y + 6}" stroke="{RULE}"/>',
        f'<text x="24" y="{y + 32}" font-size="14" font-weight="600" fill="{INK}">Netherlands, added 24 Nov · 50 parameters'
        " · newer prompt, so not added to the total above</text>",
    ]
    y += 44
    for (name, _), c in done:
        body += [
            f'<text x="24" y="{y + 20}" font-size="16" font-weight="600" fill="{INK}">{escape(name)}</text>',
            *bar(300, 600, y, 46, c, f"Netherlands, {name}", big=True, rx=4),
        ]
        y += 58
    missing = [name for (name, _), c in zip(MODELS, nl) if not c]
    if missing:
        body.append(
            f'<text x="24" y="{y + 8}" font-size="12.5" fill="{MUTED}">{escape(", ".join(missing))}: '
            "not finished on the Netherlands yet.</text>"
        )
        y += 18
    y += 20
    body += [
        f'<line x1="24" y1="{y}" x2="916" y2="{y}" stroke="{RULE}"/>',
        f'<text x="24" y="{y + 24}" font-size="12.5" fill="{MUTED}">The three models are within 2 points of each other: '
        "with 192 parameters, that is inside the run-to-run variation.</text>",
        f'<text x="24" y="{y + 42}" font-size="12.5" fill="{FAINT}">Ready to accept = the proposal has the right value and '
        "a quote checked word for word in the law. Wrong = a different value passed the checks.</text>",
        f'<text x="24" y="{y + 60}" font-size="12.5" fill="{FAINT}">The result differs a lot between countries: '
        "see the per-country chart.</text>",
    ]
    return svg(
        940,
        y + 82,
        "Models JRC can host do as well as GPT",
        "Per 100 legislation-based parameters of the four-country panel: proposals ready to accept, wrong "
        "proposals and parameters left to the analyst, for GPT, MiniMax M2.7 and DeepSeek V4 Flash; and GPT "
        "and DeepSeek on the 50 Dutch parameters added on 24 Nov 2026.",
        body,
    )


def by_country():
    x0, width, row, top = 330, 540, 22, 118
    groups = [("All four countries", "192 parameters", None, totals(FOUR))] + [
        (name, f"{next(c for c in counts if c)[2]} parameters", note, counts) for name, note, counts in COUNTRIES
    ]
    bottom = top + len(groups) * 86 - 20
    body = [
        f'<text x="24" y="34" font-size="18" font-weight="600" fill="{INK}">The result depends on the country more than on the model</text>',
        f'<text x="24" y="56" font-size="13" fill="{MUTED}">Per 100 legislation-based parameters · panel of 250 '
        "parameters, system year 2024 → 2025 · 17–24 Nov 2026</text>",
        *legend(76, 12.5, 12, (24, 387, 519), "Left to the analyst: not found, rejected or error"),
    ]
    for i in range(5):
        x = x0 + i * width / 4
        body += [
            f'<line x1="{x:.1f}" y1="110" x2="{x:.1f}" y2="{bottom}" stroke="{RULE}" stroke-width="1"/>',
            f'<text x="{x:.1f}" y="{bottom + 16}" font-size="11.5" fill="{FAINT}" text-anchor="middle">{i * 25}</text>',
        ]
    y = top
    for name, size, note, counts in groups:
        body += [
            f'<text x="24" y="{y + 13}" font-size="13.5" font-weight="600" fill="{INK}">{escape(name)}</text>',
            f'<text x="24" y="{y + 30}" font-size="11.5" fill="{MUTED}">{size}</text>',
        ]
        if note:
            body.append(
                f'<text x="24" y="{y + 46}" font-size="11.5" font-style="italic" fill="{MUTED}">{escape(note)}</text>'
            )
        for r, ((model, _), c) in enumerate(zip(MODELS, counts)):
            ry = y + r * row
            body.append(
                f'<text x="318" y="{ry + 13}" font-size="12" fill="{MUTED}" text-anchor="end">{escape(model)}</text>'
            )
            if c is None:
                body.append(
                    f'<text x="{x0 + 6}" y="{ry + 13}" font-size="11.5" font-style="italic" fill="{FAINT}">not finished: OpenRouter rate limits</text>'
                )
            else:
                body += bar(x0, width, ry, 18, c, f"{name}, {model}", big=False, rx=3)
        y += 86
    foot = bottom + 40
    body += [
        f'<text x="24" y="{foot}" font-size="11.5" fill="{FAINT}">Ground truth is EUROMOD&#x27;s own 2025 value. One run per '
        "model; about 50 cases per country, so one case is 2 points.</text>",
        f'<text x="24" y="{foot + 16}" font-size="11.5" fill="{FAINT}">GPT: gpt-6-luna proposes, gpt-6.1-sol checks. MiniMax '
        "and DeepSeek each check their own proposals, as on a one-model server.</text>",
        f'<text x="24" y="{foot + 32}" font-size="11.5" fill="{FAINT}">Spain was run again on 18 Nov (regional codes); Ireland '
        "on 19 Nov, after adding 43 statutory instruments and the search for the held figure.</text>",
        f'<text x="24" y="{foot + 48}" font-size="11.5" fill="{FAINT}">The Netherlands joined on 24 Nov (GPT run 260, DeepSeek run 264, newer '
        "prompt 0.16.0); its total is kept out of «All four countries».</text>",
    ]
    return svg(
        940,
        foot + 64,
        "Share of parameters ready to accept on the five-country panel",
        "Per 100 legislation-based parameters: ready to accept, wrong proposals, and left to the analyst, for "
        "GPT, MiniMax M2.7 and DeepSeek V4 Flash on France, Spain, Ireland and Lithuania, and for GPT on the "
        "Netherlands, 2024 to 2025, in total and per country.",
        body,
    )


if __name__ == "__main__":
    (HERE / "jrc_summary_simple.svg").write_text(simple())
    (HERE / "jrc_summary_by_country.svg").write_text(by_country())
