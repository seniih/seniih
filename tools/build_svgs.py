"""Generates the light/dark SVG drawings used in the profile README.

Run: python3 tools/build_svgs.py
"""

from pathlib import Path

ASSETS = Path(__file__).resolve().parent.parent / "assets"

THEMES = {
    "light": {
        "paper": "#FAFAF7",
        "ink": "#1B1F24",
        "muted": "#6B7178",
        "faint": "#E4E2DC",
        "accent": "#1F4E9C",
    },
    "dark": {
        "paper": "#0D1117",
        "ink": "#C9D1D9",
        "muted": "#8B949E",
        "faint": "#21262D",
        "accent": "#7AA2F7",
    },
}

FONT = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"


def defs(c):
    return f"""
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
      <path d="M0,1 L9,5 L0,9" fill="none" stroke="{c['ink']}" stroke-width="1.2"/>
    </marker>
    <pattern id="dots" width="20" height="20" patternUnits="userSpaceOnUse">
      <circle cx="1" cy="1" r="0.8" fill="{c['faint']}"/>
    </pattern>
  </defs>
  <style>
    text {{ font-family: {FONT}; fill: {c['ink']}; }}
    .muted {{ fill: {c['muted']}; }}
    .accent {{ fill: {c['accent']}; }}
    .label {{ font-size: 8.5px; letter-spacing: 1.2px; fill: {c['muted']}; }}
    .line {{ stroke: {c['ink']}; fill: none; }}
    .thin {{ stroke: {c['ink']}; stroke-width: 0.8; fill: none; }}
    .hidden {{ stroke: {c['muted']}; stroke-width: 1; stroke-dasharray: 6 4; fill: none; }}
  </style>"""


def sheet_frame(c, w, h, cols, rows):
    """Outer border, inner border and zone markers like a drawing sheet."""
    parts = [
        f'<rect x="0" y="0" width="{w}" height="{h}" fill="{c["paper"]}"/>',
        f'<rect x="4" y="4" width="{w - 8}" height="{h - 8}" class="line" stroke-width="1.5"/>',
        f'<rect x="20" y="20" width="{w - 40}" height="{h - 40}" class="line" stroke-width="1"/>',
    ]
    inner_w, inner_h = w - 40, h - 40
    col_w, row_h = inner_w / cols, inner_h / rows
    for i in range(cols):
        x = 20 + col_w * i
        if i:
            parts.append(f'<line x1="{x}" y1="4" x2="{x}" y2="20" class="thin"/>')
            parts.append(f'<line x1="{x}" y1="{h - 20}" x2="{x}" y2="{h - 4}" class="thin"/>')
        cx = x + col_w / 2
        parts.append(f'<text x="{cx}" y="15.5" font-size="9" text-anchor="middle" class="muted">{i + 1}</text>')
        parts.append(f'<text x="{cx}" y="{h - 8.5}" font-size="9" text-anchor="middle" class="muted">{i + 1}</text>')
    for j in range(rows):
        y = 20 + row_h * j
        if j:
            parts.append(f'<line x1="4" y1="{y}" x2="20" y2="{y}" class="thin"/>')
            parts.append(f'<line x1="{w - 20}" y1="{y}" x2="{w - 4}" y2="{y}" class="thin"/>')
        cy = y + row_h / 2 + 3
        letter = chr(ord("A") + j)
        parts.append(f'<text x="12" y="{cy}" font-size="9" text-anchor="middle" class="muted">{letter}</text>')
        parts.append(f'<text x="{w - 12}" y="{cy}" font-size="9" text-anchor="middle" class="muted">{letter}</text>')
    return "\n  ".join(parts)


def svg(w, h, title, body):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="t">
  <title id="t">{title}</title>{body}
