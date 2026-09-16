from tokens import *

PHASES = [
    ("01", "Pre-Onboarding"), ("02", "Communication"), ("03", "System Entry"),
    ("04", "First Communication"), ("05", "Agreement"), ("06", "Post-Onboarding"),
    ("07", "Relationship"),
]

def stepper(active):
    """active = 1..7 — เฟสก่อนหน้าถือว่าผ่านแล้ว"""
    cells = []
    for i, (num, name) in enumerate(PHASES, start=1):
        if i < active:
            dot = f'<div style="width:26px;height:26px;border-radius:999px;background:{SUCCESS};display:grid;place-items:center">{icon(I_CHECK,15,"#0F172A")}</div>'
            col, weight = TXT2, "500"
        elif i == active:
            dot = (f'<div style="width:26px;height:26px;border-radius:999px;background:{PRIMARY};'
                   f'box-shadow:0 0 0 4px rgba(59,130,246,.22);display:grid;place-items:center">'
                   f'<div style="width:8px;height:8px;border-radius:999px;background:#fff"></div></div>')
            col, weight = TXT, "700"
        else:
            dot = f'<div style="width:26px;height:26px;border-radius:999px;border:1.5px solid {DIVIDER}"></div>'
            col, weight = TXT3, "500"
        line = ("" if i == len(PHASES) else
                f'<div style="flex-grow:1;height:1.5px;background:{SUCCESS if i < active else DIVIDER};margin:0 10px"></div>')
        cells.append(f"""<div class="row grow" style="gap:0">
  <div class="col" style="gap:7px;align-items:center;min-width:104px">
    {dot}
    <div class="col" style="gap:0;align-items:center">
      <span style="font-size:11px;font-weight:700;letter-spacing:.08em;color:{col}">{num}</span>
      <span style="font-size:12px;font-weight:{weight};color:{col};text-align:center;text-wrap:pretty">{name}</span>
    </div>
  </div>{line}
</div>""")
    return f'<div class="row" style="align-items:flex-start">{"".join(cells)}</div>'

def header(pct=46, status="IN PROGRESS"):
    return f"""<div class="card pad col" style="gap:18px">
  <div class="row" style="gap:14px;align-items:flex-start">
    <div class="col grow" style="gap:6px">
      <div class="row" style="gap:12px">
        <h1 class="h5">ABC Property Pattaya</h1>
        {status_chip(status)}
      </div>
      <div class="row" style="gap:22px;flex-wrap:wrap">
        <span class="cap"><span class="mut">Agency ID</span> &nbsp;AG-00238</span>
        <span class="cap"><span class="mut">Assigned Seller</span> &nbsp;K. Somchai</span>
        <span class="cap"><span class="mut">Owner</span> &nbsp;Mr. Chatchai P.</span>
        <span class="cap"><span class="mut">Created</span> &nbsp;15 Sep 2026</span>
        <span class="cap"><span class="mut">Last Updated</span> &nbsp;16 Sep 2026, 10:42</span>
      </div>
    </div>
    <button class="btn out">View Agency</button>
    <button class="btn">Save Progress</button>
  </div>

  <div class="col" style="gap:7px">
    <div class="row">
      <span class="sec">Overall Onboarding Progress</span>
      <span class="grow"></span>
      <span class="b2" style="font-weight:700;color:{PRIMARY_L}">{pct}%</span>
    </div>
    {bar(pct)}
    <span class="cap mut">18 / 39 required items completed · 2 mandatory items outstanding</span>
  </div>
</div>"""

def detail_page(active, body, h, pct=46, status="IN PROGRESS"):
    inner = f"""<div class="col" style="padding:26px 30px;gap:18px">
  {header(pct, status)}
  <div class="card pad">{stepper(active)}</div>
  {body}
</div>"""
    return page(inner, 1240, h)

def check(label, done=True, muted=False):
    if done:
        mark = f'<div style="width:19px;height:19px;border-radius:6px;background:{SUCCESS};display:grid;place-items:center;flex-shrink:0">{icon(I_CHECK,13,"#0F172A")}</div>'
        col = TXT
    else:
        mark = f'<div style="width:19px;height:19px;border-radius:6px;border:1.5px solid {DIVIDER};flex-shrink:0"></div>'
        col = TXT3 if muted else TXT2
    return (f'<div class="row" style="gap:10px;padding:5px 0">{mark}'
            f'<span class="b2" style="color:{col}">{label}</span></div>')

def panel(title, right="", body="", note=None):
    note_html = f'<p class="cap mut" style="margin:0">{note}</p>' if note else ""
    return f"""<div class="card pad col" style="gap:14px">
  <div class="row" style="gap:12px">
    <h3 class="sec grow">{title}</h3>{right}
  </div>
  {note_html}
  {body}
</div>"""

def field(label, value="", placeholder=None, w=None):
    style = f"flex-grow:1;min-width:0" if w is None else f"width:{w}px;flex-shrink:0"
    shown = value if value else f'<span class="mut">{placeholder or ""}</span>'
    return f"""<div class="col" style="gap:0;{style}">
  <p class="lbl">{label}</p>
  <div class="fld">{shown}</div>
</div>"""

def multiselect(label, chosen, rest):
    tags = "".join(
        f'<span class="chip" style="background:rgba(59,130,246,.16);color:{PRIMARY_L}">{c}</span>'
        for c in chosen)
    tags += "".join(
        f'<span class="chip" style="border:1px solid {DIVIDER};color:{TXT3}">{c}</span>'
        for c in rest)
    return f"""<div class="col" style="gap:0">
  <p class="lbl">{label}</p>
  <div class="row" style="gap:8px;flex-wrap:wrap">{tags}</div>
</div>"""
