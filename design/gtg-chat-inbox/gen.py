# -*- coding: utf-8 -*-
"""โทเคนและชิ้นส่วน UI — ลอกค่าจริงจาก agency-care/web/src/theme.ts + components/Layout.tsx"""
import io, os

T = dict(
    bg="#0a0913",                      # palette.background.default
    sidebar="#100e1c",                 # Drawer PaperProps.background
    surface="rgba(26, 23, 43, 0.66)",  # palette.background.paper
    surfaceSolid="#171429",
    line="rgba(255,255,255,0.07)",     # palette.divider
    cardBorder="rgba(255,255,255,0.06)",
    ink="#ECEBF5",                     # text.primary
    muted="#9B99B8",                   # text.secondary
    accent="#7c6ff0",                  # primary.main
    accentLight="#9d93f5",             # primary.light
    accentDark="#5b4fd6",              # primary.dark
    accentInk="#FFFFFF",
    card="rgba(124,111,240,0.16)",     # primary tint (chip พื้นหลัง)
    inb="rgba(255,255,255,0.04)",      # แถวที่เลือก / hover
    warn="#fbbf24",                    # warning.main
    danger="#f87171",                  # error.main
    ok="#34d399",                      # success.main
    info="#60a5fa",
)
# body background จาก MuiCssBaseline
PAGE_BG = ("radial-gradient(1100px 700px at 82% -12%, rgba(91,79,214,0.28) 0%, rgba(91,79,214,0) 55%),"
           "radial-gradient(900px 600px at -10% 110%, rgba(79,195,247,0.10) 0%, rgba(79,195,247,0) 55%),"
           "linear-gradient(180deg, #0b0a17 0%, #08070f 100%)")
BTN_GRAD = "linear-gradient(135deg, #8b7ff5 0%, #6a5be0 100%)"
BTN_SHADOW = "0 8px 22px -8px rgba(124,111,240,0.7)"
NAV_ACTIVE = "linear-gradient(90deg, rgba(124,111,240,0.30), rgba(124,111,240,0.04))"

BODY = "'Sarabun','Inter','Roboto','Helvetica',sans-serif"
DISPLAY = BODY
MONO = "'IBM Plex Mono',ui-monospace,monospace"
DRAWER = 252

