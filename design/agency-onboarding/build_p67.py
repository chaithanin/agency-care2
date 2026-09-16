from shell import *

# ── Phase 6 — Post-Onboarding Support ────────────────────────
MAT = [("Latest Construction Update",True),("Price Lists",True),("Availability Lists",True),
       ("Matrix",True),("Company Profile",False),("Sales Kit",True),("Promotions",False)]
mat = "".join(check(x, d) for x, d in MAT)

visit_form = f"""<div class="col" style="gap:14px">
  <div class="row" style="gap:14px">
    {field("Visit Date","12 Sep 2026", w=180)}
    {field("Visited By","K. Somchai, K. Marketing")}
    {field("Agency Office Location","Second Road, Pattaya")}
  </div>
  {field("Purpose","Post-signing visit — deliver materials and review project presentation")}
  {multiselect("Agency Needs", ["Brochures","Stand","Price List"],
               ["Flyers","Posters","Model","Window Sticker","Window Picture","Other"])}
  <div class="col" style="gap:0">
    <p class="lbl">Materials Delivered</p>
    <table>
      <thead><tr><th>Item</th><th style="width:120px">Quantity</th></tr></thead>
      <tbody>
        <tr><td>Brochure — Ocean Residence</td><td>120</td></tr>
        <tr><td>Floor-standing display</td><td>1</td></tr>
        <tr><td>Price list (printed)</td><td>25</td></tr>
      </tbody>
    </table>
  </div>
  <div class="row" style="gap:14px;align-items:flex-start">
    <div class="col grow" style="gap:0">
      <p class="lbl">Visit Photos</p>
      <div class="row" style="gap:10px">
        <div style="width:78px;height:78px;border-radius:12px;background:{SURFACE};border:1px solid {DIVIDER}"></div>
        <div style="width:78px;height:78px;border-radius:12px;background:{SURFACE};border:1px solid {DIVIDER}"></div>
        <div style="width:78px;height:78px;border-radius:12px;border:1.5px dashed {DIVIDER};
             display:grid;place-items:center">{icon(I_PLUS,18,TXT3)}</div>
      </div>
    </div>
    <div class="col" style="gap:0;width:280px;flex-shrink:0">
      <p class="lbl">Project Presentation Quality</p>
      <div class="row" style="gap:8px">
        <span class="chip" style="background:rgba(34,197,94,.15);color:{SUCCESS}">Good</span>
        <span class="chip" style="border:1px solid {DIVIDER};color:{TXT3}">Needs Improvement</span>
      </div>
    </div>
  </div>
  <div class="col" style="gap:0">
    <p class="lbl">Internal Notes</p>
    <div class="fld" style="min-height:64px;color:{TXT2}">Office is well located but the window
      display is empty — offered a window sticker set. Sales team presents from phone only;
      suggested the tablet kit.</div>
  </div>
</div>"""

body = f"""<div class="row" style="gap:12px">
  <h2 class="h6 grow">Phase 6 — Post-Onboarding Support</h2>
  <span class="cap mut">Last Material Update: 16 Sep 2026</span>
</div>
{panel("Sales Materials", f'<span class="cap mut">5 / 7</span>',
  f'<div style="display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:0 24px">{mat}</div>')}
{panel("Agency Visit",
  f'<button class="btn sm">{icon(I_PLUS,13,"#fff")} &nbsp;New Visit</button>', visit_form)}
<div class="row" style="gap:10px;justify-content:flex-end">
  <button class="btn out">Back</button>
  <button class="btn">Continue to Phase 7</button>
</div>"""
open("Phase6.dc.html","w").write(detail_page(6, body, 1780, pct=83, status="IN PROGRESS", done=34, total=41, outstanding=4))
print("Phase6.dc.html")

# ── Phase 7 — Relationship Maintenance ───────────────────────
SCHED = [("Agency Visit",2,1),("Agency Call",4,3),("Material Update",4,4),
         ("Customer Viewing Support",None,2)]
srows = ""
for name, target, done in SCHED:
    if target is None:
        prog, tgt = f'<span class="cap mut">no target</span>', "—"
    else:
        pct = int(done / target * 100)
        col = SUCCESS if done >= target else WARNING
        prog = f'<div style="width:150px">{bar(pct, col)}</div>'
        tgt = str(target)
    srows += (f'<tr><td style="font-weight:600">{name}</td><td>{tgt}</td>'
              f'<td style="font-weight:700">{done}</td><td>{prog}</td></tr>')

sched_body = f"""<table>
  <thead><tr><th>Activity</th><th style="width:100px">Target</th>
    <th style="width:120px">Completed</th><th style="width:190px">Progress</th></tr></thead>
  <tbody>{srows}</tbody></table>
<div class="row" style="gap:10px;background:rgba(251,191,36,.10);
     border:1px solid rgba(251,191,36,.35);border-radius:14px;padding:11px 14px">
  {icon(I_WARN,16,WARNING)}
  <span class="b2" style="color:{WARNING};font-weight:600">Agency Visit: 1 visit remaining this month</span>
  <span class="grow"></span>
  <button class="btn sm out">Create task</button>
</div>"""

