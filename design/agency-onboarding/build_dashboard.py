from tokens import *

def stat(n, label, color, active=False):
    ring = f"border:1px solid {color}" if active else f"border:1px solid {DIVIDER}"
    return f"""<div class="col" style="background:{PAPER};{ring};border-radius:20px;padding:16px 20px;gap:2px;min-width:150px">
  <div style="font-size:28px;font-weight:700;letter-spacing:-0.02em;color:{color}">{n}</div>
  <div class="cap" style="font-weight:600">{label}</div>
</div>"""

def agency_card(name, code, status, seller, phase_no, phase_name, pct, done, total,
                last, next_action, alert=None):
    color = {"NEW": INFO, "IN PROGRESS": PRIMARY_L, "WAITING AGENCY": SECOND,
             "NEED ATTENTION": WARNING, "COMPLETED": SUCCESS}[status]
    alert_html = ""
    if alert:
        alert_html = f"""<div class="row" style="gap:8px;background:rgba(251,191,36,.10);
      border:1px solid rgba(251,191,36,.35);border-radius:12px;padding:9px 12px">
      {icon(I_WARN, 16, WARNING)}
      <span class="b2" style="color:{WARNING};font-weight:600">{alert}</span></div>"""
    btns = f"""<button class="btn sm">Open Onboarding</button>
        <button class="btn sm out">View Agency</button>"""
    return f"""<div class="card pad col" style="gap:14px">
  <div class="row" style="gap:12px">
    <div class="col grow" style="gap:2px">
      <div class="h6" style="font-size:17px;font-weight:700">{name}</div>
      <div class="cap mut">{code} · Assigned: {seller}</div>
    </div>
    {status_chip(status)}
  </div>

  <div class="col" style="gap:7px">
    <div class="row" style="gap:8px">
      <span class="cap" style="color:{TXT2};font-weight:600">Phase {phase_no} of 7 — {phase_name}</span>
      <span class="grow"></span>
      <span class="b2" style="font-weight:700;color:{color}">{pct}%</span>
    </div>
    {bar(pct, color)}
    <div class="cap mut">{done} / {total} required items completed</div>
  </div>

  {alert_html}

  <div class="row" style="gap:16px;align-items:flex-start">
    <div class="col grow" style="gap:2px">
      <div class="cap mut" style="font-weight:600">Next Action</div>
      <div class="b2" style="font-weight:600">{next_action}</div>
    </div>
    <div class="col" style="gap:2px;align-items:flex-end">
      <div class="cap mut" style="font-weight:600">Last activity</div>
      <div class="b2">{last}</div>
    </div>
  </div>

  <div style="height:1px;background:{DIVIDER}"></div>
  <div class="row" style="gap:10px">{btns}</div>
</div>"""

NAV_GROUPS = [
    ("OVERVIEW", []), ("LEADS & CUSTOMERS", []), ("SALES", []),
    ("AGENCIES", ["Agency List", "Agency Matrix", "Agency Transfers",
                  "Location Verification", "Onboarding"]),
    ("PROPERTIES", []), ("FIELD WORK", []), ("TASKS & DOCUMENTS", []),
]

def sidebar():
    out = []
    for title, items in NAV_GROUPS:
        out.append(f'<div class="row" style="gap:8px;padding:11px 14px">'
                   f'<span class="sec" style="font-size:11px">{title}</span>'
                   f'<span class="grow"></span>{icon(I_CHEV,14,TXT3)}</div>')
        for it in items:
            on = it == "Onboarding"
            style = (f"background:rgba(59,130,246,.16);color:{PRIMARY_L};font-weight:600"
                     if on else f"color:{TXT2}")
            out.append(f'<div class="row" style="gap:10px;margin:2px 8px;padding:9px 12px;'
                       f'border-radius:14px;{style}"><span class="b2">{it}</span></div>')
    return f"""<div class="col" style="width:232px;flex-shrink:0;background:{PAPER};
     border-right:1px solid {DIVIDER};padding:16px 0;gap:0">
  <div class="row" style="gap:10px;padding:0 16px 18px">
    <div style="width:38px;height:38px;border-radius:11px;background:linear-gradient(135deg,{PRIMARY},{SECOND});
         display:grid;place-items:center;font-weight:800;font-size:15px;color:#fff">AC</div>
    <div class="col" style="gap:0">
      <span class="b2" style="font-weight:700">Agency Care</span>
      <span style="font-size:10px;letter-spacing:.14em;color:{TXT3}">CONNECT · VISIT · GROW</span>
    </div>
  </div>
  {''.join(out)}
</div>"""