ICONS = {
 "inbox": '<path d="M4 13h4l1.6 2.6h4.8L16 13h4"/><path d="M5.6 5h12.8l2.1 7.2V19H3.5v-6.8z"/>',
 "users": '<circle cx="9.5" cy="8" r="3.2"/><path d="M3.5 19.5c0-3.3 2.7-5.6 6-5.6s6 2.3 6 5.6"/><path d="M16.5 5.4a3.1 3.1 0 0 1 0 5.4"/><path d="M18.2 13.9c1.6.7 2.3 2.2 2.3 4.4"/>',
 "bolt": '<path d="M13.2 3.5 6 13.6h5l-.9 6.9 7.6-10.4h-5.2z"/>',
 "megaphone": '<path d="M4.5 10.2v3.6h3L14 17.4V6.6L7.5 10.2z"/><path d="M17.6 9.3a3.2 3.2 0 0 1 0 5.4"/><path d="M7.5 13.8v4.1h3.1"/>',
 "chart": '<path d="M4.5 19.5V11"/><path d="M10 19.5V5"/><path d="M15.5 19.5v-6"/><path d="M21 19.5V8.5"/><path d="M3 19.5h18"/>',
 "settings": '<circle cx="12" cy="12" r="3.1"/><path d="M12 3.4v2.3M12 18.3v2.3M20.6 12h-2.3M5.7 12H3.4M18.1 5.9l-1.6 1.6M7.5 16.5l-1.6 1.6M18.1 18.1l-1.6-1.6M7.5 7.5 5.9 5.9"/>',
 "search": '<circle cx="11" cy="11" r="6.2"/><path d="m20 20-4.5-4.5"/>',
 "send": '<path d="M20.5 3.5 3.5 10.8l7 2.7 2.7 7z"/><path d="M10.5 13.5 20.5 3.5"/>',
 "plus": '<path d="M12 5.5v13M5.5 12h13"/>',
 "check": '<path d="m5.5 12.5 4.3 4.3L18.5 7.5"/>',
 "clock": '<circle cx="12" cy="12" r="8"/><path d="M12 7.6V12l3 1.9"/>',
 "key": '<circle cx="8" cy="14.5" r="3.9"/><path d="m10.8 11.7 8.7-8.7"/><path d="m16.6 5.9 2.4 2.4"/><path d="m14.4 8.1 2.4 2.4"/>',
 "link": '<path d="M10.2 13.8a4 4 0 0 0 5.7 0l2.8-2.8A4 4 0 0 0 13 5.3l-1.1 1.1"/><path d="M13.8 10.2a4 4 0 0 0-5.7 0L5.3 13a4 4 0 0 0 5.7 5.7l1.1-1.1"/>',
 "filter": '<path d="M4 6.5h16M7 12h10M10 17.5h4"/>',
 "chevron": '<path d="m9.5 6 6 6-6 6"/>',
 "chevdown": '<path d="m6.5 9.5 5.5 5.5 5.5-5.5"/>',
 "tag": '<path d="M3.5 12.2V4.5h7.7l9.3 9.3-7.7 7.7z"/><circle cx="7.6" cy="8.6" r="1.3"/>',
 "arrowdown": '<path d="M12 4.5v15"/><path d="m6.5 14 5.5 5.5L17.5 14"/>',
 "dots": '<circle cx="5.5" cy="12" r="1.4"/><circle cx="12" cy="12" r="1.4"/><circle cx="18.5" cy="12" r="1.4"/>',
 "back": '<path d="m14.5 6-6 6 6 6"/>',
 "mail": '<rect x="3.5" y="5.5" width="17" height="13" rx="2"/><path d="m4 7 8 5.5L20 7"/>',
 "note": '<path d="M5.5 4.5h13v11l-4 4h-9z"/><path d="M18.5 15.5h-4v4"/>',
 "shield": '<path d="M12 3.5 5 6.2v5c0 4 2.9 7.5 7 9.3 4.1-1.8 7-5.3 7-9.3v-5z"/><path d="m9.2 11.8 2 2 3.6-3.8"/>',
 "hub": '<circle cx="12" cy="12" r="2.6"/><circle cx="12" cy="4.6" r="2.1"/><circle cx="19" cy="16" r="2.1"/><circle cx="5" cy="16" r="2.1"/><path d="M12 7v2.4M13.9 13.6l3 1.2M10.1 13.6l-3 1.2"/>',
 "store": '<path d="M4 9.5V19h16V9.5"/><path d="M3.2 9.5 5 4.5h14l1.8 5a2.6 2.6 0 0 1-4.6 1.7 2.6 2.6 0 0 1-4.2 0 2.6 2.6 0 0 1-4.2 0A2.6 2.6 0 0 1 3.2 9.5z"/>',
 "calendar": '<rect x="3.5" y="5" width="17" height="15" rx="2.4"/><path d="M3.5 9.6h17M8 3.4v3.2M16 3.4v3.2"/>',
 "walk": '<circle cx="13" cy="4.6" r="1.9"/><path d="m10 20 2.2-5.2-2-2.2.8-4.1 3 1.6 2.4 2.1"/><path d="m8.4 12.6 1.6-3.1M14.4 14.8 16 20"/>',
 "doc": '<path d="M6 3.5h7.5L18.5 8v12.5H6z"/><path d="M13.2 3.6V8.3h4.9M9 13h6M9 16.5h4.5"/>',
 "person": '<circle cx="12" cy="8" r="3.4"/><path d="M5.5 20c0-3.6 2.9-6.2 6.5-6.2s6.5 2.6 6.5 6.2"/>',
}

def ic(name, size=20, sw=1.7, color="currentColor"):
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" '
            f'stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round">{ICONS[name]}</svg>')

def head(title):
    return f'''<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Sarabun:wght@400;500;600;700;800&family=IBM+Plex+Mono:wght@400;500&display=swap">
  <style>
    body {{ margin: 0; font-family: {BODY}; color: {T['ink']}; -webkit-font-smoothing: antialiased; }}
    a {{ color: {T['accentLight']}; text-decoration: none; }}
    a:hover {{ color: #c0b9fb; }}
  </style>
</helmet>'''

TAIL = '''</x-dc>
</body>
</html>
'''

# เมนูจริงของ Agency Care (ตัดมาเท่าที่พอในความสูง 900px) + กลุ่มใหม่ของโมดูลแชท
NAV_TOP = [("chart","Dashboard"),("store","Agency"),("person","New Agency Acquisition"),
           ("calendar","Assignments"),("walk","Site Visit")]
NAV_CHAT = [("inbox","Chat Inbox","3"),("users","Chat Contacts",None),("bolt","Chat Automations",None),
            ("megaphone","Chat Broadcast",None),("chart","Chat Insight",None)]
NAV_BOTTOM = [("doc","Documents"),("settings","Settings")]

