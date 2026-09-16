from tokens import *

TABS = ["OVERVIEW", "CONTACTS", "SEND HISTORY", "TEMPLATES", "ANALYTICS"]

def tabs(active):
    out = []
    for t in TABS:
        on = t == active
        style = (f"color:{PRIMARY_L};border-bottom:2px solid {PRIMARY};font-weight:700"
                 if on else f"color:{TXT3};border-bottom:2px solid transparent;font-weight:600")
        out.append(f'<div style="padding:11px 18px;font-size:13px;letter-spacing:.04em;{style}">{t}</div>')
    return (f'<div class="row" style="gap:2px;border-bottom:1px solid {DIVIDER}">'
            f'{"".join(out)}</div>')

def page_shell(active_tab, body, w, h, title="LINE Broadcast Center",
               subtitle="ประกาศและข้อความถึงทีมขาย ลูกค้า และเอเจนซี่ผ่าน LINE OA", actions=""):
    inner = f"""<div class="col" style="padding:26px 30px;gap:18px">
  <div class="row" style="gap:12px">
    <div class="col grow" style="gap:3px">
      <h1 class="h5">{title}</h1>
      <p class="cap mut" style="margin:0">{subtitle}</p>
    </div>
    {actions}
  </div>
  {tabs(active_tab)}
  {body}
</div>"""
    return page(inner, w, h)

def stat(n, label, color, warn=False):
    border = f"1px solid {WARNING}" if warn else f"1px solid {DIVIDER}"
    bg = "rgba(251,191,36,.07)" if warn else PAPER
    return f"""<div class="col" style="background:{bg};border:{border};border-radius:20px;
     padding:16px 20px;gap:2px;min-width:160px;cursor:pointer">
  <div style="font-size:28px;font-weight:700;letter-spacing:-0.02em;color:{color}">{n}</div>
  <div class="cap" style="font-weight:600;letter-spacing:.04em">{label}</div>
</div>"""

def role_chip(kind):
    m = {"Sales":    (INFO,    "rgba(56,189,248,.14)"),
         "Customer": (SUCCESS, "rgba(34,197,94,.14)"),
         "Agency":   (SECOND,  "rgba(167,139,250,.16)"),
         "Partner":  (PRIMARY_L,"rgba(59,130,246,.16)"),
         "Other":    (TXT2,    "rgba(203,213,225,.10)")}
    c, bg = m[kind]
    return f'<span class="chip" style="color:{c};background:{bg}">{kind}</span>'

UNCLASSIFIED_CHIP = (f'<span class="chip" style="color:{WARNING};'
                     f'background:rgba(251,191,36,.15)">Unclassified</span>')

def status_dot(s):
    c = {"Active": SUCCESS, "New": INFO, "Blocked": ERROR, "Inactive": TXT3}[s]
    return (f'<span class="row" style="gap:6px"><span style="width:7px;height:7px;'
            f'border-radius:999px;background:{c};display:inline-block"></span>'
            f'<span class="b2" style="color:{c}">{s}</span></span>')

def panel(title, right="", body="", note=None):
    note_html = f'<p class="cap mut" style="margin:0">{note}</p>' if note else ""
    return f"""<div class="card pad col" style="gap:14px">
  <div class="row" style="gap:12px"><h3 class="sec grow">{title}</h3>{right}</div>
  {note_html}
  {body}
</div>"""

def field(label, value="", w=None, placeholder=None):
    style = "flex-grow:1;min-width:0" if w is None else f"width:{w}px;flex-shrink:0"
    shown = value if value else f'<span class="mut">{placeholder or ""}</span>'
    return f"""<div class="col" style="gap:0;{style}">
  <p class="lbl">{label}</p>
  <div class="fld">{shown}</div>
</div>"""

def pill(label, on=False):
    return (f'<div class="row fld" style="gap:8px;padding:8px 12px;border-radius:999px;cursor:pointer">'
            f'<span class="b2" style="color:{TXT if on else TXT2}">{label}</span>{icon(I_CHEV,14,TXT3)}</div>')

def steps(active):
    names = ["Audience", "Message", "Preview", "Send / Schedule"]
    out = []
    for i, n in enumerate(names, start=1):
        if i < active:  dot, col = SUCCESS, TXT2
        elif i == active: dot, col = PRIMARY, TXT
        else: dot, col = DIVIDER, TXT3
        mark = (icon(I_CHECK, 13, "#0F172A") if i < active
                else f'<span style="font-size:11px;font-weight:700;color:{"#fff" if i==active else TXT3}">{i}</span>')
        circle = (f'<div style="width:24px;height:24px;border-radius:999px;background:{dot};'
                  f'display:grid;place-items:center">{mark}</div>' if i <= active else
                  f'<div style="width:24px;height:24px;border-radius:999px;border:1.5px solid {DIVIDER};'
                  f'display:grid;place-items:center">{mark}</div>')
        line = "" if i == 4 else f'<div style="flex-grow:1;height:1.5px;background:{SUCCESS if i<active else DIVIDER};margin:0 12px"></div>'
        out.append(f'<div class="row grow" style="gap:0"><div class="row" style="gap:9px">'
                   f'{circle}<span class="b2" style="color:{col};font-weight:{"700" if i==active else "500"}">{n}</span>'
                   f'</div>{line}</div>')
    return f'<div class="card pad row" style="align-items:center">{"".join(out)}</div>'
