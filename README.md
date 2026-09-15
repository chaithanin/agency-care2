# agency-care2

ที่เก็บงานพัฒนาโมดูลของ Agency Care

## โปรเจกต์ย่อยในรีโปนี้

| โฟลเดอร์ | คืออะไร |
| --- | --- |
| [`apps/chat-inbox`](apps/chat-inbox) | ต้นแบบระบบแชทรวมช่องทาง (Inbox + Automations) พร้อม REST API และ webhook ที่ Agency Care เรียกใช้ได้ — รันในเครื่องได้ทันทีด้วย Node 22 โดยไม่ต้องติดตั้ง dependency |

เริ่มจากตรงนี้:

```bash
cd apps/chat-inbox
npm run demo    # เห็นภาพรวมทั้งระบบในคำสั่งเดียว
```

รายละเอียดการติดตั้ง, รายการ API และสัญญา webhook อยู่ใน [apps/chat-inbox/README.md](apps/chat-inbox/README.md)
