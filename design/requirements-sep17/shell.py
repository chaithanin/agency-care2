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