TYPES = ["Meeting","Call","Visit","Customer Feedback","Opportunity","Agency Request","Issue","Closing Result"]
chips = "".join(
    f'<span class="chip" style="{"background:rgba(59,130,246,.16);color:"+PRIMARY_L if t=="Visit" else "border:1px solid "+DIVIDER+";color:"+TXT3}">{t}</span>'
    for t in TYPES)

activity_body = f"""<div class="col" style="gap:14px">
  <div class="col" style="gap:0">
    <p class="lbl">Activity Type</p>
    <div class="row" style="gap:8px;flex-wrap:wrap">{chips}</div>
  </div>
  <div class="col" style="gap:0"><p class="lbl">Notes</p>
    <div class="fld" style="min-height:64px;color:{TXT2}">Dropped off new brochures and reviewed
      the September availability list with the sales team.</div></div>
  <div class="row" style="gap:14px">
    {field("Related Customer","Mr. Ivan K.")}
    {field("Opportunity Value","฿ 5,400,000", w=210)}
    {field("Next Follow-up","23 Sep 2026", w=180)}
  </div>
  <div class="row" style="gap:12px">
    <button class="btn sm out">{icon(I_UP,13,TXT2)} &nbsp;Attachment</button>
    <span class="grow"></span>
    <button class="btn sm">Add Activity</button>
  </div>
</div>"""

ready_body = f"""<div class="col" style="gap:16px">
  <div class="row" style="gap:20px;align-items:center">
    <div class="col" style="gap:2px">
      <div style="font-size:36px;font-weight:700;letter-spacing:-0.02em;color:{WARNING}">95%</div>
      <div class="cap mut">Onboarding readiness</div>
    </div>
    <div class="col grow" style="gap:8px">
      {bar(95, WARNING)}
      <span class="cap mut">2 required items remaining before this agency can be completed</span>
    </div>
  </div>
  <div class="col" style="gap:8px">
    <div class="row" style="gap:10px;background:rgba(239,68,68,.10);
         border:1px solid rgba(239,68,68,.32);border-radius:14px;padding:10px 14px">
      {icon(I_CIRCLE,16,ERROR)}<span class="b2" style="color:{ERROR};font-weight:600">Owner Passport</span>
      <span class="grow"></span><button class="btn sm out">Upload</button></div>
    <div class="row" style="gap:10px;background:rgba(239,68,68,.10);
         border:1px solid rgba(239,68,68,.32);border-radius:14px;padding:10px 14px">
      {icon(I_CIRCLE,16,ERROR)}<span class="b2" style="color:{ERROR};font-weight:600">Signed Agreement</span>
      <span class="grow"></span><button class="btn sm out">Upload</button></div>
  </div>
  <div style="height:1px;background:{DIVIDER}"></div>
  <div class="row" style="gap:14px">
    <button class="btn" style="background:{SURFACE};color:{TXT3};cursor:not-allowed">Complete Onboarding</button>
    <span class="cap mut" style="max-width:420px">Stays disabled until every mandatory item is
      verified — completion is calculated, never set by hand.</span>
  </div>
</div>"""

body7 = f"""<div class="row" style="gap:12px">
  <h2 class="h6 grow">Phase 7 — Relationship Maintenance</h2>
  <span class="cap mut">September 2026</span>
</div>
{panel("Relationship Schedule",
  f'<span class="cap mut">Auto-generated after onboarding completes</span>', sched_body,
  note="Targets follow the standing rule: 2 agency visits and 4 calls per month, materials weekly.")}
{panel("Add Agency Activity", "", activity_body)}
{panel("Completion", f'<span class="chip" style="color:{WARNING};background:rgba(251,191,36,.15)">2 required items remaining</span>', ready_body)}
<div class="card pad row" style="gap:14px;border-color:rgba(34,197,94,.35);background:rgba(34,197,94,.07)">
  <div style="width:34px;height:34px;border-radius:999px;background:{SUCCESS};display:grid;place-items:center;flex-shrink:0">
    {icon(I_CHECK,19,"#0F172A")}</div>
  <div class="col grow" style="gap:2px">
    <span class="b2" style="font-weight:700;color:{SUCCESS}">Agency Successfully Onboarded</span>
    <span class="cap mut">Completed 18 Sep 2026 · Onboarded by K. Somchai · Assigned Seller K. Somchai
      — agency moves to Relationship Maintenance automatically</span>
  </div>
  <span class="cap mut" style="font-style:italic">preview of the completed state</span>
</div>"""
open("Phase7.dc.html","w").write(detail_page(7, body7, 1800, pct=95, status="IN PROGRESS", done=39, total=41, outstanding=2))
print("Phase7.dc.html")
