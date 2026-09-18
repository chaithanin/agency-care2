from tokens import *

def sheet(title, subtitle, body, w, h, badge=None):
    b = (f'<span class="chip" style="color:{SECOND};background:rgba(167,139,250,.16)">{badge}</span>'
         if badge else "")
    inner = f"""<div class="col" style="padding:26px 30px;gap:18px">
  <div class="row" style="gap:12px;align-items:flex-start">
    <div class="col grow" style="gap:3px">
      <div class="row" style="gap:10px"><h1 class="h5">{title}</h1>{b}</div>
      <p class="cap mut" style="margin:0">{subtitle}</p>
    </div>
  </div>
  {body}
</div>"""
    return page(inner, w, h)

def panel(title, right="", body="", note=None, grow=True):
    note_html = f'<p class="cap mut" style="margin:0">{note}</p>' if note else ""
    return f"""<div class="card pad col {'grow' if grow else ''}" style="gap:14px">
  <div class="row" style="gap:12px"><h3 class="sec grow">{title}</h3>{right}</div>
  {note_html}{body}
</div>"""

def field(label, value="", w=None, placeholder=None, required=False):
    style = "flex-grow:1;min-width:0" if w is None else f"width:{w}px;flex-shrink:0"
    star = f'<span style="color:{ERROR}">&nbsp;*</span>' if required else ""
    shown = value if value else f'<span class="mut">{placeholder or ""}</span>'
    return (f'<div class="col" style="gap:0;{style}"><p class="lbl">{label}{star}</p>'
            f'<div class="fld">{shown}</div></div>')

def check(label, on=True):
    mark = (f'<div style="width:18px;height:18px;border-radius:5px;background:{SUCCESS};'
            f'display:grid;place-items:center;flex-shrink:0">{icon(I_CHECK,12,"#0F172A")}</div>' if on else
            f'<div style="width:18px;height:18px;border-radius:5px;border:1.5px solid {DIVIDER};flex-shrink:0"></div>')
    return (f'<div class="row" style="gap:10px;padding:5px 0">{mark}'
            f'<span class="b2" style="color:{TXT if on else TXT2}">{label}</span></div>')

def note_box(kind, text, extra=""):
    c = {"warn": WARNING, "error": ERROR, "ok": SUCCESS, "info": PRIMARY_L}[kind]
    bg = {"warn": "rgba(251,191,36,.10)", "error": "rgba(239,68,68,.10)",
          "ok": "rgba(34,197,94,.08)", "info": "rgba(59,130,246,.10)"}[kind]
    ic = I_CHECK if kind == "ok" else I_WARN
    return (f'<div class="row" style="gap:10px;background:{bg};border:1px solid {c}55;'
            f'border-radius:14px;padding:11px 14px">{icon(ic,16,c)}'
            f'<span class="b2 grow" style="color:{c};font-weight:600">{text}</span>{extra}</div>')

def big(n, label, color=None):
    return (f'<div class="col" style="gap:1px"><span style="font-size:26px;font-weight:700;'
            f'letter-spacing:-0.02em;color:{color or TXT}">{n}</span>'
            f'<span class="cap mut">{label}</span></div>')


def tabs(names, active):
    out = []
    for n in names:
        on = n == active
        style = (f'color:{TXT};border-bottom:2px solid {PRIMARY}' if on
                 else f'color:{TXT3};border-bottom:2px solid transparent')
        out.append(f'<div style="padding:9px 2px;font-size:14px;font-weight:600;{style}">{n}</div>')
    return (f'<div class="row" style="gap:26px;border-bottom:1px solid {DIVIDER}">'
            f'{"".join(out)}</div>')


def kpi_strip(items):
    """[(value, label, color)] -- the KPI strip at the top of a page."""
    cells = []
    for v, l, c in items:
        cells.append(f'''<div class="col" style="gap:2px;padding:12px 18px;background:{SURFACE};
          border:1px solid {DIVIDER};border-radius:14px;min-width:132px">
          <span style="font-size:20px;font-weight:700;letter-spacing:-.02em;color:{c or TXT}">{v}</span>
          <span class="cap mut">{l}</span></div>''')
    return f'<div class="row" style="gap:12px;flex-wrap:wrap">{"".join(cells)}</div>'


