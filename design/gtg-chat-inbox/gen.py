# -*- coding: utf-8 -*-
"""โทเคนและชิ้นส่วน UI — ลอกค่าจริงจาก agency-care/web/src/theme/ThemeContext.tsx (โหมดมืด)"""
import io, os

T = dict(
    bg="#0F172A",                    # ต้นทางของ gradient พื้นหลัง
    sidebar="#111827",               # MuiDrawer paper
    topbar="#1F2937",                # MuiAppBar
    surface="#111827",               # การ์ด
    surfaceSolid="#111827",
    line="#374151",                  # palette.divider
    cardBorder="#374151",
    ink="#F1F5F9",                   # text.primary
    muted="#CBD5E1",                 # text.secondary
    dim="#94A3B8",
    accent="#3B82F6",                # primary.main
    accentLight="#60A5FA",           # primary.light
    accentDark="#1E40AF",            # primary.dark
    accentInk="#FFFFFF",
    card="rgba(59,130,246,0.16)",    # ทินต์สีหลัก (ชิป/เมนูที่เลือก)
    inb="rgba(255,255,255,0.04)",
    warn="#FBBF24",                  # warning.main
    danger="#EF4444",                # error.main
    ok="#22C55E",                    # success.main
    info="#38BDF8",
)
PAGE_BG = "linear-gradient(135deg, #0F172A 0%, #111827 60%, #1F2937 100%)"
BTN_GRAD = T["accent"]                       # ปุ่ม contained เป็นสีทึบ ไม่มี gradient
BTN_SHADOW = "none"
NAV_ACTIVE = "rgba(59,130,246,0.16)"
R_CARD = 20          # MuiPaper rounded
R_BTN = 999          # MuiButton — ปุ่มทรงแคปซูล
R_INPUT = 12         # MuiOutlinedInput
R_NAV = 14           # MuiListItemButton

BODY = "'SF Pro Display',-apple-system,'Segoe UI','IBM Plex Sans Thai',Roboto,Helvetica,Arial,sans-serif"
DISPLAY = BODY
MONO = "'IBM Plex Mono',ui-monospace,monospace"
DRAWER = 264

