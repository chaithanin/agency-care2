from shell import *

# ══════ 1. บนสุด — Filter + KPI + Audience + Channel + Trend ══════
def seg(items, active):
    out = []
    for t in items:
        on = t == active
        style = (f"background:{PRIMARY};color:#fff;font-weight:700"
                 if on else f"color:{TXT2};font-weight:600")
        out.append(f'<div style="padding:6px 15px;border-radius:999px;font-size:13px;{style}">{t}</div>')
    return (f'<div class="row" style="gap:3px;background:{SURFACE};border:1px solid {DIVIDER};'
            f'border-radius:999px;padding:3px">{"".join(out)}</div>')

filters = f"""<div class="card" style="padding:14px 18px">
  <div class="row" style="gap:12px;flex-wrap:wrap;align-items:center">
    {seg(["Today","7 Days","This Month","Custom"], "7 Days")}
    <div class="row fld" style="gap:8px;padding:7px 12px;border-radius:999px">
      <span class="b2">All Channels</span>{icon(I_CHEV,14,TXT3)}</div>
    <div class="row fld" style="gap:8px;padding:7px 12px;border-radius:999px">
      <span class="b2">All Projects</span>{icon(I_CHEV,14,TXT3)}</div>
    <div class="row fld" style="gap:8px;padding:7px 12px;border-radius:999px">
      <span class="b2">All Contact Types</span>{icon(I_CHEV,14,TXT3)}</div>
    <div class="row fld" style="gap:8px;padding:7px 12px;border-radius:999px">
      <span class="b2">All Sales</span>{icon(I_CHEV,14,TXT3)}</div>
    <span class="grow"></span>
    <button class="btn sm out">Refresh</button>
    <button class="btn sm out">Export Report</button>
  </div>
  <p class="cap mut" style="margin:10px 0 0">ตัวกรองชุดนี้ใช้กับทุกกล่องในหน้าพร้อมกัน ·
    ข้อมูล ณ 16 Sep 2026 15:04 · ซิงก์จาก respond.io ล่าสุด 4 นาทีที่แล้ว</p>
</div>"""

kpis = f"""<div class="row" style="gap:12px;flex-wrap:wrap">
  {kpi("Total Contacts","12,486")}
  {kpi("New Contacts","+386","18%")}
  {kpi("Active Conversations","142")}
  {kpi("New Leads","264","9%")}
  {kpi("Avg. First Response","3m 24s","12s", delta_good=False)}
  {kpi("Resolution Rate","91%","2%")}
  {kpi("Broadcast Read Rate","76%")}
  {kpi("Reservations / Closed","18 / 32")}
</div>"""

# ── Audience ──
AUD = [("Customer", 46.8, S_BLUE, "5,842"), ("Agency", 17.3, S_ORANGE, "2,164"),
       ("Sales", 0.7, S_AQUA, "86"), ("Unclassified", 3.2, S_YELLOW, "394")]
aud_rows = "".join(
    f'<div class="row" style="gap:12px;align-items:center;padding:6px 0;cursor:pointer">'
    f'<span style="width:11px;height:11px;border-radius:3px;background:{c};flex-shrink:0"></span>'
    f'<span class="b2 grow" style="color:{TXT2}">{l}</span>'
    f'<span class="b2" style="font-weight:700;width:64px;text-align:right">{v}</span>'
    f'<span class="cap mut" style="width:52px;text-align:right">{p}%</span></div>'
    for l, p, c, v in AUD)