def kanban_col(title, count, cards, width=232, sub=None):
    sub_html = f'<p class="cap mut" style="margin:0">{sub}</p>' if sub else ""
    return f'''<div class="col" style="gap:10px;width:{width}px;flex-shrink:0">
  <div class="col" style="gap:2px">
    <div class="row" style="gap:8px">
      <span class="sec" style="color:{TXT}">{title}</span>
      <span class="chip" style="color:{TXT2};background:{SURFACE}">{count}</span>
    </div>{sub_html}
  </div>
  <div class="col" style="gap:9px">{"".join(cards)}</div>
</div>'''


def lead_card(name, project, meta, chip_html="", owner=None):
    owner_html = (f'<div class="row" style="gap:6px">{icon(I_USER,12,TXT3)}'
                  f'<span class="cap mut">{owner}</span></div>' if owner else "")
    return f'''<div class="col" style="gap:7px;background:{SURFACE};border:1px solid {DIVIDER};
     border-radius:14px;padding:11px 13px">
  <span class="b2" style="font-weight:600">{name}</span>
  <span class="cap mut">{project}</span>
  {chip_html}
  <div class="row" style="gap:10px;justify-content:space-between">
    <span class="cap mut">{meta}</span>{owner_html}
  </div>
</div>'''


def steps(names, active_idx):
    out = []
    for i, n in enumerate(names):
        done, on = i < active_idx, i == active_idx
        if done:
            dot = (f'<div style="width:22px;height:22px;border-radius:999px;background:{SUCCESS};'
                   f'display:grid;place-items:center;flex-shrink:0">{icon(I_CHECK,13,"#0F172A")}</div>')
            col = TXT2
        elif on:
            dot = (f'<div style="width:22px;height:22px;border-radius:999px;background:{PRIMARY};'
                   f'display:grid;place-items:center;color:#fff;font-size:12px;font-weight:700;'
                   f'flex-shrink:0">{i+1}</div>')
            col = TXT
        else:
            dot = (f'<div style="width:22px;height:22px;border-radius:999px;border:1.5px solid {DIVIDER};'
                   f'display:grid;place-items:center;color:{TXT3};font-size:12px;font-weight:700;'
                   f'flex-shrink:0">{i+1}</div>')
            col = TXT3
        bar_ = ("" if i == len(names) - 1 else
                f'<div style="height:1.5px;width:26px;background:{SUCCESS if done else DIVIDER}"></div>')
        out.append(f'<div class="row" style="gap:9px">{dot}'
                   f'<span class="b2" style="color:{col};font-weight:600">{n}</span>{bar_}</div>')
    return f'<div class="row" style="gap:9px;flex-wrap:wrap">{"".join(out)}</div>'


def timeline(entries):
    """[(when, title, detail, color)] -- the shared Activity Timeline, usable on any entity."""
    rows = []
    for i, (when, title, detail, c) in enumerate(entries):
        last = i == len(entries) - 1
        line = ("" if last else
                f'<div style="position:absolute;left:5px;top:16px;bottom:-16px;width:1px;background:{DIVIDER}"></div>')
        det = f'<span class="cap mut">{detail}</span>' if detail else ""
        rows.append(f'''<div style="position:relative;padding-left:22px">{line}
  <div style="position:absolute;left:0;top:5px;width:11px;height:11px;border-radius:999px;
       background:{c or PRIMARY};border:2px solid {PAPER}"></div>
  <div class="col" style="gap:1px">
    <span class="cap mut">{when}</span>
    <span class="b2" style="font-weight:600">{title}</span>{det}
  </div></div>''')
    return f'<div class="col" style="gap:16px">{"".join(rows)}</div>'


def table(cols, rows, widths=None):
    ws = widths or [None] * len(cols)
    head = "".join(f'<th{f" style=width:{w}px" if w else ""}>{c}</th>' for c, w in zip(cols, ws))
    body = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f"<table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>"


def modal(title, body, actions, w=420):
    return f'''<div class="card col" style="width:{w}px;gap:0;overflow:hidden;box-shadow:0 24px 64px rgba(0,0,0,.45)">
  <div class="row pad" style="gap:12px;border-bottom:1px solid {DIVIDER};padding-bottom:14px">
    <h3 class="h6 grow">{title}</h3>{icon(I_X,18,TXT3)}
  </div>
  <div class="col pad" style="gap:14px">{body}</div>
  <div class="row pad" style="gap:10px;justify-content:flex-end;border-top:1px solid {DIVIDER};padding-top:14px">
    {actions}
  </div>
</div>'''


