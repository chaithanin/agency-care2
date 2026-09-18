# คำสั่งสำหรับตัวหลัก

ส่งทีละก้อน ก้อนก่อนหน้าต้องขึ้น production แล้วจึงส่งก้อนถัดไป

คำสั่งสั้นได้เพราะ `BRIEF.md` ลิงก์ไปหาไฟล์ที่เหลือทั้งหมดไว้แล้ว —
work order, audit, ผลกระทบตอน deploy, คำถามที่ยังไม่ตัดสิน และกฎของโปรเจกต์

ถ้า session ปลายทางมองไม่เห็นรีโปนี้ ดู [`FETCH.md`](./FETCH.md) — มี 3 วิธี ทดสอบแล้วทุกวิธี

---

## ก้อนที่ 0 — patch ที่เขียนเสร็จแล้ว (ส่งก่อน)

> เอา patch ที่เตรียมไว้ไป apply
>
> คำสั่งเต็มอยู่ที่รีโป chaithanin/agency-care2
> branch claude/agency-care-test-project-zo163o
> ไฟล์ design/sales-crm-restructure/patches/README.md — อ่านทั้งไฟล์ก่อนเริ่ม
>
> แตกงานจาก feat/all-appointments-clean-on-118a2e2 เท่านั้น
> เสร็จแล้วเปิด PR อย่าเพิ่ง deploy

---

## ก้อนที่ 1 — Core Sales Architecture

> ทำ Phase 1 Core Sales Architecture ตามแบบที่
> https://claude.ai/artifact/SNAd42xy9r3icnxvxFfHhf
>
> คำสั่งเต็มอยู่ที่รีโป chaithanin/agency-care2
> branch claude/agency-care-test-project-zo163o
> ไฟล์ design/sales-crm-restructure/BRIEF.md — อ่านทั้งไฟล์ก่อนเริ่ม
> แล้วอ่าน WORK_ORDERS.md หัวข้อ Phase 1 ต่อ
>
> แตกงานจาก feat/all-appointments-clean-on-118a2e2 เท่านั้น
> เสร็จแล้วเปิด PR อย่าเพิ่ง deploy

---

## ก้อนที่ 2 — Financial

> ทำ Phase 2 Financial ตามแบบที่
> https://claude.ai/artifact/SNAd42xy9r3icnxvxFfHhf
>
> คำสั่งเต็มอยู่ที่รีโป chaithanin/agency-care2
> branch claude/agency-care-test-project-zo163o
> ไฟล์ design/sales-crm-restructure/BRIEF.md — อ่านทั้งไฟล์ก่อนเริ่ม
> แล้วอ่าน WORK_ORDERS.md หัวข้อ Phase 2 ต่อ
>
> Phase 1 ขึ้น production แล้ว
> แตกงานจาก feat/all-appointments-clean-on-118a2e2 เท่านั้น
> เสร็จแล้วเปิด PR อย่าเพิ่ง deploy

---

## ก้อนที่ 3 — Commission

> ทำ Phase 3 Commission ตามแบบที่
> https://claude.ai/artifact/SNAd42xy9r3icnxvxFfHhf
>
> คำสั่งเต็มอยู่ที่รีโป chaithanin/agency-care2
> branch claude/agency-care-test-project-zo163o
> ไฟล์ design/sales-crm-restructure/BRIEF.md — อ่านทั้งไฟล์ก่อนเริ่ม
> แล้วอ่าน WORK_ORDERS.md หัวข้อ Phase 3 ต่อ
>
> Phase 2 ขึ้น production แล้ว
> แตกงานจาก feat/all-appointments-clean-on-118a2e2 เท่านั้น
> เสร็จแล้วเปิด PR อย่าเพิ่ง deploy

---

## ก้อนที่ 4 — Agency & Visit

> ทำ Phase 4 Agency & Visit ตามแบบที่
> https://claude.ai/artifact/SNAd42xy9r3icnxvxFfHhf
>
> คำสั่งเต็มอยู่ที่รีโป chaithanin/agency-care2
> branch claude/agency-care-test-project-zo163o
> ไฟล์ design/sales-crm-restructure/BRIEF.md — อ่านทั้งไฟล์ก่อนเริ่ม
> แล้วอ่าน WORK_ORDERS.md หัวข้อ Phase 4 ต่อ
>
> Phase 3 ขึ้น production แล้ว
> แตกงานจาก feat/all-appointments-clean-on-118a2e2 เท่านั้น
> เสร็จแล้วเปิด PR อย่าเพิ่ง deploy

---

## ก้อนที่ 5 — Cleanup

> ทำ Phase 5 Cleanup ตามแบบที่
> https://claude.ai/artifact/SNAd42xy9r3icnxvxFfHhf
>
> คำสั่งเต็มอยู่ที่รีโป chaithanin/agency-care2
> branch claude/agency-care-test-project-zo163o
> ไฟล์ design/sales-crm-restructure/BRIEF.md — อ่านทั้งไฟล์ก่อนเริ่ม
> แล้วอ่าน WORK_ORDERS.md หัวข้อ Phase 5 ต่อ
>
> Phase 4 ขึ้น production แล้ว
> เฟสนี้กระทบสิ่งที่คนใช้ทุกวันมากที่สุด — route ที่ยุบต้อง redirect ห้ามลบ
> แตกงานจาก feat/all-appointments-clean-on-118a2e2 เท่านั้น
> เสร็จแล้วเปิด PR อย่าเพิ่ง deploy

---

## ถ้าตัวหลักถามกลับมา

| ถามเรื่อง | ชี้ไปที่ |
| --- | --- |
| ยังไม่ได้ตัดสิน / ไม่รู้จะเอาค่าไหน | `OPEN_DECISIONS.md` — 5 ข้อ มีคำตอบร่างและค่าตั้งต้นให้ทำไปก่อนทุกข้อ |
| เจอบั๊ก / ข้อมูลไม่เชื่อมกัน | `CODE_AUDIT.md` — ตรวจไว้แล้ว อ้างไฟล์และบรรทัด §4 บอกว่ากระทบเฟสไหน |
| จะ deploy | `DEPLOY_IMPACT.md` — Phase 1 เป็นเฟสเดียวที่ rollback container แล้วไม่คืน มี SQL กู้อยู่ในไฟล์ |
| ดึงไฟล์ไม่ได้ | `FETCH.md` — 3 วิธี ทดสอบแล้วทุกวิธี |

## เรื่องที่อย่าให้ถูกกวาดเข้าไปในเฟสไหน

`CODE_AUDIT.md` M2 · M3 · L2 — จงใจไม่แก้ เพราะสองข้อแรกต้องรู้นโยบายก่อน (ยูนิตที่ `sold` แล้วถูกยกเลิก
จะทำยังไง · ลบ lead ควร soft-delete แบบดีลหรือบล็อกแบบ agency) และข้อสุดท้ายเปลี่ยนวิธีออกเลขดีล