audience = panel("Audience",
  f'<span class="cap mut">กดตัวเลขเพื่อดูรายชื่อ</span>',
  f"""<div class="row" style="gap:22px;align-items:center">
    {donut([(l, p, c) for l, p, c, v in AUD], 168, 26)}
    <div class="col grow" style="gap:0">
      <div class="col" style="gap:1px;padding-bottom:10px;border-bottom:1px solid {DIVIDER}">
        <span style="font-size:26px;font-weight:700;letter-spacing:-0.02em">12,486</span>
        <span class="cap mut">Total Contacts</span>
      </div>
      <div class="col" style="gap:0;padding-top:6px">{aud_rows}</div>
    </div>
  </div>
  <div class="row" style="gap:10px;background:rgba(250,178,25,.10);border:1px solid rgba(250,178,25,.35);
       border-radius:14px;padding:10px 14px">
    {icon(I_WARN,16,ST_WARN)}
    <span class="b2" style="color:{ST_WARN};font-weight:600">394 unclassified — ยังไม่รู้ว่าเป็นใคร</span>
    <span class="grow"></span><span class="cap mut">New today +48</span>
  </div>""")

# ── Omnichannel Performance ──
CH = [("LINE","5,842","486","192","2m 48s",S_BLUE,"Healthy",56),
      ("Facebook","2,947","281","84","4m 12s",S_ORANGE,"Healthy",22),
      ("Instagram","1,866","194","62","3m 51s",S_AQUA,"Healthy",13),
      ("WhatsApp","931","86","28","5m 16s",S_YELLOW,"Monitor",6),
      ("Website","486","43","21","2m 19s",S_MAGENTA,"Healthy",3)]
ch_rows = ""
for name, contacts, convo, leads, resp, color, st, pct in CH:
    sc, sbg = ((ST_GOOD,"rgba(12,163,12,.16)") if st == "Healthy" else (ST_WARN,"rgba(250,178,25,.15)"))
    ch_rows += f"""<tr>
  <td><div class="row" style="gap:9px"><span style="width:11px;height:11px;border-radius:3px;
      background:{color};flex-shrink:0"></span><span style="font-weight:600">{name}</span></div></td>
  <td style="text-align:right">{contacts}</td><td style="text-align:right">{convo}</td>
  <td style="text-align:right;font-weight:600">{leads}</td><td style="text-align:right">{resp}</td>
  <td><span class="chip" style="color:{sc};background:{sbg}">{st}</span></td>
</tr>"""

channels = panel("Omnichannel Performance", "",
  f"""<div class="row" style="gap:24px;align-items:flex-start">
    <div class="col" style="gap:10px;flex-shrink:0">
      <span class="cap mut" style="font-weight:600">Conversations by channel</span>
      {donut([(n, p, c) for n, _, _, _, _, c, _, p in CH], 150, 24)}
    </div>
    <div class="grow">
      <table><thead><tr>
        <th>Channel</th><th style="text-align:right">Contacts</th>
        <th style="text-align:right">Conversations</th><th style="text-align:right">New Leads</th>
        <th style="text-align:right">Avg Response</th><th style="width:110px">Status</th>
      </tr></thead><tbody>{ch_rows}</tbody></table>
    </div>
  </div>
  {legend([(n, c) for n, _, _, _, _, c, _, _ in CH])}""",
  note="Monitor = ตอบช้ากว่าเกณฑ์ 5 นาที ยังไม่ถึงขั้นวิกฤต")

# ── Trend ──
LAB = ["10 Sep","11","12","13","14","15","16"]
trend = panel("Contact &amp; Conversation Trend",
  seg(["Daily","Weekly","Monthly"], "Daily"),
  f"""{line_chart([
      ("New Contacts",[42,58,51,74,66,88,96], S_BLUE),
      ("Conversations",[38,44,41,59,52,71,78], S_ORANGE),
      ("Resolved",[31,40,37,52,48,64,72], S_AQUA)],
      LAB, w=980, h=230)}
  {legend([("New Contacts",S_BLUE),("Conversations",S_ORANGE),("Resolved Conversations",S_AQUA)])}""")

body = f"""{filters}
{kpis}
<div class="row" style="gap:18px;align-items:stretch">{audience}{channels}</div>
{trend}"""

open("Main.dc.html","w").write(
    dash("Omnichannel Overview",
         "respond.io เป็นแหล่งข้อมูล · Agency Care สรุปให้ผู้บริหารดูในหน้าเดียว",
         body, 1760, 1240))
print("Main.dc.html")