def radio(label, on=False, note=None):
    dot = (f'<div style="width:16px;height:16px;border-radius:999px;border:5px solid {PRIMARY};'
           f'background:{PAPER};flex-shrink:0"></div>' if on else
           f'<div style="width:16px;height:16px;border-radius:999px;border:1.5px solid {DIVIDER};flex-shrink:0"></div>')
    n = f'<span class="cap mut">&nbsp;· {note}</span>' if note else ""
    return (f'<div class="row" style="gap:9px;padding:3px 0">{dot}'
            f'<span class="b2" style="color:{TXT if on else TXT2}">{label}</span>{n}</div>')


def kv(pairs, cols=2):
    """A label/value grid, used for sections on a detail page."""
    cells = []
    for k, v in pairs:
        cells.append(f'<div class="col" style="gap:2px"><span class="cap mut">{k}</span>'
                     f'<span class="b2">{v}</span></div>')
    return (f'<div style="display:grid;grid-template-columns:repeat({cols},1fr);gap:13px 20px">'
            f'{"".join(cells)}</div>')


def sect(title, body, right=""):
    return f'''<div class="col" style="gap:10px">
  <div class="row" style="gap:10px"><h4 class="sec grow">{title}</h4>{right}</div>
  {body}</div>'''


def progress(pct, color=None, label=None):
    lab = f'<span class="cap mut" style="white-space:nowrap">{label}</span>' if label else ""
    return (f'<div class="row" style="gap:12px"><div class="grow">{bar(pct, color)}</div>{lab}</div>')


# ── Components that mirror the real MUI page (web/src/pages/DealsPage.tsx) ──

STAGE_COLOR = {
  "Open": "#64748B", "1st Follow Up": "#EC407A", "2nd Follow Up": "#AB47BC",
  "3rd Follow Up": "#7E57C2", "Holding": "#78909C", "4th Follow Up": "#5C6BC0",
  "Reservation": "#FFA726", "Holding / Reservation": "#FFA726",
  "Missed": "#8D6E63", "Closed Deals": "#2E7D32", "Cancelled": "#B0593E",
}

def mui_col(label, count, units, value, cards, color=None, extra_chips="",
            highlight=False, width=250):
    """One Kanban column, drawn as DealsPage renders it: solid colour header,
    label + optional chips, then 'N deals · N units · money'."""
    c = color or STAGE_COLOR[label]
    ring = f"box-shadow:0 0 0 2px {SUCCESS};border-radius:9px;" if highlight else ""
    body = "".join(cards) or (
        f'<p class="cap" style="text-align:center;color:{TXT3};padding:16px 0;margin:0">Empty</p>')
    return f'''<div class="col" style="width:{width}px;flex-shrink:0;{ring}">
  <div style="background:{c};color:#fff;padding:6px 12px;border-radius:8px 8px 0 0">
    <div class="row" style="gap:5px">
      <span style="font-weight:700;font-size:13px;white-space:nowrap">{label}</span>{extra_chips}
    </div>
    <div style="font-size:11px;opacity:.9">{count} deals · {units} units · {value}</div>
  </div>
  <div style="background:{PAPER};border:1px solid {DIVIDER};border-top:none;
       border-radius:0 0 8px 8px;min-height:100px;padding:6px">{body}</div>
</div>'''

def mui_hdr_chip(text):
    return (f'<span style="display:inline-flex;align-items:center;height:16px;padding:0 6px;'
            f'border-radius:999px;font-size:10px;background:rgba(255,255,255,.25);color:#fff">{text}</span>')

def mui_chip(text, kind="default", h=18):
    st = {
      "default":  f"background:{SURFACE};color:{TXT2};border:1px solid {DIVIDER}",
      "info":     f"background:{INFO};color:#0F172A;border:1px solid {INFO}",
      "secondary":f"background:transparent;color:{SECOND};border:1px solid {SECOND}",
      "new":      f"background:{SUCCESS};color:#0F172A;border:1px solid {SUCCESS}",
    }[kind]
    return (f'<span style="display:inline-flex;align-items:center;height:{h}px;padding:0 7px;'
            f'border-radius:999px;font-size:10px;line-height:1;{st}">{text}</span>')

