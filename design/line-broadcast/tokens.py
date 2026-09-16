# ค่าทั้งหมดดึงตรงจาก web/src/theme/ThemeContext.tsx (โหมด dark) ของ agency-care
# branch feat/all-appointments-clean-on-118a2e2 = revision agency-care-00886-nus

BG        = "linear-gradient(135deg,#0F172A 0%,#111827 60%,#1F2937 100%)"
PAPER     = "#111827"
SURFACE   = "#1F2937"
DIVIDER   = "#374151"
TXT       = "#F1F5F9"
TXT2      = "#CBD5E1"
TXT3      = "#6B7280"
PRIMARY   = "#3B82F6"
PRIMARY_L = "#60A5FA"
SECOND    = "#A78BFA"
SUCCESS   = "#22C55E"
WARNING   = "#FBBF24"
ERROR     = "#EF4444"
INFO      = "#38BDF8"
FONT      = '"SF Pro Display",-apple-system,"Segoe UI","Roboto","Helvetica","Arial",sans-serif'

CSS = f"""
  *{{box-sizing:border-box}}
  body{{margin:0;font-family:{FONT};background:{BG};color:{TXT};
       -webkit-font-smoothing:antialiased;line-height:1.5}}
  a{{color:{PRIMARY_L};text-decoration:none}} a:hover{{color:{PRIMARY}}}
  .card{{background:{PAPER};border:1px solid {DIVIDER};border-radius:20px}}
  .pad{{padding:20px 24px}}
  .row{{display:flex;align-items:center}}
  .col{{display:flex;flex-direction:column}}
  .grow{{flex-grow:1}}
  .h5{{font-size:24px;font-weight:700;letter-spacing:-0.01em;margin:0}}
  .h6{{font-size:20px;font-weight:600;margin:0}}
  .sec{{font-size:12px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:{TXT2};margin:0}}
  .b2{{font-size:14px;line-height:1.43;margin:0}}
  .cap{{font-size:12px;line-height:1.66;color:{TXT2};margin:0}}
  .mut{{color:{TXT3}}}
  .btn{{border-radius:999px;border:0;padding:7px 18px;font-family:inherit;font-size:14px;
        font-weight:600;cursor:pointer;background:{PRIMARY};color:#fff}}
  .btn.out{{background:transparent;border:1px solid {DIVIDER};color:{TXT2}}}
  .btn.sm{{padding:5px 14px;font-size:13px}}
  .chip{{display:inline-flex;align-items:center;gap:5px;height:24px;padding:0 10px;
         border-radius:999px;font-size:12px;font-weight:600;line-height:1}}
  .fld{{background:{SURFACE};border:1px solid {DIVIDER};border-radius:12px;
        padding:9px 12px;font-size:14px;color:{TXT}}}
  .lbl{{font-size:12px;font-weight:600;color:{TXT2};margin:0 0 6px}}
  input.fld,select.fld,textarea.fld{{font-family:inherit;width:100%;outline:none}}
  table{{width:100%;border-collapse:collapse}}
  th{{text-align:left;font-size:12px;font-weight:700;color:{TXT2};padding:10px 12px;
      border-bottom:1px solid {DIVIDER};letter-spacing:.02em}}
  td{{font-size:14px;padding:12px;border-bottom:1px solid {DIVIDER};vertical-align:middle}}
"""

def status_chip(kind):
    """ป้ายสถานะ 5 แบบตามที่กำหนด — สีมาจาก palette ของแอป"""
    m = {
        "NEW":            (INFO,    "rgba(56,189,248,.14)"),
        "IN PROGRESS":    (PRIMARY_L, "rgba(59,130,246,.16)"),
        "WAITING AGENCY": (SECOND,  "rgba(167,139,250,.16)"),
        "NEED ATTENTION": (WARNING, "rgba(251,191,36,.15)"),
        "COMPLETED":      (SUCCESS, "rgba(34,197,94,.15)"),
    }
    c, bg = m[kind]
    return f'<span class="chip" style="color:{c};background:{bg}">{kind}</span>'

def bar(pct, color=None):
    color = color or PRIMARY
    return (f'<div style="height:8px;border-radius:4px;background:{SURFACE};overflow:hidden">'
            f'<div style="width:{pct}%;height:100%;border-radius:4px;background:{color}"></div></div>')

def icon(d, size=18, color=None, fill="none", extra=""):
    color = color or TXT2
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="{fill}" '
            f'stroke="{color}" stroke-width="1.8" stroke-linecap="round" '
            f'stroke-linejoin="round" {extra}>{d}</svg>')

I_CHECK  = '<polyline points="20 6 9 17 4 12"></polyline>'
I_CIRCLE = '<circle cx="12" cy="12" r="9"></circle>'
I_WARN   = '<path d="M12 3 2 20h20L12 3z"></path><line x1="12" y1="10" x2="12" y2="14"></line><circle cx="12" cy="17.5" r=".6" fill="currentColor"></circle>'
I_EXT    = '<path d="M15 3h6v6"></path><path d="M10 14 21 3"></path><path d="M18 13v7a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h7"></path>'
I_SEARCH = '<circle cx="11" cy="11" r="7"></circle><line x1="21" y1="21" x2="16.7" y2="16.7"></line>'
I_CHEV   = '<polyline points="6 9 12 15 18 9"></polyline>'
I_UP     = '<path d="M12 16V4"></path><path d="m7 9 5-5 5 5"></path><path d="M4 16v3a1 1 0 0 0 1 1h14a1 1 0 0 0 1-1v-3"></path>'
I_PLUS   = '<line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line>'
I_CLOCK  = '<circle cx="12" cy="12" r="9"></circle><polyline points="12 7 12 12 15 14"></polyline>'

def page(inner, w, h):
    return f"""<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
  <style>{CSS}</style>
</helmet>
<div style="width:{w}px;min-height:{h}px;background:{BG};padding:0">
{inner}
</div>
</x-dc>
</body>
</html>
"""