def _nav_item(icon_name, text, active=False, badge=None):
    col = "#fff" if active else T['muted']
    icol = T['accentLight'] if active else "inherit"
    bg = NAV_ACTIVE if active else "transparent"
    weight = 700 if active else 500
    badge_html = (f'<span style="min-width:20px;height:20px;border-radius:9px;background:{T["danger"]};color:#1a1020;'
                  f'font-size:11px;font-weight:700;display:flex;align-items:center;justify-content:center;padding:0 6px">{badge}</span>') if badge else ""
    return (f'<div style="display:flex;align-items:center;gap:0;height:38px;padding:0 10px;margin-bottom:4px;'
            f'border-radius:12px;background:{bg};color:{col}">'
            f'<span style="width:36px;flex:none;display:flex;align-items:center;color:{icol}">{ic(icon_name,19)}</span>'
            f'<span style="flex:1;font-size:14px;font-weight:{weight};white-space:nowrap;overflow:hidden;text-overflow:ellipsis">{text}</span>'
            f'{badge_html}</div>')

def _nav_label(text):
    return (f'<div style="padding:12px 12px 6px;font-size:10.5px;font-weight:700;letter-spacing:.14em;'
            f'color:rgba(155,153,184,0.7)">{text}</div>')

def rail(active):
    """Sidebar 252px ตาม Layout.tsx — active คือคีย์ไอคอนของเมนูแชท"""
    top = "".join(_nav_item(i, t) for i, t in NAV_TOP)
    chat = "".join(_nav_item(i, t, active=(i == active), badge=b) for i, t, b in NAV_CHAT)
    bottom = "".join(_nav_item(i, t, active=(i == "settings" and active == "settings")) for i, t in NAV_BOTTOM)
    return (
      f'<div style="width:{DRAWER}px;flex:none;background:{T["sidebar"]};border-right:1px solid {T["cardBorder"]};'
      f'display:flex;flex-direction:column;padding:12px;overflow:hidden">'
      f'<div style="display:flex;align-items:center;gap:12px;padding:12px 8px;margin-bottom:8px">'
      f'<span style="width:42px;height:42px;flex:none;border-radius:50%;background:linear-gradient(135deg,#8b7ff5,#5b4fd6);'
      f'box-shadow:0 10px 24px -8px rgba(124,111,240,0.7);display:flex;align-items:center;justify-content:center">{ic("hub",23,1.8,"#fff")}</span>'
      f'<span style="display:flex;flex-direction:column;line-height:1">'
      f'<span style="font-weight:800;font-size:18px;line-height:1">AGENCY</span>'
      f'<span style="color:{T["accentLight"]};font-weight:800;font-size:12px;letter-spacing:3px">CARE</span></span></div>'
      f'<div style="flex:1;overflow:hidden;padding:0 4px">{top}{_nav_label("CHAT")}{chat}'
      f'<div style="height:1px;background:{T["line"]};margin:10px 6px"></div>{bottom}</div>'
      f'<div style="display:flex;align-items:center;gap:12px;padding:10px;border-radius:24px;background:rgba(255,255,255,0.04)">'
      f'<span style="width:38px;height:38px;flex:none;border-radius:50%;background:{T["accentDark"]};color:#fff;'
      f'display:flex;align-items:center;justify-content:center;font-size:14px;font-weight:700">PL</span>'
      f'<span style="flex:1;display:flex;flex-direction:column;min-width:0">'
      f'<span style="font-size:13.5px;font-weight:700">Ploy Srisai</span>'
      f'<span style="font-size:11.5px;color:{T["muted"]}">Agency Care</span></span>'
      f'<span style="color:{T["muted"]}">{ic("dots",17)}</span></div>'
      f'</div>')

def topbar(title, right="", subtitle=""):
    sub = f'<span style="font-size:13px;color:{T["muted"]}">{subtitle}</span>' if subtitle else ""
    return (f'<div style="flex:none;display:flex;align-items:center;gap:12px;padding:24px 28px 12px">'
            f'<div style="display:flex;flex-direction:column;gap:2px;min-width:0">'
            f'<span style="font-size:22px;font-weight:800;letter-spacing:-0.3px;line-height:1.15">{title}</span>{sub}</div>'
            f'<div style="flex:1"></div>{right}</div>')

def search_box(placeholder="ค้นหา", width=240):
    return (f'<div style="display:flex;align-items:center;gap:8px;width:{width}px;height:38px;padding:0 12px;'
            f'border:1px solid rgba(255,255,255,0.14);border-radius:12px;background:rgba(255,255,255,0.03);color:{T["muted"]}">'
            f'{ic("search",16)}<span style="font-size:13px">{placeholder}</span></div>')