def filter_pill(label, value=None):
    v = value or label
    strong = value is not None
    col = TXT if strong else TXT2
    return (f'<div class="row fld" style="gap:8px;padding:8px 12px;border-radius:999px;cursor:pointer">'
            f'<span class="b2" style="color:{col}">{v}</span>{icon(I_CHEV,14,TXT3)}</div>')

CARDS = [
    agency_card("ABC Property Pattaya", "AG-00238", "IN PROGRESS", "K. Somchai", 3,
                "System Entry & Digital Setup", 44, 18, 41,
                "Today 10:42", "Upload Owner Passport"),
    agency_card("Ocean Property", "AG-00241", "NEED ATTENTION", "K. Anna", 5,
                "Agreement & Formal Setup", 68, 28, 41,
                "12 Sep 2026, 16:20", "Chase signed agreement",
                alert="Agreement pending signature — 4 days"),
    agency_card("Siam Estate Bangkok", "AG-00244", "NEW", "K. Warun", 1,
                "Pre-Onboarding", 9, 3, 34,
                "16 Sep 2026, 09:05", "Collect agency background form"),
    agency_card("Bright Living Phuket", "AG-00230", "WAITING AGENCY", "K. Nira", 4,
                "First Communication Package", 59, 24, 41,
                "12 Sep 2026, 14:10", "Waiting agency to confirm materials received",
                alert="เงียบมา 4 วัน — ระบบตั้ง Waiting Agency ให้เองเมื่อครบ 3 วัน"),
]

inner = f"""<div class="row" style="align-items:stretch;min-height:1180px">
{sidebar()}
<div class="col grow" style="padding:26px 30px;gap:20px">

  <div class="row" style="gap:12px">
    <div class="col grow" style="gap:3px">
      <h1 class="h5">New Agency Onboarding</h1>
      <p class="cap mut" style="margin:0">Track every agency from first meeting to full partnership</p>
    </div>
    <button class="btn out">Export</button>
    <button class="btn">Start Onboarding</button>
  </div>

  <div class="row" style="gap:12px;flex-wrap:wrap">
    {stat(12,"Total",TXT)}
    {stat(3,"New",INFO)}
    {stat(6,"In Progress",PRIMARY_L,active=True)}
    {stat(2,"Need Attention",WARNING)}
    {stat(1,"Completed",SUCCESS)}
  </div>

  <div class="card" style="padding:14px 18px">
    <div class="row" style="gap:10px;flex-wrap:wrap">
      <div class="row fld grow" style="gap:9px;padding:8px 14px;border-radius:999px;min-width:280px">
        {icon(I_SEARCH,16,TXT3)}
        <span class="b2 mut">Search agency / owner / seller...</span>
      </div>
      {filter_pill("All Agencies")}
      {filter_pill("Assigned Seller")}
      {filter_pill("Current Phase")}
      {filter_pill("Status")}
      {filter_pill("Last Activity")}
    </div>
  </div>

  <div style="display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px">
    {''.join(CARDS)}
  </div>

</div>
</div>"""

open("Main.dc.html", "w").write(page(inner, 1440, 1180))
print("Main.dc.html เขียนแล้ว")
