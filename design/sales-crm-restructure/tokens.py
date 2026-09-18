# Every value is taken straight from web/src/theme/ThemeContext.tsx (dark mode) in agency-care
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
    """The five status pills — colours come from the app palette."""
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

# Workflow status colours — always paired with a label, never colour alone
FLOW = {
  "Draft":            (TXT3,    "rgba(107,114,128,.18)"),
  "Upcoming":         (INFO,    "rgba(56,189,248,.14)"),
  "Due":              (WARNING, "rgba(251,191,36,.15)"),
  "Pending Approval": (WARNING, "rgba(251,191,36,.15)"),
  "Submitted":        (PRIMARY_L,"rgba(59,130,246,.16)"),
  "Under Review":     (SECOND,  "rgba(167,139,250,.16)"),
  "Approved":         (SUCCESS, "rgba(34,197,94,.14)"),
  "Ordered":          (PRIMARY_L,"rgba(59,130,246,.16)"),
  "Received":         (SECOND,  "rgba(167,139,250,.16)"),
  "Completed":        (SUCCESS, "rgba(34,197,94,.14)"),
  "Overdue":          (ERROR,   "rgba(239,68,68,.15)"),
  "Rejected":         (ERROR,   "rgba(239,68,68,.15)"),
  "Available":        (SUCCESS, "rgba(34,197,94,.14)"),
  "Reserved":         (WARNING, "rgba(251,191,36,.15)"),
  "Booked":           (SECOND,  "rgba(167,139,250,.16)"),
  "Sold":             (TXT3,    "rgba(107,114,128,.18)"),
  "PASS":             (SUCCESS, "rgba(34,197,94,.14)"),
  "FAIL":             (ERROR,   "rgba(239,68,68,.15)"),
  "Internal":         (ERROR,   "rgba(239,68,68,.15)"),
  "External":         (SUCCESS, "rgba(34,197,94,.14)"),
}

def flow_chip(name):
    c, bg = FLOW[name]
    return f'<span class="chip" style="color:{c};background:{bg}">{name}</span>'

def flow_line(stages, active=None, reject=None):
    """A status row — stages not yet reached are dimmed."""
    out = []
    idx = stages.index(active) if active in stages else -1
    for i, s in enumerate(stages):
        if idx >= 0 and i > idx:
            body = f'<span class="chip" style="border:1px solid {DIVIDER};color:{TXT3}">{s}</span>'
        else:
            body = flow_chip(s)
        arrow = "" if i == len(stages) - 1 else f'<span style="color:{TXT3}">→</span>'
        out.append(f'<div class="row" style="gap:9px">{body}{arrow}</div>')
    tail = ""
    if reject:
        tail = (f'<div class="row" style="gap:9px;padding-left:14px;border-left:1px solid {DIVIDER}">'
                f'<span style="color:{TXT3}">↘</span>{flow_chip(reject)}</div>')
    return f'<div class="row" style="gap:9px;flex-wrap:wrap;align-items:center">{"".join(out)}{tail}</div>'