def btn(label, kind="ghost", icon=None, size=36):
    if kind == "primary":
        style = f'background:{BTN_GRAD};color:#fff;box-shadow:{BTN_SHADOW};border:none;font-weight:600'
    elif kind == "danger":
        style = f'background:transparent;color:{T["danger"]};border:1px solid rgba(248,113,113,0.4);font-weight:600'
    else:
        style = f'background:transparent;color:{T["muted"]};border:1px solid rgba(255,255,255,0.08);font-weight:600'
    inner = (ic(icon,16) if icon else "") + f'<span>{label}</span>'
    return (f'<div style="display:flex;align-items:center;gap:7px;height:{size}px;padding:0 14px;border-radius:12px;'
            f'font-size:13px;white-space:nowrap;{style}">{inner}</div>')

def icon_btn(icon_name, text=None):
    t = f'<span style="font-size:11.5px;font-weight:700">{text}</span>' if text else ""
    return (f'<div style="display:flex;align-items:center;gap:5px;height:36px;padding:0 12px;border-radius:40px;'
            f'border:1px solid rgba(255,255,255,0.08);color:{T["muted"]}">{ic(icon_name,17)}{t}</div>')

def pill(text, tone="muted"):
    tones = {
      "muted": ("rgba(255,255,255,0.06)", T['muted'], "rgba(255,255,255,0.10)"),
      "accent": ("rgba(124,111,240,0.18)", T['accentLight'], "rgba(124,111,240,0.35)"),
      "warn": ("rgba(251,191,36,0.14)", T['warn'], "rgba(251,191,36,0.32)"),
      "danger": ("rgba(248,113,113,0.14)", T['danger'], "rgba(248,113,113,0.32)"),
      "ok": ("rgba(52,211,153,0.14)", T['ok'], "rgba(52,211,153,0.32)"),
    }
    bgc, fg, bd = tones[tone]
    return (f'<span style="display:inline-flex;align-items:center;height:22px;padding:0 9px;border-radius:9px;'
            f'background:{bgc};color:{fg};border:1px solid {bd};font-size:11.5px;font-weight:600;white-space:nowrap">{text}</span>')

def dot(color, size=8):
    return f'<span style="width:{size}px;height:{size}px;border-radius:50%;background:{color};flex:none"></span>'

CHAN = {"LINE":"#06C755","Facebook":"#1877F2","WhatsApp":"#25D366","Instagram":"#C13584"}

def chan(name):
    return (f'<span style="display:inline-flex;align-items:center;gap:5px;font-size:11.5px;color:{T["muted"]}">'
            f'{dot(CHAN[name])}{name}</span>')

def avatar(initials, size=36, bg=None, fg=None):
    return (f'<div style="width:{size}px;height:{size}px;flex:none;border-radius:50%;background:{bg or T["accentDark"]};'
            f'color:{fg or "#fff"};display:flex;align-items:center;justify-content:center;'
            f'font-weight:700;font-size:{max(11,int(size*0.34))}px">{initials}</div>')

def label(text):
    return (f'<div style="font-size:12px;font-weight:700;letter-spacing:.04em;text-transform:uppercase;color:{T["muted"]}">{text}</div>')

def card(inner, pad=18, extra=""):
    return (f'<div style="background:{T["surface"]};border:1px solid {T["cardBorder"]};border-radius:16px;'
            f'padding:{pad}px;{extra}">{inner}</div>')

def select(value, width=150):
    return (f'<div style="display:flex;align-items:center;justify-content:space-between;gap:8px;width:{width}px;'
            f'height:38px;padding:0 12px;border:1px solid rgba(255,255,255,0.14);border-radius:12px;'
            f'background:rgba(255,255,255,0.03);font-size:13px">{value}<span style="color:{T["muted"]}">{ic("chevdown",14)}</span></div>')

def field(lbl, value, width=None, mono=False, placeholder=False):
    w = f'width:{width}px;' if width else 'flex:1;'
    fam = f'font-family:{MONO};' if mono else ''
    col = T['muted'] if placeholder else T['ink']
    return (f'<div style="display:flex;flex-direction:column;gap:6px;{w}">'
            f'<span style="font-size:12px;color:{T["muted"]}">{lbl}</span>'
            f'<div style="height:40px;display:flex;align-items:center;padding:0 12px;border:1px solid rgba(255,255,255,0.14);'
            f'border-radius:12px;background:rgba(255,255,255,0.03);font-size:13.5px;{fam}color:{col}">{value}</div></div>')

def page(inner, w=1440, h=900):
    return (f'<div style="width:{w}px;height:{h}px;display:flex;background:{PAGE_BG};background-repeat:no-repeat;'
            f'font-family:{BODY};color:{T["ink"]};overflow:hidden">{inner}</div>')

def write(name, body):
    with io.open(name, "w", encoding="utf-8") as f:
        f.write(head(name[:-8]) + "\n" + body + "\n" + TAIL)
    print("wrote", name, os.path.getsize(name), "bytes")
