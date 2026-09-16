from shell import *

def big(n, label, color=None):
    return (f'<div class="col" style="gap:1px"><span style="font-size:26px;font-weight:700;'
            f'letter-spacing:-0.02em;color:{color or TXT}">{n}</span>'
            f'<span class="cap mut">{label}</span></div>')

# ── Conversation Performance ──
sla_rows = ""
for label, pct, color in [("Within 5 min",78,ST_GOOD),("Within 15 min",92,ST_GOOD),("Over 30 min",8,ST_SERIOUS)]:
    sla_rows += f"""<div class="row" style="gap:14px;align-items:center">
  <span class="b2" style="width:120px;flex-shrink:0;color:{TXT2}">{label}</span>
  <div style="width:230px;flex-shrink:0;height:12px;background:{SURFACE};border-radius:4px">
    <div style="width:{pct}%;height:12px;background:{color};border-radius:4px"></div></div>
  <span class="b2" style="font-weight:700">{pct}%</span>
</div>"""

convo = panel("Conversation Performance", "",
  f"""<div class="row" style="gap:26px;flex-wrap:wrap">
    {big("386","Opened")}{big("352","Resolved",ST_GOOD)}{big("34","Open")}{big("12","Overdue",ST_CRIT)}
  </div>
  <div style="height:1px;background:{DIVIDER}"></div>
  <div class="row" style="gap:26px;flex-wrap:wrap">
    {big("3m 24s","Avg. First Response")}{big("5m 42s","Avg. Response")}
    {big("1h 18m","Avg. Resolution")}{big("91%","Resolution Rate")}
  </div>
  <div style="height:1px;background:{DIVIDER}"></div>
  <div class="col" style="gap:9px"><span class="sec">SLA</span>{sla_rows}</div>""")

# ── Customer vs Agency ──
CVA = [("Active Contacts","3,824","986"),("Conversations","412","184"),
       ("New This Month","264","38"),("Avg. Response","3m 16s","4m 02s"),
       ("Active last 30d","78%","66%")]
crows = "".join(
    f'<tr><td style="color:{TXT2}">{m}</td>'
    f'<td style="text-align:right;font-weight:700">{c}</td>'
    f'<td style="text-align:right;font-weight:700">{a}</td></tr>' for m, c, a in CVA)
cva = panel("Customer vs Agency", "",
  f"""<table><thead><tr><th>Metric</th>
    <th style="text-align:right;width:110px"><span class="row" style="gap:7px;justify-content:flex-end">
      <span style="width:11px;height:11px;border-radius:3px;background:{S_BLUE}"></span>Customer</span></th>
    <th style="text-align:right;width:110px"><span class="row" style="gap:7px;justify-content:flex-end">
      <span style="width:11px;height:11px;border-radius:3px;background:{S_ORANGE}"></span>Agency</span></th>
  </tr></thead><tbody>{crows}</tbody></table>""",
  note="ดูว่าทีมดูแลลูกค้าตรงกับเครือข่ายเอเจนซี่ได้สมดุลแค่ไหน")

# ── Broadcast ──
BC = [("Customer",72,S_BLUE),("Agency",84,S_ORANGE),("Sales",96,S_AQUA)]
brows = "".join(hbar(l, p, "read rate", c, 210) for l, p, c in BC)
recent = "".join(
    f'<div class="row" style="gap:12px;padding:8px 0;border-bottom:1px solid {DIVIDER}">'
    f'<span class="b2 grow" style="color:{TXT2}">{t}</span>'
    f'<span class="cap mut">{d}</span></div>'
    for t, d in [("LOVE IT September Promotion","76% read"),
                 ("MGB Final Pre-Sale","81% read"),
                 ("Harmonia Construction Update","69% read")])
bcast = panel("Broadcast Performance",
  '<button class="btn sm out">View All Broadcasts</button>',
  f"""<div class="row" style="gap:26px;flex-wrap:wrap">
    {big("24","Campaigns")}{big("8,486","Sent")}{big("8,271","Delivered",ST_GOOD)}
    {big("6,384","Read")}{big("76%","Read Rate")}{big("215","Failed",ST_CRIT)}
  </div>
  <div style="height:1px;background:{DIVIDER}"></div>
  <div class="col" style="gap:9px"><span class="sec">Read rate by audience</span>{brows}
    {legend([(l, c) for l, _, c in BC])}</div>
  <div style="height:1px;background:{DIVIDER}"></div>
  <div class="col" style="gap:0"><span class="sec" style="padding-bottom:4px">Recent campaigns</span>{recent}</div>""")

# ── Team ──
TEAM = [("K. May","128","72","2m 18s","68","4",ST_GOOD),
        ("K. Anna","104","61","3m 02s","55","6",ST_GOOD),
        ("K. John","96","48","4m 26s","39","9",ST_WARN),
        ("K. Nira","88","44","5m 51s","31","13",ST_SERIOUS)]
trows = ""
for name, assigned, convos, resp, resolved, open_, c in TEAM:
    trows += (f'<tr><td style="font-weight:600">{name}</td>'
              f'<td style="text-align:right">{assigned}</td><td style="text-align:right">{convos}</td>'
              f'<td style="text-align:right;color:{c};font-weight:600">{resp}</td>'
              f'<td style="text-align:right">{resolved}</td>'
              f'<td style="text-align:right;font-weight:600">{open_}</td></tr>')
team = panel("Team Performance",
  f"""<div class="row" style="gap:6px">
    <span class="chip" style="background:rgba(59,130,246,.16);color:{PRIMARY_L}">All</span>
    <span class="chip" style="border:1px solid {DIVIDER};color:{TXT3}">Customer Team</span>
    <span class="chip" style="border:1px solid {DIVIDER};color:{TXT3}">Agency Team</span>
  </div>""",
  f"""<table><thead><tr><th>Sales / Staff</th>
    <th style="text-align:right">Assigned</th><th style="text-align:right">Conversations</th>
    <th style="text-align:right">First Response</th><th style="text-align:right">Resolved</th>
    <th style="text-align:right">Open</th></tr></thead><tbody>{trows}</tbody></table>""",
  note="เรียงตามภาระงาน ไม่ใช่การจัดอันดับแข่งกัน — สีบอกเวลาตอบที่เริ่มช้า")

body = f"""<div class="row" style="gap:18px;align-items:flex-start">{convo}{cva}</div>
<div class="row" style="gap:18px;align-items:flex-start">{bcast}{team}</div>"""
open("Performance.dc.html","w").write(
    dash("Omnichannel Overview — Performance",
         "ทีมตอบเร็วแค่ไหน ดูแลสองฝั่งสมดุลไหม และ broadcast ได้ผลเท่าไร",
         body, 1560, 1180))
print("Performance.dc.html")