# -- Extra statuses for the Sales CRM Restructure set --------------------
FLOW.update({
  "New":                (INFO,      "rgba(56,189,248,.14)"),
  "Contacted":          (PRIMARY_L, "rgba(59,130,246,.16)"),
  "Visit":              (SECOND,    "rgba(167,139,250,.16)"),
  "Holding":            (WARNING,   "rgba(251,191,36,.15)"),
  "Reservation":        (WARNING,   "rgba(251,191,36,.15)"),
  "Holding / Reservation": (WARNING,"rgba(251,191,36,.15)"),
  "Sold Deal":          (SUCCESS,   "rgba(34,197,94,.14)"),
  "Lost":               (ERROR,     "rgba(239,68,68,.15)"),
  "Missed":             (TXT3,      "rgba(107,114,128,.18)"),
  # Deal lifecycle
  "Confirmed":          (PRIMARY_L, "rgba(59,130,246,.16)"),
  "Contracted":         (SECOND,    "rgba(167,139,250,.16)"),
  "Payment In Progress":(INFO,      "rgba(56,189,248,.14)"),
  "Transfer Pending":   (WARNING,   "rgba(251,191,36,.15)"),
  "Active":             (SUCCESS,   "rgba(34,197,94,.14)"),
  "Cancelled":          (ERROR,     "rgba(239,68,68,.15)"),
  "Refunded":           (TXT3,      "rgba(107,114,128,.18)"),
  # Payment
  "Paid":               (SUCCESS,   "rgba(34,197,94,.14)"),
  "Partial":            (WARNING,   "rgba(251,191,36,.15)"),
  "Partially Paid":     (WARNING,   "rgba(251,191,36,.15)"),
  "Pending":            (TXT3,      "rgba(107,114,128,.18)"),
  "Unpaid":             (TXT3,      "rgba(107,114,128,.18)"),
  "Future":             (TXT3,      "rgba(107,114,128,.18)"),
  # Commission
  "Ready for Payment":  (PRIMARY_L, "rgba(59,130,246,.16)"),
  "On Hold":            (TXT3,      "rgba(107,114,128,.18)"),
  "Calculated":         (INFO,      "rgba(56,189,248,.14)"),
  "Confirm Sale":       (PRIMARY_L, "rgba(59,130,246,.16)"),
  # Contract / transfer
  "Signed":             (SUCCESS,   "rgba(34,197,94,.14)"),
  "Unsigned":           (TXT3,      "rgba(107,114,128,.18)"),
  "Not Ready":          (TXT3,      "rgba(107,114,128,.18)"),
  # Accounting-style removal
  "Void":               (ERROR,     "rgba(239,68,68,.15)"),
  "Reversed":           (ERROR,     "rgba(239,68,68,.15)"),
  # Impact badges — dots plus a label, never colour alone
  "Existing":           (SUCCESS,   "rgba(34,197,94,.14)"),
  "Add column":         (WARNING,   "rgba(251,191,36,.15)"),
  "New table":          (SECOND,    "rgba(167,139,250,.16)"),
  "Config only":        (PRIMARY_L, "rgba(59,130,246,.16)"),
})

# Impact level on the existing workflow -- used on Main and Migration
IMPACT = {
  0: ("No impact",   SUCCESS,   "rgba(34,197,94,.14)"),
  1: ("Low",         PRIMARY_L, "rgba(59,130,246,.16)"),
  2: ("Medium",      WARNING,   "rgba(251,191,36,.15)"),
  3: ("High",        ERROR,     "rgba(239,68,68,.15)"),
}

def impact_chip(level):
    label, c, bg = IMPACT[level]
    dots = "●" * (level or 1) if level else "—"
    return (f'<span class="chip" style="color:{c};background:{bg}">'
            f'<span style="font-size:9px;letter-spacing:1px">{dots}</span>{label}</span>')

I_CAM    = '<path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"></path><circle cx="12" cy="13" r="4"></circle>'
I_MONEY  = '<line x1="12" y1="1" x2="12" y2="23"></line><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path>'
I_ARROW  = '<line x1="5" y1="12" x2="19" y2="12"></line><polyline points="12 5 19 12 12 19"></polyline>'
I_LOCK   = '<rect x="3" y="11" width="18" height="11" rx="2"></rect><path d="M7 11V7a5 5 0 0 1 10 0v4"></path>'
I_USER   = '<path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle>'
I_BUILD  = '<rect x="4" y="2" width="16" height="20" rx="2"></rect><line x1="9" y1="7" x2="9" y2="7"></line><line x1="15" y1="7" x2="15" y2="7"></line><line x1="9" y1="12" x2="9" y2="12"></line><line x1="15" y1="12" x2="15" y2="12"></line>'
I_X      = '<line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line>'