ICONS = {
 "home": '<path d="M4 11.2 12 4.5l8 6.7"/><path d="M6.2 10v9.5h11.6V10"/><path d="M10 19.5v-5.2h4v5.2"/>',
 "grid": '<rect x="4" y="4" width="7" height="7" rx="1.6"/><rect x="13" y="4" width="7" height="7" rx="1.6"/><rect x="4" y="13" width="7" height="7" rx="1.6"/><rect x="13" y="13" width="7" height="7" rx="1.6"/>',
 "bell": '<path d="M6.5 10a5.5 5.5 0 0 1 11 0c0 4 1.4 5.4 1.4 5.4H5.1S6.5 14 6.5 10z"/><path d="M10.2 18.6a2 2 0 0 0 3.6 0"/>',
 "moon": '<path d="M20 13.4A8 8 0 1 1 10.6 4a6.6 6.6 0 0 0 9.4 9.4z"/>',
 "swap": '<path d="M4 8.5h13l-3.2-3.2"/><path d="M20 15.5H7l3.2 3.2"/>',
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
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Thai:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap">
  <style>
    body {{ margin: 0; font-family: {BODY}; color: {T['ink']}; -webkit-font-smoothing: antialiased; }}
    a {{ color: {T['accentLight']}; text-decoration: none; }}
    a:hover {{ color: #93C5FD; }}
  </style>
</helmet>'''

TAIL = '''</x-dc>
</body>
</html>
'''

# เมนูจริงของ Agency Care แบ่งเป็นกลุ่มตามหน้าเว็บ + กลุ่มใหม่ของโมดูลแชท
NAV_GROUPS = [
    ("OVERVIEW", [("home", "Home", None), ("chart", "Dashboard", None),
                  ("doc", "Company News", None), ("tag", "Promotion", None)]),
    ("CHAT", [("inbox", "Chat Inbox", "3"), ("users", "Chat Contacts", None),
              ("bolt", "Chat Automations", None), ("megaphone", "Chat Broadcast", None),
              ("chart", "Chat Insight", None)]),
    ("AGENCIES", [("store", "Agency List", None), ("grid", "Agency Matrix", None)]),
]

def _nav_item(icon_name, text, active=False, badge=None):
    col = T['accentLight'] if active else T['muted']
    bg = NAV_ACTIVE if active else "transparent"
    weight = 700 if active else 500
    badge_html = (f'<span style="min-width:22px;height:20px;border-radius:999px;background:{T["danger"]};color:#fff;'
                  f'font-size:11px;font-weight:700;display:flex;align-items:center;justify-content:center;padding:0 6px">{badge}</span>') if badge else ""
    return (f'<div style="display:flex;align-items:center;gap:0;height:42px;padding:0 12px;margin-bottom:2px;'
            f'border-radius:{R_NAV}px;background:{bg};color:{col}">'
            f'<span style="width:34px;flex:none;display:flex;align-items:center">{ic(icon_name,20)}</span>'
            f'<span style="flex:1;font-size:14.5px;font-weight:{weight};white-space:nowrap;overflow:hidden;text-overflow:ellipsis">{text}</span>'
            f'{badge_html}</div>')

def _group_label(text):
    return (f'<div style="display:flex;align-items:center;gap:8px;padding:14px 12px 6px;font-size:11px;font-weight:700;'
            f'letter-spacing:.12em;color:{T["dim"]}">{text}<span style="flex:1"></span>{ic("chevdown",15)}</div>')

def rail(active):
    """Sidebar ตาม Layout จริง: การ์ดโลโก้ด้านบน เมนูแบ่งกลุ่ม การ์ดผู้ใช้ด้านล่าง"""
    groups = "".join(
        _group_label(label) + "".join(_nav_item(i, t, active=(i == active), badge=b) for i, t, b in items)
        for label, items in NAV_GROUPS)
    return (
      f'<div style="width:{DRAWER}px;flex:none;background:{T["sidebar"]};border-right:1px solid {T["line"]};'
      f'display:flex;flex-direction:column;padding:16px 12px;overflow:hidden">'
      # การ์ดโลโก้
      f'<div style="background:#080C16;border:1px solid rgba(255,255,255,0.06);border-radius:{R_CARD}px;'
      f'padding:16px;display:flex;flex-direction:column;align-items:center;gap:6px;margin-bottom:10px">'
      f'<svg width="56" height="56" viewBox="0 0 56 56" fill="none">'
      f'<defs><linearGradient id="acg" x1="0" y1="0" x2="1" y2="1">'
      f'<stop offset="0%" stop-color="#22D3EE"/><stop offset="55%" stop-color="#3B82F6"/><stop offset="100%" stop-color="#34D399"/>'
      f'</linearGradient></defs>'
      f'<path d="M8 44 24 10l16 34" stroke="url(#acg)" stroke-width="5" stroke-linecap="round" stroke-linejoin="round" fill="none"/>'
      f'<path d="M15 33h18" stroke="url(#acg)" stroke-width="5" stroke-linecap="round"/>'
      f'<path d="M50 20a15 15 0 1 0 0 18" stroke="url(#acg)" stroke-width="5" stroke-linecap="round" fill="none"/>'
      f'<path d="m40 30 4 4 8-9" stroke="#34D399" stroke-width="4" stroke-linecap="round" stroke-linejoin="round" fill="none"/></svg>'
      f'<span style="font-size:16px;font-weight:700;letter-spacing:.01em">Agency Care</span>'
      f'<span style="font-size:8.5px;letter-spacing:.24em;color:{T["dim"]}">CONNECT · VISIT · GROW</span></div>'
      f'<div style="flex:1;overflow:hidden">{groups}</div>'
      # การ์ดผู้ใช้
      f'<div style="display:flex;align-items:center;gap:12px;padding:10px 12px;border-radius:16px;background:rgba(255,255,255,0.04)">'
      f'<span style="width:38px;height:38px;flex:none;border-radius:50%;background:{T["accent"]};color:#fff;'
      f'display:flex;align-items:center;justify-content:center;font-size:14px;font-weight:700">PL</span>'
      f'<span style="flex:1;display:flex;flex-direction:column;min-width:0">'
      f'<span style="font-size:14px;font-weight:700">Ploy Srisai</span>'
      f'<span style="font-size:12px;color:{T["dim"]}">Agency Care</span></span></div>'
      f'<div style="display:flex;align-items:center;gap:10px;padding:12px 14px 2px;font-size:12px;'
      f'letter-spacing:.14em;color:{T["dim"]};font-weight:700">LOGOUT</div>'
      f'</div>')

def topbar(title, right="", subtitle=""):
    """แถบบนของแอป (คำทักทาย + เครื่องมือ) แล้วต่อด้วยหัวข้อของหน้าในเนื้อหา"""
    sub = f'<span style="font-size:13px;color:{T["dim"]}">{subtitle}</span>' if subtitle else ""
    tool = lambda inner, extra="": (
        f'<span style="width:36px;height:36px;border-radius:50%;border:1px solid {T["line"]};color:{T["muted"]};'
        f'display:flex;align-items:center;justify-content:center;position:relative;{extra}">{inner}</span>')
    bell = (f'<span style="position:relative;display:flex">{ic("bell",18)}'
            f'<span style="position:absolute;top:-7px;right:-9px;min-width:18px;height:18px;border-radius:999px;'
            f'background:{T["danger"]};color:#fff;font-size:10px;font-weight:700;display:flex;align-items:center;'
            f'justify-content:center;padding:0 4px">86</span></span>')
    return (
      # แถบแอป
      f'<div style="flex:none;height:64px;display:flex;align-items:center;gap:10px;padding:0 24px;'
      f'background:{T["topbar"]};border-bottom:1px solid {T["line"]}">'
      f'<div style="display:flex;flex-direction:column;gap:1px">'
      f'<span style="font-size:19px;font-weight:700;letter-spacing:-0.01em">Good afternoon, Ploy 👋</span>'
      f'<span style="font-size:12.5px;color:{T["dim"]}">Tuesday, September 15</span></div>'
      f'<div style="flex:1"></div>'
      f'<span style="display:flex;align-items:center;gap:7px;height:34px;padding:0 14px;border-radius:999px;'
      f'border:1px solid {T["line"]};color:{T["muted"]};font-size:12.5px;font-weight:600">{ic("swap",15)}Manager</span>'
      f'<span style="display:flex;align-items:center;gap:6px;height:34px;padding:0 12px;border-radius:999px;'
      f'border:1px solid {T["line"]};color:{T["muted"]};font-size:12.5px;font-weight:600">EN English{ic("chevdown",14)}</span>'
      f'{tool(ic("search",18))}{tool(ic("moon",18))}{tool(bell)}'
      f'<span style="width:36px;height:36px;border-radius:50%;background:{T["accent"]};color:#fff;display:flex;'
      f'align-items:center;justify-content:center;font-size:13px;font-weight:700">PL</span>'
      f'</div>'
      # หัวข้อของหน้า
      f'<div style="flex:none;display:flex;align-items:center;gap:12px;padding:20px 24px 12px">'
      f'<div style="display:flex;flex-direction:column;gap:2px;min-width:0">'
      f'<span style="font-size:21px;font-weight:700;letter-spacing:-0.01em;line-height:1.2">{title}</span>{sub}</div>'
      f'<div style="flex:1"></div>{right}</div>')

def search_box(placeholder="ค้นหา", width=240):
    return (f'<div style="display:flex;align-items:center;gap:8px;width:{width}px;height:38px;padding:0 13px;'
            f'border:1px solid {T["line"]};border-radius:{R_INPUT}px;background:rgba(255,255,255,0.03);color:{T["dim"]}">'
            f'{ic("search",16)}<span style="font-size:13px">{placeholder}</span></div>')

def btn(label, kind="ghost", icon=None, size=38):
    if kind == "primary":
        style = f'background:{T["accent"]};color:#fff;border:none;font-weight:600'
    elif kind == "danger":
        style = f'background:transparent;color:{T["danger"]};border:1px solid rgba(239,68,68,0.45);font-weight:600'
    else:
        style = f'background:transparent;color:{T["muted"]};border:1px solid {T["line"]};font-weight:600'
    inner = (ic(icon,16) if icon else "") + f'<span>{label}</span>'
    return (f'<div style="display:flex;align-items:center;gap:8px;height:{size}px;padding:0 18px;border-radius:{R_BTN}px;'
            f'font-size:13.5px;white-space:nowrap;{style}">{inner}</div>')

def icon_btn(icon_name, text=None):
    t = f'<span style="font-size:12px;font-weight:700">{text}</span>' if text else ""
    return (f'<div style="display:flex;align-items:center;gap:6px;height:36px;padding:0 13px;border-radius:999px;'
            f'border:1px solid {T["line"]};color:{T["muted"]}">{ic(icon_name,17)}{t}</div>')

def pill(text, tone="muted"):
    tones = {
      "muted": ("rgba(255,255,255,0.06)", T['muted'], "rgba(255,255,255,0.12)"),
      "accent": ("rgba(59,130,246,0.18)", T['accentLight'], "rgba(59,130,246,0.38)"),
      "warn": ("rgba(251,191,36,0.16)", T['warn'], "rgba(251,191,36,0.35)"),
      "danger": ("rgba(239,68,68,0.16)", T['danger'], "rgba(239,68,68,0.35)"),
      "ok": ("rgba(34,197,94,0.16)", T['ok'], "rgba(34,197,94,0.35)"),
    }
    bgc, fg, bd = tones[tone]
    return (f'<span style="display:inline-flex;align-items:center;height:23px;padding:0 10px;border-radius:999px;'
            f'background:{bgc};color:{fg};border:1px solid {bd};font-size:11.5px;font-weight:600;white-space:nowrap">{text}</span>')

def dot(color, size=8):
    return f'<span style="width:{size}px;height:{size}px;border-radius:50%;background:{color};flex:none"></span>'

CHAN = {"LINE":"#06C755","Facebook":"#1877F2","WhatsApp":"#25D366","Instagram":"#C13584"}

def chan(name):
    return (f'<span style="display:inline-flex;align-items:center;gap:5px;font-size:11.5px;color:{T["dim"]}">'
            f'{dot(CHAN[name])}{name}</span>')

def avatar(initials, size=36, bg=None, fg=None):
    return (f'<div style="width:{size}px;height:{size}px;flex:none;border-radius:50%;background:{bg or T["accent"]};'
            f'color:{fg or "#fff"};display:flex;align-items:center;justify-content:center;'
            f'font-weight:700;font-size:{max(11,int(size*0.34))}px">{initials}</div>')

def label(text):
    return (f'<div style="font-size:12px;font-weight:700;letter-spacing:.04em;text-transform:uppercase;color:{T["dim"]}">{text}</div>')

def card(inner, pad=18, extra=""):
    return (f'<div style="background:{T["surface"]};border:1px solid {T["cardBorder"]};border-radius:{R_CARD}px;'
            f'padding:{pad}px;{extra}">{inner}</div>')

def select(value, width=150):
    return (f'<div style="display:flex;align-items:center;justify-content:space-between;gap:8px;width:{width}px;'
            f'height:38px;padding:0 13px;border:1px solid {T["line"]};border-radius:{R_INPUT}px;'
            f'background:rgba(255,255,255,0.03);font-size:13px">{value}<span style="color:{T["dim"]}">{ic("chevdown",14)}</span></div>')

def field(lbl, value, width=None, mono=False, placeholder=False):
    w = f'width:{width}px;' if width else 'flex:1;'
    fam = f'font-family:{MONO};' if mono else ''
    col = T['dim'] if placeholder else T['ink']
    return (f'<div style="display:flex;flex-direction:column;gap:6px;{w}">'
            f'<span style="font-size:12px;color:{T["dim"]}">{lbl}</span>'
            f'<div style="height:42px;display:flex;align-items:center;padding:0 13px;border:1px solid {T["line"]};'
            f'border-radius:{R_INPUT}px;background:rgba(255,255,255,0.03);font-size:13.5px;{fam}color:{col}">{value}</div></div>')

def page(inner, w=1440, h=900):
    return (f'<div style="width:{w}px;height:{h}px;display:flex;background:{PAGE_BG};background-repeat:no-repeat;'
            f'font-family:{BODY};color:{T["ink"]};overflow:hidden">{inner}</div>')

def write(name, body):
    with io.open(name, "w", encoding="utf-8") as f:
        f.write(head(name[:-8]) + "\n" + body + "\n" + TAIL)
    print("wrote", name, os.path.getsize(name), "bytes")