</svg>
"""


def title_block(c):
    w, h = 880, 300
    cells = []
    # Title block table, bottom right of the sheet
    x0, y0, cw, rh = 600, 140, 130, 35
    rows = [
        [("DRAWN BY", "seniih"), ("SHEET", "01 / 01")],
        [("SCALE", "1 : 1"), ("REV", "2026.10")],
        [("LOCATION", "GEBZE, TÜRKİYE")],
        [("STATUS", "IN PROGRESS")],
    ]
    cells.append(f'<rect x="{x0}" y="{y0}" width="{cw * 2}" height="{rh * 4}" class="line" stroke-width="1"/>')
    for r, row in enumerate(rows):
        y = y0 + rh * r
        if r:
            cells.append(f'<line x1="{x0}" y1="{y}" x2="{x0 + cw * 2}" y2="{y}" class="thin"/>')
        span = cw * 2 // len(row)
        for i, (label, value) in enumerate(row):
            x = x0 + span * i
            if i:
                cells.append(f'<line x1="{x}" y1="{y}" x2="{x}" y2="{y + rh}" class="thin"/>')
            cls = ' class="accent"' if label == "STATUS" else ""
            cells.append(f'<text x="{x + 8}" y="{y + 12}" class="label">{label}</text>')
            cells.append(f'<text x="{x + 8}" y="{y + 28}" font-size="13"{cls}>{value}</text>')
    cells.append(f'<circle cx="{x0 + 108}" cy="{y0 + rh * 3 + 23.5}" r="3.5" fill="{c["accent"]}"/>')

    body = f"""{defs(c)}
  {sheet_frame(c, w, h, 6, 3)}
  <rect x="21" y="21" width="{w - 42}" height="{h - 42}" fill="url(#dots)"/>

  <text x="48" y="88" font-size="34" font-weight="700" letter-spacing="3">AHMET SENİH DEMİREL</text>
  <text x="49" y="114" font-size="12" letter-spacing="1.6" class="muted">COMPUTER ENGINEERING · GEBZE TECHNICAL UNIVERSITY</text>

  <!-- dimension line: the range of the work -->
  <line x1="48" y1="150" x2="48" y2="190" class="thin"/>
  <line x1="560" y1="150" x2="560" y2="190" class="thin"/>
  <line x1="304" y1="174" x2="304" y2="186" class="thin"/>
  <line x1="50" y1="180" x2="558" y2="180" class="line" stroke-width="1" marker-start="url(#arrow)" marker-end="url(#arrow)"/>
  <text x="304" y="168" font-size="10" letter-spacing="2" text-anchor="middle" class="accent">SPAN OF WORK</text>
  <text x="56" y="202" font-size="11" class="muted">mobile</text>
  <text x="304" y="202" font-size="11" text-anchor="middle" class="muted">backend</text>
  <text x="552" y="202" font-size="11" text-anchor="end" class="muted">metal</text>

  <text x="48" y="246" font-size="13">Ships products end to end. Takes hardware</text>
  <text x="48" y="264" font-size="13">apart to learn how it works.</text>

  <!-- registration mark -->
  <circle cx="830" cy="50" r="9" class="thin"/>
  <line x1="816" y1="50" x2="844" y2="50" class="thin"/>
  <line x1="830" y1="36" x2="830" y2="64" class="thin"/>

  {chr(10).join("  " + s for s in cells).lstrip()}"""
    return svg(w, h, "Ahmet Senih Demirel — Computer Engineering, Gebze Technical University", body)


def box(x, y, w, h, title, sub):
    return f"""<rect x="{x}" y="{y}" width="{w}" height="{h}" class="line" stroke-width="1.2"/>
  <text x="{x + 12}" y="{y + h / 2 - 2}" font-size="13" font-weight="700">{title}</text>
  <text x="{x + 12}" y="{y + h / 2 + 15}" font-size="10.5" class="muted">{sub}</text>"""


def balloon(c, n, cx, cy, tx, ty):
    """Item balloon with a leader line pointing at (tx, ty)."""
    return f"""<line x1="{tx}" y1="{ty}" x2="{cx}" y2="{cy}" class="thin"/>
  <circle cx="{tx}" cy="{ty}" r="1.8" fill="{c['ink']}"/>
  <circle cx="{cx}" cy="{cy}" r="11" fill="{c['paper']}" stroke="{c['accent']}" stroke-width="1.2"/>
  <text x="{cx}" y="{cy + 4}" font-size="11" text-anchor="middle" class="accent">{n}</text>"""


def flow(x1, y1, x2, y2, label, side="right"):
    lx = x1 + 8 if side == "right" else x1 - 8
    anchor = "start" if side == "right" else "end"
    my = (y1 + y2) / 2 + 4
    return f"""<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="line" stroke-width="1" marker-end="url(#arrow)"/>
  <text x="{lx}" y="{my}" font-size="10" text-anchor="{anchor}" class="muted">{label}</text>"""


def assembly(c):
    w, h = 880, 540
    body = f"""{defs(c)}
  {sheet_frame(c, w, h, 6, 4)}
  <rect x="21" y="21" width="{w - 42}" height="{h - 42}" fill="url(#dots)"/>

  <text x="44" y="52" font-size="14" font-weight="700" letter-spacing="2">ASSY 01 — TRENDARSA PLATFORM</text>
  <text x="836" y="52" font-size="10" letter-spacing="1.5" text-anchor="end" class="muted">EXPLODED VIEW · NOT TO SCALE</text>
  <line x1="44" y1="62" x2="836" y2="62" class="thin"/>

  <!-- clients -->
  {box(44, 96, 222, 64, "Mobile app", "Flutter · iOS + Android")}
  {box(330, 96, 222, 64, "Admin panel", "Next.js · Cloudflare Workers")}
  {box(614, 96, 222, 64, "Websites ×2", "Next.js · Netlify · i18n")}

  <!-- client → backend flows -->
  {flow(155, 160, 155, 252, "browse · admin login")}
  {flow(500, 160, 500, 252, "CRUD as admin")}
  {flow(725, 160, 725, 252, "public reads")}

  <!-- backend -->
  <rect x="44" y="252" width="792" height="112" class="line" stroke-width="1.5"/>
  <text x="56" y="272" font-size="10" letter-spacing="2" class="accent">SUPABASE</text>
  {box(60, 284, 230, 64, "Auth", "admin accounts only")}
  {box(312, 284, 256, 64, "Postgres + RLS", "public read · admin write")}
  {box(590, 284, 230, 64, "Edge Functions", "upload URL · push trigger")}

  <!-- hidden line: image uploads pass behind the backend straight to storage -->
  <path d="M342,160 L342,236 L301,236 L301,446" class="hidden" marker-end="url(#arrow)"/>
  <text x="293" y="420" font-size="10" text-anchor="end" class="muted">signed PUT · images</text>

  {flow(705, 348, 705, 446, "push")}

  <!-- infrastructure -->
  {box(150, 446, 250, 58, "Cloudflare R2", "listing images")}
  {box(560, 446, 270, 58, "Firebase Cloud Messaging", "notifications → app")}

  <!-- item balloons -->
  {balloon(c, 1, 250, 78, 240, 98)}
  {balloon(c, 2, 536, 78, 526, 98)}
  {balloon(c, 3, 820, 78, 810, 98)}
  {balloon(c, 4, 270, 384, 250, 344)}
  {balloon(c, 5, 588, 384, 560, 344)}
  {balloon(c, 6, 840, 384, 812, 344)}
  {balloon(c, 7, 420, 476, 398, 476)}
  {balloon(c, 8, 845, 428, 826, 450)}"""
    return svg(w, h, "System drawing of the TrendArsa platform: mobile app, admin panel and websites on Supabase, with Cloudflare R2 for images and Firebase Cloud Messaging for push", body)


def main():
    ASSETS.mkdir(exist_ok=True)
    for theme, colors in THEMES.items():
        suffix = "" if theme == "light" else "-dark"
        (ASSETS / f"title-block{suffix}.svg").write_text(title_block(colors), encoding="utf-8")
        (ASSETS / f"assembly{suffix}.svg").write_text(assembly(colors), encoding="utf-8")
    print("written:", ", ".join(sorted(p.name for p in ASSETS.glob("*.svg"))))


if __name__ == "__main__":
    main()