def mui_card(name, agency=None, lead_chip="No lead", chips=(), units="1 u",
             value=None, follow=None, overdue=False, avatars=2):
    bc = ERROR if overdue else DIVIDER
    ag = (f'<div style="font-size:11px;color:{TXT2};white-space:nowrap;overflow:hidden;'
          f'text-overflow:ellipsis">{agency}</div>' if agency else "")
    lc = (mui_chip(f"&#128279; {lead_chip}", "info", 20) if lead_chip != "No lead"
          else mui_chip("No lead", "default", 20))
    ch = ("".join(chips))
    chrow = (f'<div class="row" style="gap:4px;flex-wrap:wrap;margin-top:4px">{ch}</div>' if ch else "")
    av = "".join(
      f'<div style="width:19px;height:19px;border-radius:999px;background:{SURFACE};'
      f'border:1.5px solid {PAPER};margin-left:{-6 if i else 0}px;display:grid;place-items:center;'
      f'font-size:9px;color:{TXT2}">{c}</div>' for i, c in enumerate(["JS", "SL"][:avatars]))
    val = (f'<span style="font-size:11px;font-weight:700;color:{TXT2}">{value}</span>' if value else "")
    fu = ""
    if follow:
        c = ERROR if overdue else TXT2
        fu = (f'<div class="row" style="gap:4px;margin-top:4px">{icon(I_CLOCK,12,c)}'
              f'<span style="font-size:10.5px;color:{c}">{follow}</span></div>')
    return f'''<div style="background:{PAPER};border:1px solid {bc};border-radius:8px;
     padding:9px 10px;margin-bottom:6px">
  <div style="font-weight:600;font-size:13px;white-space:nowrap;overflow:hidden;
       text-overflow:ellipsis">{name}</div>
  {ag}
  <div style="margin-top:4px">{lc}</div>
  {chrow}
  <div class="row" style="gap:5px;margin-top:6px">
    <div class="row">{av}</div><div class="grow"></div>
    {mui_chip(units)}{val}
  </div>
  {fu}
</div>'''

def mui_field(label, value, w=150, caret=True):
    cv = icon(I_CHEV, 13, TXT3) if caret else ""
    return f'''<div style="position:relative;width:{w}px;flex-shrink:0">
  <div style="position:absolute;top:-7px;left:9px;background:{PAPER};padding:0 4px;
       font-size:10.5px;color:{TXT3}">{label}</div>
  <div class="row" style="gap:6px;border:1px solid {DIVIDER};border-radius:6px;
       padding:7px 10px;font-size:13px;color:{TXT2}">
    <span class="grow" style="white-space:nowrap;overflow:hidden">{value}</span>{cv}</div>
</div>'''

def mui_iconbtn(d, color=None):
    return (f'<div style="width:30px;height:30px;border-radius:999px;display:grid;'
            f'place-items:center;flex-shrink:0">{icon(d,17,color or TXT2)}</div>')

def sidebar_section(title, rows):
    body = "".join(rows)
    return (f'<div class="col" style="gap:5px;padding:9px 0;border-bottom:1px solid {DIVIDER}">'
            f'<span style="font-size:11px;font-weight:700;color:{TXT3};letter-spacing:.04em">{title}</span>'
            f'{body}</div>')

def sidebar_row(text, active=False, dot=None):
    d = (f'<span style="width:8px;height:8px;border-radius:999px;background:{dot};'
         f'flex-shrink:0"></span>' if dot else "")
    bg = f"background:{SURFACE};" if active else ""
    return (f'<div class="row" style="gap:7px;padding:4px 8px;border-radius:6px;{bg}">'
            f'{d}<span style="font-size:12.5px;color:{TXT if active else TXT2}">{text}</span></div>')

def alert(kind, text):
    c = {"warn": WARNING, "error": ERROR, "info": PRIMARY_L, "ok": SUCCESS}[kind]
    bg = {"warn": "rgba(251,191,36,.12)", "error": "rgba(239,68,68,.12)",
          "info": "rgba(59,130,246,.12)", "ok": "rgba(34,197,94,.12)"}[kind]
    return (f'<div class="row" style="gap:9px;background:{bg};border-radius:6px;padding:8px 13px">'
            f'{icon(I_WARN,16,c)}<span style="font-size:13px;color:{c}">{text}</span></div>')
