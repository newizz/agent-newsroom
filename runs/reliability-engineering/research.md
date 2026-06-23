# Research: ภาพรวม Reliability Engineering — ACA, ASM, AHM, WEM, RCA→KM, ASO และความเชื่อมโยงทั้งหมด

**Slug:** reliability-engineering
**Brief:** runs/reliability-engineering/brief.md
**Research date:** 2026-06-23
**Confidence:** high

---

## TL;DR

Reliability Engineering ในบริบทของ Asset Performance Management (APM) คือกรอบงานที่จัดระเบียบการบำรุงรักษาสินทรัพย์อุตสาหกรรมเป็นวงจรปิดต่อเนื่อง 7 ขั้นตอน เรียกว่า "APM Loop" ได้แก่ ACA (วิเคราะห์ความสำคัญสินทรัพย์) → ASM (กำหนดกลยุทธ์บำรุงรักษา) → AHM (ติดตามสุขภาพสินทรัพย์แบบ real-time) → WEM (บริหารการปฏิบัติงานซ่อมบำรุง) → RCA (วิเคราะห์สาเหตุรากเหง้าเมื่อเกิดความล้มเหลว) → KM (จัดเก็บและเผยแพร่บทเรียนจาก RCA) → ASO (ปรับปรุงกลยุทธ์ด้วยข้อมูลเชิงปริมาณ) → วนกลับไปปรับ ASM ใหม่ [^1][^25] ตัวชี้วัดหลัก ได้แก่ MTBF, MTTR, OEE, Availability และ Cost of Unreliability (COUR) ซึ่งค่าเฉลี่ยอุตสาหกรรมสำหรับค่าหยุดเครื่องที่ไม่ได้วางแผนไว้อยู่ที่ 532,000 ดอลลาร์ต่อชั่วโมงในปี 2024 [^9] กรอบงานนี้ได้รับการสนับสนุนจากมาตรฐานสากล ISO 55000 และ SMRP Body of Knowledge และถูกนำไปใช้ในซอฟต์แวร์อย่าง GE Vernova APM, IBM Maximo, และ SAP APM [^20][^21][^23]

---

## Key findings

1. **ACA คือรากฐานของ APM Loop — ลงทุนในที่ที่คุ้มค่าที่สุด** — Asset Criticality Analysis ใช้สูตร Risk = Likelihood of Failure × Consequence of Failure เพื่อจัดลำดับความสำคัญของสินทรัพย์ทุกชิ้น โดยพิจารณาผลกระทบ 5 มิติ ได้แก่ ความปลอดภัย (Safety), กฎระเบียบ (Regulatory), ชื่อเสียง (Reputation), การผลิต (Production), และการเงิน (Financial) [^2] สินทรัพย์ที่ได้คะแนน Criticality สูง (Critical) จะได้รับงบประมาณ, กลยุทธ์ PdM/CBM, และความถี่การตรวจสอบที่มากกว่า ขณะที่สินทรัพย์ Non-Critical อาจใช้กลยุทธ์ Run-to-Failure อย่างมีเจตนา [^3]

2. **ASM แปลงผล ACA เป็นแผนบำรุงรักษาที่ถูกต้องตามหลักวิศวกรรม** — Asset Strategy Management กำหนดกลยุทธ์การบำรุงรักษา 4 ระดับ ได้แก่ Reactive (RTF), Time-Based Preventive (TBM), Condition-Based (CBM), และ Predictive Maintenance (PdM) โดยเกณฑ์เลือกขึ้นอยู่กับ: (a) ความสำคัญของสินทรัพย์ (ACA output), (b) รูปแบบความล้มเหลว (failure mode), (c) ความสามารถตรวจจับการเสื่อมสภาพก่อนล้มเหลว (P-F interval) [^4][^5] GE Vernova APM ใช้ RCM และ FMEA เป็นเครื่องมือหลักใน ASM เพื่อระบุ failure mode ทั้งหมดและกำหนด mitigating action [^6]

3. **AHM เป็น "ระบบตรวจสุขภาพสินทรัพย์" แบบ real-time โดยคำนวณ Health Score จากหลายแหล่งข้อมูล** — Asset Health Management รวบรวมข้อมูลจากเซ็นเซอร์วัดการสั่นสะเทือน (Vibration Analysis), อินฟราเรด (Thermography), การวิเคราะห์น้ำมัน (Oil Analysis), อัลตราซาวนด์ (Ultrasonic Detection), และ การตรวจสอบด้วยสายตา (Visual Inspection) เพื่อคำนวณ Asset Health Index (AHI) โดยอัตโนมัติ [^7][^8] เมื่อ Health Score ต่ำกว่า threshold ที่กำหนด ระบบจะส่ง recommendation ตรงไปยัง EAM เพื่อสร้าง Work Order โดยอัตโนมัติ [^8]

4. **WEM เป็นขั้นตอนที่แปลงกลยุทธ์เป็นการปฏิบัติงานจริง และต้นทุนงานเชิงรับสูงกว่างานเชิงรุก 2-4 เท่า** — Work Execution Management ครอบคลุมวงจรชีวิต Work Order ตั้งแต่การระบุความต้องการ (Identification) → การอนุมัติ (Approval) → การวางแผน (Planning) → การจัดตาราง (Scheduling) → การปฏิบัติงาน (Execution) → การปิดงาน (Closure) พร้อมบันทึก Actuals [^10] MRO (Maintenance, Repair and Operations) inventory คิดเป็น 40-60% ของงบประมาณบำรุงรักษาทั้งหมด และระบบที่ดีควรรักษา service level ที่ 95-97% [^11] ประสิทธิภาพแรงงานเพิ่มจาก <30% เป็น ~60% เมื่อเปลี่ยนจาก reactive เป็น planned/scheduled work [^11]

5. **RCA มี 4 วิธีหลักที่เหมาะกับความซับซ้อนต่างกัน — ไม่มีวิธีใดเหมาะกับทุกสถานการณ์** — 5-Why (ง่าย, เร็ว, เหมาะปัญหาสายเดียว), Fishbone/Ishikawa (ปานกลาง, เหมาะปัญหาหลายสาเหตุ, ใช้ 6M framework: Man/Machine/Material/Method/Measurement/Environment), Fault Tree Analysis (ซับซ้อน, เชิงปริมาณ, ใช้ Boolean logic, เหมาะ safety-critical), และ FMEA (เชิงรุก, ทำก่อนความล้มเหลว, RPN = Severity × Occurrence × Detection) [^12][^13] สำหรับสินทรัพย์ Critical ใน process industry แนะนำใช้ RCFA (Root Cause Failure Analysis) ซึ่งผสม FTA กับ barrier analysis [^12]

6. **KM ปิด feedback loop ด้วยการแปลง RCA findings เป็นความรู้ที่นำไปใช้ได้ทั้งองค์กร** — Knowledge Management ในบริบท RE หมายถึงกระบวนการจัดเก็บ (Capture), จัดระเบียบ (Organize), และเผยแพร่ (Distribute) ผลลัพธ์ RCA ไปยังสินทรัพย์ที่คล้ายกันทั่วโรงงาน องค์กรชั้นนำใช้ทั้ง FMEA ในช่วงออกแบบและติดตั้ง และ RCA เมื่อเกิดความล้มเหลว ผลลัพธ์จาก RCA จะอัปเดต FMEA library, PM task list, training materials, และ spare parts list เพื่อป้องกันการเกิดซ้ำในสินทรัพย์เดียวกันและสินทรัพย์ fleet เดียวกัน [^14]

7. **ASO ใช้ Monte Carlo simulation เพื่อหาจุดสมดุลระหว่าง Risk กับ Cost อย่างเป็นวิทยาศาสตร์** — Asset Strategy Optimization ขยายความสามารถของ ASM ด้วยการเพิ่ม quantitative modeling โดย GE Vernova APM Meridium module ASO ใช้ Monte Carlo simulation กำหนด Time-to-Failure (TTF) และ Time-to-Repair (TTR) สำหรับแต่ละ action ใน strategy และเปรียบเทียบ Active vs Proposed scenarios เพื่อหา optimal balance ระหว่าง risk mitigation กับ cost of maintenance action [^15][^16] ผลลัพธ์ ASO จะส่งกลับไปปรับ ASM เพื่อสร้าง closed-loop continuous improvement

8. **Digital Twin + IIoT + ML กำลังเปลี่ยนรูปแบบ RE จากเชิงรับเป็นเชิงรุกอย่างสมบูรณ์** — ในปี 2025-2026 โรงงานชั้นนำรวม sensor data จาก IIoT เข้ากับ Digital Twin เพื่อรัน ML models (LSTM, Random Forest, Autoencoders) สำหรับ Remaining Useful Life (RUL) prediction [^17] Edge computing ทำให้ประมวลผลข้อมูล vibration/temperature ได้ใน <10 milliseconds โดยไม่ต้องส่งไป cloud [^17] ขั้นถัดไปคือ AI-driven Prescriptive Analytics ที่แนะนำ action อัตโนมัติ ไม่ใช่แค่แจ้งเตือน [^18]

---

## Background / context

### Reliability Engineering คืออะไร?

Reliability Engineering (RE) คือสาขาวิศวกรรมที่มุ่งเน้นการทำให้สินทรัพย์ทางกายภาพ (เครื่องจักร, อุปกรณ์, ระบบ) ทำงานได้ตามฟังก์ชันที่ต้องการ ตามระยะเวลาที่กำหนด ภายใต้เงื่อนไขการใช้งานจริง โดยไม่เกิดความล้มเหลวที่ไม่ได้วางแผนไว้ [^19] บทบาทหลักของ Reliability Engineer คือการป้องกันความล้มเหลว (Strategic/Proactive) ในขณะที่ Maintenance Engineer มีบทบาทกู้คืนสินทรัพย์เมื่อเกิดความล้มเหลว (Tactical/Reactive) — ความสัมพันธ์นี้เปรียบได้กับ "วิศวกรดับเพลิง (Fire Marshal)" กับ "นักดับเพลิง (Firefighter)" [^19]

### กรอบงาน ISO 55000 และมาตรฐานสากล

ISO 55000 (2014, ปรับปรุง 2024) คือมาตรฐานนานาชาติด้าน Asset Management ซึ่งประกอบด้วย 3 มาตรฐาน: ISO 55000 (Overview, principles, terminology), ISO 55001 (Requirements), และ ISO 55002 (Implementation guidelines) [^20] มาตรฐานนี้กำหนดหลักการ 4 ประการหลักของ Asset Management ได้แก่ Value (คุณค่า), Alignment (การจัดแนว), Leadership (ผู้นำ), และ Assurance (การรับประกัน) [^20] SMRP (Society for Maintenance & Reliability Professionals) ออก Body of Knowledge ที่ครอบคลุม 5 เสาหลัก: Business & Management, Equipment Reliability, Manufacturing Process Reliability, Organization & Leadership, และ Work Management และออก CMRP (Certified Maintenance & Reliability Professional) certification [^21]

### บริบท APM ในอุตสาหกรรมกระบวนการ

Asset Performance Management (APM) คือกรอบงานที่รวมทุกกิจกรรมด้านการบำรุงรักษาและความน่าเชื่อถือเข้าไว้ใน data-driven loop เดียว [^1] ต้นทุนหยุดเครื่องที่ไม่ได้วางแผนในอุตสาหกรรมอยู่ที่เฉลี่ย 532,000 ดอลลาร์ต่อชั่วโมงในปี 2024 [^9] การเปลี่ยนจาก reactive maintenance (รับมือหลังเสีย) เป็น proactive/predictive maintenance สามารถลด maintenance cost ได้ 10-40% และลด unplanned downtime ได้ 25-50% [^4]

### บริบทในอุตสาหกรรมไทย

ในประเทศไทย อุตสาหกรรมปิโตรเคมี, โรงไฟฟ้าพลังความร้อนร่วม (ผลิตไฟฟ้ามากกว่า 40% ของประเทศ), โรงกลั่นน้ำมัน และโรงงานการผลิต ต่างเป็นกลุ่มที่ใช้หลักการ Reliability Engineering อย่างเข้มข้น ผู้ให้บริการ RE ในประเทศไทย เช่น reliaSPACE (จังหวัดระยอง) ให้บริการวิเคราะห์การสั่นสะเทือน (Vibration Analysis), การให้คำปรึกษาด้านความน่าเชื่อถือของเครื่องจักร (Machine Reliability Consulting), และ Predictive Maintenance Service [^31] กรอบงาน APM และหลักการ "การวางแผนการบำรุงรักษา" (Maintenance Planning) ที่ดีช่วยลดต้นทุนปฏิบัติการในอุตสาหกรรมไทยได้อย่างมีนัยสำคัญ [^31]

---

## Deep dive

### Q1: Asset Criticality Analysis (ACA) — วิเคราะห์ความสำคัญสินทรัพย์

**คำนิยาม:** ACA คือกระบวนการประเมินและจัดลำดับความสำคัญของสินทรัพย์โดยพิจารณาจากความเสี่ยงและผลกระทบที่จะเกิดขึ้นหากสินทรัพย์นั้นล้มเหลว [^2]

**สูตรคำนวณ:**
```
Criticality Score = Likelihood of Failure × Consequence of Failure
```
หรือในรูป FMEA:
```
RPN = Severity × Occurrence × Detection (แต่ละค่า 1-10)
```

**ปัจจัยที่ใช้ประเมิน Consequence (ผลกระทบ) ครอบคลุม 5 มิติ:**
- **Safety Impact** — ความเสี่ยงต่อชีวิตและสุขภาพ
- **Environmental Impact** — ผลกระทบต่อสิ่งแวดล้อม
- **Production Impact** — การสูญเสียกำลังการผลิต
- **Financial Impact** — ต้นทุนซ่อมแซมและรายได้ที่เสียไป
- **Regulatory/Reputation Impact** — การละเมิดกฎระเบียบและชื่อเสียง

**กระบวนการ 9 ขั้นตอน:**
1. กำหนดขอบเขต (Scope Definition)
2. รวบรวมข้อมูลสินทรัพย์ (Asset Inventory Review)
3. ประเมินความเสี่ยงแต่ละสินทรัพย์ (Risk Evaluation)
4. ตรวจสอบกับข้อมูลประวัติ (Validation vs Historical Data)
5. ประเมินกลยุทธ์ลดความเสี่ยงที่มีอยู่
6. บันทึก Governance และผู้รับผิดชอบ
7. สัมภาษณ์ Stakeholders
8. จัดทำรายงานและ Criticality Registry
9. ติดตาม Continuous Improvement [^2]

**Output ของ ACA:**
- Criticality Register (ทะเบียนสินทรัพย์พร้อม criticality tier: Critical / Semi-Critical / Non-Critical)
- Input สู่ ASM เพื่อกำหนดกลยุทธ์ที่เหมาะสม
- Input สู่ AHM เพื่อกำหนด monitoring frequency [^3][^28]

---

### Q2: Asset Strategy Management (ASM) — กำหนดกลยุทธ์บำรุงรักษา

**คำนิยาม:** ASM คือกระบวนการกำหนดและบริหารจัดการแผนดูแลสินทรัพย์ (Asset Care Plan) ให้สอดคล้องกับบริบทการดำเนินงาน สภาพสินทรัพย์ และระดับความสำคัญ [^6]

**กลยุทธ์การบำรุงรักษา 4+1 ประเภทหลัก:**

| กลยุทธ์ | คำอธิบาย | เมื่อใดควรใช้ | ข้อดี | ข้อเสีย |
|---|---|---|---|---|
| Run-to-Failure (RTF/Reactive) | ปล่อยให้เสียก่อนค่อยซ่อม | สินทรัพย์ Non-Critical, มี redundancy, ซ่อมง่าย | ต้นทุน PM ต่ำ | ไม่ควบคุมเวลาเสีย |
| Time-Based Preventive (TBM) | ซ่อมบำรุงตามตารางเวลา | สินทรัพย์ Semi-Critical, failure mode ตามอายุ | วางแผนได้, ลด downtime | อาจ over-maintain |
| Condition-Based (CBM) | ซ่อมตามสภาพที่ตรวจพบ | มี P-F interval พอซ่อมได้ทัน | ลดงานที่ไม่จำเป็น | ต้องการ sensor/data |
| Predictive (PdM) | คาดการณ์ล่วงหน้าด้วย analytics | Critical, failure mode มีสัญญาณล่วงหน้า | ลด downtime สูงสุด | ลงทุนสูง, ต้องมีข้อมูล |
| Reliability-Centered (RCM) | วิเคราะห์ failure mode ทุกตัวอย่างเป็นระบบ | ทุกสินทรัพย์ Critical ใหม่/ที่มีปัญหาซ้ำ | ครอบคลุมทุก failure mode | ใช้เวลาและทรัพยากรสูง |

**เครื่องมือหลักใน ASM:**
- **FMEA (Failure Modes and Effects Analysis)**: ระบุ failure mode, effect, และ RPN
- **RCM (Reliability-Centered Maintenance)**: วิเคราะห์ระดับระบบเพื่อกำหนด strategy ที่ดีที่สุด
- **P-F Interval Analysis**: ระยะเวลาระหว่างจุดที่เริ่มเสื่อม (P) ถึงจุดที่ล้มเหลว (F) กำหนดว่า CBM/PdM ทำได้หรือไม่ [^5]

**Output ของ ASM:**
- Maintenance Plans ใน CMMS/EAM
- Task Lists และ Job Procedures
- Spare Parts Recommendations
- Input สู่ AHM (กำหนด monitoring parameters) และ WEM (กำหนด work scope) [^6]

---

### Q3: Asset Health Management (AHM) — ติดตามสุขภาพสินทรัพย์

**คำนิยาม:** AHM คือกลยุทธ์เชิงรุกที่ใช้การตรวจสอบสภาพอย่างต่อเนื่องเพื่อประเมินสุขภาพสินทรัพย์ ตรวจจับการเสื่อมสภาพล่วงหน้า และส่งมอบข้อมูลสำหรับการตัดสินใจบำรุงรักษา [^7]

**เทคนิค Condition Monitoring หลัก:**

| เทคนิค | ตรวจพบอะไร | อุปกรณ์ที่ใช้ |
|---|---|---|
| Vibration Analysis | ความไม่สมดุล, bearing wear, misalignment | Accelerometers, velocity sensors |
| Thermography (IR) | ความร้อนผิดปกติ, electrical faults, insulation | Infrared cameras |
| Oil Analysis | Wear debris, contamination, lubricant degradation | Lab kits, online sensors |
| Ultrasonic Detection | Subsurface cracks, steam leaks, bearing defects | Ultrasonic transducers |
| Electrical Signature Analysis | Motor degradation, stator/rotor faults | Current clamps, power analyzers |
| Visual Inspection | Surface defects, corrosion, leaks | Fixed cameras, drones, robotics |

**Asset Health Index (AHI) — การคำนวณ:**

GE Vernova APM Health คำนวณ Health Score อัตโนมัติ (โดยทั่วไปทุกคืน) โดยรวบรวมจาก:
- ข้อมูล Operator Rounds
- Time-series sensor measurements
- Predictive diagnostic alerts
- Work recommendations
- ประวัติ PM/CM [^8]

Health Score 100 = สมบูรณ์, เมื่อ Score ต่ำกว่า threshold ที่กำหนด (เช่น <60/100) ระบบส่ง alert และสร้าง Work Order อัตโนมัติใน EAM [^8]

**Output ของ AHM:**
- Health Score dashboard รายสินทรัพย์
- Condition alerts และ prioritized maintenance recommendations
- Work Order requests ส่งไปยัง WEM
- Data feed สู่ ASO สำหรับ strategy optimization [^8]

---

### Q4: Work Execution Management (WEM) — บริหารการปฏิบัติงาน

**คำนิยาม:** WEM คือกระบวนการแปลงงานที่ถูกระบุจาก RE และ AHM ให้เป็นงานที่ถูกปฏิบัติจริง มีการวางแผน จัดตาราง และบันทึกผลอย่างครบถ้วน [^10]

**วงจรชีวิต Work Order (Work Order Lifecycle):**

```
[AHM Alert / PM Schedule / Operator Request]
         ↓
  1. Identify Need (ระบุความต้องการ)
         ↓
  2. Approve Work Order (อนุมัติ)
         ↓
  3. Plan Work (วางแผน: scope, parts, crew, tools)
         ↓
  4. Schedule Work (จัดตาราง: time window, resource allocation)
         ↓
  5. Execute Work (ปฏิบัติงาน)
         ↓
  6. Close Work Order (ปิดงาน + บันทึก Actuals: ชั่วโมงทำงาน, parts used, findings)
         ↓
  [Actuals feed back → AHM update, ASO data, RCA trigger if failure]
```

**องค์ประกอบสำคัญของ WEM:**
- **Planning**: เตรียม scope, parts, procedures ก่อน technician รับงาน
- **Scheduling**: จัดสรร time window, resource, และ shutdown windows
- **MRO Inventory**: บริหาร spare parts ให้มี service level 95-97% [^11]
- **CMMS/EAM**: ระบบที่รองรับ workflow ทั้งหมด

**ประสิทธิภาพที่ได้จาก Proactive WEM:**
- ต้นทุนงาน Proactive = 1/4 ถึง 1/2 ของงาน Reactive [^11]
- ประสิทธิภาพแรงงาน (Wrench Time) เพิ่มจาก <30% เป็น ~60% [^11]
- เป้าหมาย: งานที่ถูก Plan & Schedule ≥ 80% ของงานทั้งหมดต่อสัปดาห์ [^11]

---

### Q5: Root Cause Analysis (RCA) — วิเคราะห์สาเหตุรากเหง้า

**คำนิยาม:** RCA คือกระบวนการเชิงระบบในการระบุสาเหตุรากเหง้าของความล้มเหลว มุ่งแก้ไขที่ต้นเหตุ ไม่ใช่แค่อาการ เพื่อป้องกันการเกิดซ้ำ [^12]

**4 วิธีหลักของ RCA เปรียบเทียบ:**

| ปัจจัย | 5-Why | Fishbone (Ishikawa) | Fault Tree Analysis (FTA) | FMEA |
|---|---|---|---|---|
| ความซับซ้อน | ต่ำ-ปานกลาง | ปานกลาง-สูง | สูง | ใช้ก่อนเกิดความล้มเหลว |
| เวลาที่ใช้ | ชั่วโมง-วัน | วัน-สัปดาห์ | สัปดาห์-เดือน | ก่อน commissioning |
| ความเชี่ยวชาญ | เบื้องต้น | ปานกลาง | ขั้นสูง | ปานกลาง-สูง |
| Output | สายเหตุ linear | แผนผัง visual | โครงสร้าง logic + probability | RPN + action list |
| เหมาะกับ | ปัญหา operational ทั่วไป | ปัญหาหลายสาเหตุ | Safety-critical, regulated | Risk prevention |

**กระบวนการ RCA (RCFA — Root Cause Failure Analysis) ใน Process Industry:**
1. **Define** — บันทึกความล้มเหลวอย่างชัดเจน (What, When, Where, How)
2. **Collect Data** — รวบรวมข้อมูล: sensor data, maintenance history, operator logs, inspection photos
3. **Analyze** — เลือกวิธีที่เหมาะสม (5-Why / Fishbone / FTA) และวิเคราะห์
4. **Identify Root Cause** — แยกแยะ Physical Cause, Human Cause, และ Latent/System Cause
5. **Develop Corrective Actions** — แก้ที่ระดับ root cause ไม่ใช่แค่ symptom
6. **Implement & Verify** — ติดตั้งแก้ไขและยืนยันประสิทธิผล
7. **Document & Share** — บันทึกเข้า KM system [^12][^13]

---

### Q6: Knowledge Management (KM) — จัดการความรู้เพื่อป้องกันความล้มเหลวซ้ำ

**คำนิยาม:** KM ใน Reliability Engineering คือระบบและกระบวนการในการจับ (Capture), จัดระเบียบ (Organize), และเผยแพร่ (Distribute) บทเรียนและความรู้จาก RCA ไปยังสินทรัพย์ที่คล้ายกันทั่วองค์กร เพื่อป้องกันความล้มเหลวซ้ำ [^14]

**องค์ประกอบของ KM ใน RE:**
- **Failure Library / FMEA Database**: คลังข้อมูล failure modes ที่เคยเกิดขึ้น พร้อม root cause และ corrective action
- **Lessons Learned Repository**: บทเรียนสรุปจาก RCA ที่สามารถค้นหาและนำไปใช้ได้
- **Best Practice Documents**: ขั้นตอนการปฏิบัติที่ดีที่สุดสำหรับการซ่อมบำรุงสินทรัพย์แต่ละประเภท
- **Training Materials**: เนื้อหาฝึกอบรมที่อัปเดตตาม RCA findings ใหม่ๆ

**กระบวนการ KM Loop:**
```
RCA Findings
   ↓
Update FMEA Library
   ↓
Update PM Task Lists / Maintenance Procedures
   ↓
Update Spare Parts Recommendations
   ↓
Train Personnel
   ↓
Apply to Similar Assets in Fleet
   ↓
Monitor for Recurrence Prevention
```

**ผลที่ได้จาก KM ที่มีประสิทธิภาพ:** เมื่อผลลัพธ์ RCA ถูก review, implement, audit และปรับปรุงต่อเนื่อง กระบวนการนี้จะกลายเป็น self-sustaining institutional memory ที่ "บทเรียนจากความล้มเหลวหนึ่งช่วยป้องกันความล้มเหลวอื่นอีก 10 รายการ" [^14]

---

### Q7: Asset Strategy Optimization (ASO) — ปรับปรุงกลยุทธ์ด้วยข้อมูล

**คำนิยาม:** ASO ขยายความสามารถของ ASM โดยเพิ่ม advanced quantitative modeling สำหรับหาจุดสมดุลที่เหมาะสมระหว่าง cost of maintenance กับ risk of failure [^15][^16]

**ความสามารถหลักของ ASO (GE APM Meridium):**
- **Monte Carlo Simulation**: จำลองสถานการณ์หลายพันครั้งโดยใช้การแจกแจงความน่าจะเป็นของ TTF (Time to Failure) และ TTR (Time to Repair)
- **Active vs Proposed Scenario Comparison**: เปรียบเทียบกลยุทธ์ปัจจุบันกับกลยุทธ์ที่เสนอในเชิงตัวเลข
- **Resource Optimization**: กำหนดทรัพยากร (spare parts, manpower) ที่ต้องการตามกลยุทธ์
- **Closed-loop Cycle**: ผลลัพธ์ ASO ส่งกลับไปปรับ ASM โดยอัตโนมัติ [^15]

**Input ที่ ASO ต้องการ:**
- AHM data: ข้อมูลสุขภาพสินทรัพย์, failure alerts, degradation trends
- WEM actuals: ชั่วโมงซ่อมจริง, cost จริง, parts used จริง
- RCA/KM: root cause data, updated failure distributions

**Output ของ ASO:**
- Optimized maintenance intervals
- Recommended strategy changes (update to ASM)
- Resource planning recommendations
- Risk vs Cost curves [^16]

---

### Q8: APM Loop — ความเชื่อมโยงระหว่างทุกขั้นตอน

**การไหลของข้อมูลในวงจร APM:**

```
┌─────────────────────────────────────────────────────────────┐
│                    APM LOOP                                  │
│                                                             │
│  [1] ACA ──────────────────────────────────────────────┐   │
│   Risk Score, Criticality Tier                          │   │
│        │                                               │   │
│        ▼                                               │   │
│  [2] ASM ──────────────── Input: ACA Tier             │   │
│   Maintenance Strategy, Task Lists                     │   │
│        │                                               │   │
│        ▼                                               │   │
│  [3] AHM ──────────────── Input: ASM monitoring params│   │
│   Health Score, Alerts, Degradation trends             │   │
│        │                                               │   │
│        ▼                                               │   │
│  [4] WEM ──────────────── Input: AHM alerts + ASM plan│   │
│   Work Orders, Actuals, Labor/Parts records            │   │
│        │                  ▲                            │   │
│        │                  └─── WEM Actuals → AHM update│  │
│        ▼                                               │   │
│  [5] RCA ──────────────── Triggered by WEM failure     │   │
│   Root Cause Report, Corrective Actions                │   │
│        │                                               │   │
│        ▼                                               │   │
│  [6] KM ───────────────── Input: RCA findings          │   │
│   FMEA updates, Lessons Learned, PM revisions          │   │
│        │                                               │   │
│        ▼                                               │   │
│  [7] ASO ──────────────── Input: AHM + WEM + KM data  │   │
│   Optimized intervals, Resource plans                  │   │
│        │                                               │   │
│        └───────────────────────────────────────────────┘   │
│              Update ASM Strategy (New cycle begins)         │
└─────────────────────────────────────────────────────────────┘
```

**Input และ Output ของแต่ละขั้นตอน:**

| ขั้นตอน | Input | Output | ส่งไปยัง |
|---|---|---|---|
| ACA | Asset inventory, historical failure data, business impact data | Criticality Register, Risk scores | ASM, AHM |
| ASM | ACA tier, failure modes (FMEA/RCM), P-F intervals | Maintenance plans, task lists, intervals | AHM (monitoring params), WEM (work scope) |
| AHM | Sensor data, operator rounds, maintenance history | Health Score, alerts, recommendations | WEM (work orders), ASO (trend data) |
| WEM | AHM alerts, ASM plans, MRO inventory | Completed work orders, actuals (time/cost/parts) | AHM (update history), RCA (failure details), ASO |
| RCA | Failed asset data, WEM actuals, sensor data, inspection findings | Root cause report, corrective actions | KM (capture learning), ASM (update strategy) |
| KM | RCA reports, RCA corrective actions | Updated FMEA, PM procedures, training, lessons | ASO (enhanced failure models), ASM (task updates) |
| ASO | AHM trends, WEM actuals, KM/FMEA data | Optimized strategy, updated intervals, resource plan | ASM (strategy revision) → restart loop |

ความท้าทายหลักในการนำ APM Loop มาใช้คือการเชื่อมต่อข้อมูลระหว่างระบบที่มักแยกจากกัน (silos) ได้แก่ CMMS/EAM, process historian, condition monitoring platforms และ analytics tools [^1][^25]

---

### Q9: KPIs หลักของ Reliability Engineering

**สูตรและค่าอ้างอิงอุตสาหกรรม:**

| KPI | สูตร | ความหมาย | Benchmark อุตสาหกรรม | ระบุสุขภาพของ |
|---|---|---|---|---|
| MTBF | Total Operating Time / # Failures | เวลาเฉลี่ยระหว่างความล้มเหลว | Manufacturing: 200–2,000 hrs | AHM, ASM |
| MTTR | Total Repair Time / # Repairs | เวลาเฉลี่ยในการซ่อม | Manufacturing: 2–8 hrs | WEM |
| Availability | MTBF / (MTBF + MTTR) | % เวลาที่สินทรัพย์พร้อมใช้งาน | ≥ 95% (critical assets) | AHM, WEM |
| OEE | Availability × Performance × Quality | ประสิทธิผลรวมของอุปกรณ์ | World-class: 85%, ค่าเฉลี่ย: ~60% | WEM, ASM |
| COUR | (ต้นทุน downtime + ต้นทุน maintenance) | ต้นทุนความไม่น่าเชื่อถือรวม | $532K/hr (unplanned, avg 2024) | ทุกสาขา |
| PM Compliance | PM งานที่ทำได้ / PM งานที่วางแผน × 100% | % งาน PM ที่ทำได้ตามแผน | ≥ 90% | ASM, WEM |
| Schedule Adherence | งานที่ทำตาม schedule / งานทั้งหมด × 100% | % งานที่ทำตามตารางที่วาง | ≥ 90% | WEM |
| Wrench Time | เวลาปฏิบัติงานจริง / เวลาทำงานทั้งหมด | % เวลาที่ช่างทำงานจริง | Proactive: ~60% | WEM |
| Failure Rate (λ) | # Failures / Total Operating Time | อัตราความล้มเหลวต่อหน่วยเวลา | — | AHM, ASM |

**สูตรขั้นสูง:**
- **Weibull Reliability**: R(t) = e^−(t/η)^β (β = shape, η = characteristic life)
- **System Reliability (Series)**: Rs = R₁ × R₂ × ... × Rn
- **System Reliability (Parallel)**: Rs = 1 − (1−R₁)(1−R₂)...(1−Rn)
- **FMEA RPN**: RPN = Severity × Occurrence × Detection (1-10 แต่ละตัว) [^22]

---

### Q10: ซอฟต์แวร์ APM ที่นิยมใช้ในอุตสาหกรรม

**เปรียบเทียบ 6 แพลตฟอร์มหลัก:**

| แพลตฟอร์ม | จุดแข็ง | อุตสาหกรรมที่เหมาะ | ครอบคลุม Module |
|---|---|---|---|
| **GE Vernova APM** (Meridium) | OEM expertise, module set ครบที่สุด, install base ใหญ่ที่สุด | Power generation, heavy industry | ACA, ASM (RCM/FMEA), AHM (condition monitoring), RCA, ASO, Integrity Management |
| **IBM Maximo Application Suite** | รวม EAM + APM ในแพลตฟอร์มเดียว, AI-driven (Maximo Predict, Monitor, Visual Inspection) | Multi-industry enterprise | Work Management (EAM), Health monitoring, PdM (AI), IoT ingestion |
| **SAP APM** | Native integration กับ S/4HANA, asset health → finance workflow ทันที | SAP ecosystem users | Asset health monitoring, connected to SAP PM (WEM/EAM) |
| **AVEVA APM** | Deep integration กับ SCADA, process historians | Oil & gas, chemicals, process industry | Condition monitoring, anomaly detection |
| **AspenTech Mtell** | Equipment-agnostic ML, learns from your data, RUL prediction | Process industry (refining, chemicals) | PdM, anomaly detection, RUL |
| **Bentley AssetWise** | Digital twin จาก design ถึง operation, infrastructure assets | Infrastructure, utilities | Condition assessment, lifecycle management |

**ความแตกต่าง CMMS vs EAM vs APM:**
- **CMMS** (Computerized Maintenance Management System): บริหาร maintenance operations — work orders, schedules, inventory
- **EAM** (Enterprise Asset Management): ครอบคลุม CMMS + financials, HR, procurement ระดับองค์กร
- **APM**: ขยาย EAM ด้วย analytics, condition monitoring, strategy optimization — บอกว่าควรทำอะไร เมื่อไหร่ และทำไม [^23]

---

### Q11: บทบาทในองค์กร — Reliability Engineer, Maintenance Engineer, Asset Manager

**เปรียบเทียบบทบาท 3 ตำแหน่ง:**

| มิติ | Reliability Engineer | Maintenance Engineer | Asset Manager |
|---|---|---|---|
| เป้าหมาย | ป้องกันความล้มเหลว (Prevention) | กู้คืนจากความล้มเหลว (Restoration) | ดูแลสินทรัพย์ตลอดวงจรชีวิต (Lifecycle) |
| ลักษณะงาน | Strategic / Proactive | Tactical / Reactive | Strategic + Financial |
| กิจกรรมหลัก | RCA, FMEA, RCM analysis, KPI monitoring, strategy development | Work order execution, repair procedures, outage management | ACA, budget allocation, ISO 55000 compliance, Capex/Opex decisions |
| Focus | Asset-level (machine/production line) | Discipline-level (mechanical, electrical) | Portfolio-level (all assets) |
| Analogy | วิศวกรดับเพลิง (Fire Marshal) | นักดับเพลิง (Firefighter) | ผู้อำนวยการสถานีดับเพลิง |
| Certification | CMRP (SMRP), CRE (ASQ) | — | IAM Certificate, ISO 55000 |

**ความทับซ้อน:** Reliability Engineer และ Maintenance Engineer ทำงานร่วมกันอย่างใกล้ชิด — Reliability Engineer วิเคราะห์และกำหนด strategy, Maintenance Engineer นำไปปฏิบัติและรายงาน Actuals กลับมา Asset Manager ตัดสินใจระดับ portfolio และงบประมาณโดยอิงผล KPI จากทั้งสองฝ่าย [^19][^24]

---

### Q12: แนวโน้มใหม่ที่กำลังเปลี่ยนวงการ Reliability Engineering

**1. Digital Twin สำหรับ Predictive Maintenance:**
Digital Twin คือแบบจำลองเสมือนของสินทรัพย์ที่ sync กับ sensor data แบบ real-time เพื่อ simulate พฤติกรรมและคาดการณ์ failure ก่อนเกิดจริง [^17] งานวิจัยล่าสุด (2025-2026) แสดงให้เห็นว่า DT + ML สามารถประมาณ RUL (Remaining Useful Life) ได้แม่นยำขึ้นกว่าวิธีดั้งเดิมอย่างมีนัยสำคัญ [^18][^27]

**2. IIoT (Industrial Internet of Things):**
IIoT sensors รุ่นใหม่มีต้นทุนต่ำลงมากและ deploy ได้ง่ายขึ้น ทำให้สามารถติดตั้งบน Non-Critical assets ได้มากขึ้น ข้อมูลจาก IIoT ผ่าน process historian เข้าสู่ AHM platform โดยตรง [^17]

**3. ML Algorithms สำหรับ PdM:**
- **LSTM (Long Short-Term Memory)**: เหมาะกับ time-series degradation patterns
- **Random Forest**: Multi-classification สำหรับระบุ fault type
- **Autoencoders / Isolation Forest**: Anomaly detection โดยไม่ต้องการ labelled failure data
- **Hybrid Models (LSTM-ANN-GA)**: จับ temporal dependencies ซับซ้อน [^17]

**4. Edge Computing:**
ML models ย้ายจาก cloud มาทำงานบน edge hardware ในโรงงาน ประมวลผลข้อมูล vibration/temperature ใน <10 milliseconds ลด latency และ bandwidth ที่ต้องการ [^17]

**5. AI-driven Prescriptive Analytics:**
ขั้นถัดจาก Predictive (คาดการณ์) คือ Prescriptive (แนะนำ action) ที่ระบบ AI จะแนะนำว่าควรทำ maintenance อะไร เมื่อไหร่ และอย่างไร แบบอัตโนมัติ — GE Vernova APM เรียกสิ่งนี้ว่า "Generative AI-driven prescriptive analytics" [^18]

**6. Workflow Automation Integration:**
โรงงานชั้นนำในปี 2026 เชื่อม IIoT alerts + SCADA alarms + Digital Twin forecasts เข้ากับ CMMS/EAM เพื่อสร้าง Work Orders อัตโนมัติ — นี่คือ differentiator ระหว่าง top quartile กับ average plants [^17]

---

## Data / numbers

| Metric | Value | Year | Source |
|---|---|---|---|
| Average unplanned downtime cost | $532,000/hour | 2024 | [^9] |
| World-class OEE benchmark | 85% | benchmark (undated, widely cited) | [^9] |
| Industry average OEE | ~60% | benchmark (undated, widely cited) | [^9] |
| Target PM Compliance (best practice) | ≥ 90% | benchmark (undated) | [^9] |
| PM Compliance loss cost | ~$80,000/year per % point lost (mid-size plant) | benchmark (undated) | [^9] |
| MRO as % of total maintenance budget | 40–60% | benchmark (undated) | [^11] |
| MRO Service Level target | 95–97% part availability | benchmark (undated) | [^11] |
| Proactive vs Reactive work cost ratio | 1:2 to 1:4 (Proactive cheaper) | benchmark (undated) | [^11] |
| Wrench time improvement (reactive→planned) | <30% → ~60% | benchmark (undated) | [^11] |
| MTBF benchmark — Manufacturing | 200–2,000 hrs | benchmark (undated) | [^22] |
| MTTR benchmark — Manufacturing | 2–8 hrs | benchmark (undated) | [^22] |
| MTBF benchmark — Power Plants | 500–1,500 hrs | benchmark (undated) | [^22] |
| MTTR benchmark — Power Plants | 8–24 hrs | benchmark (undated) | [^22] |
| Availability — Critical automotive assets | 95–98% | benchmark (undated) | [^22] |
| PdM cost reduction potential vs reactive | 10–40% maintenance cost reduction | benchmark (undated) | [^4] |
| Unplanned downtime reduction with PdM | 25–50% | benchmark (undated) | [^4] |

---

## Worked example(s)

### กรณีศึกษา: Centrifugal Pump Failure ที่โรงกลั่นปิโตรเคมี → APM Loop ครบวงจร

**Background:** โรงกลั่นมี centrifugal pumps 120 ตัวในกระบวนการผลิต

**ขั้นที่ 1 — ACA:**
ทีมวิเคราะห์ criticality พบว่า Pump P-101 (feed pump หลัก) มี Criticality Score สูงสุด เพราะ:
- Consequence: หยุดผลิตทั้ง unit ถ้าเสีย (~$400K/hr production loss)
- Likelihood: อยู่ในสภาพแวดล้อมกัดกร่อนสูง, run 24/7
- ผลลัพธ์: จัดอยู่ใน **Tier 1 Critical**

**ขั้นที่ 2 — ASM:**
Reliability Engineer กำหนด strategy สำหรับ Pump P-101:
- PdM: ติดตั้ง vibration sensor + online oil analysis
- PM: เปลี่ยน bearing ทุก 18 เดือน (time-based)
- Spare: จัดเก็บ rotating element สำรองในคลัง

**ขั้นที่ 3 — AHM:**
ระบบ AHM ตรวจพบว่าความถี่การสั่นสะเทือนของ bearing เพิ่มขึ้น 3 เท่าจาก baseline
Health Score: ลดจาก 87/100 → 52/100 ภายใน 2 สัปดาห์
ระบบสร้าง Work Order อัตโนมัติ: "Inspect bearing P-101 — Priority High"

**ขั้นที่ 4 — WEM:**
Work Order ถูก Plan: กำหนดใช้ช่วง scheduled shutdown ใน 10 วัน, Pre-order SKF bearing 3-lug design
**Outcome:** Pump เสียก่อนถึงวันซ่อม เพราะ degradation เร็วกว่าที่ model คาดการณ์

**ขั้นที่ 5 — RCA (5-Why + Fishbone):**
1. ทำไม Bearing จึงเสียเร็วกว่ากำหนด? → มีการสึกหรอผิดปกติ
2. ทำไมถึงสึกหรอผิดปกติ? → การหล่อลื่นไม่เพียงพอ
3. ทำไมการหล่อลื่นไม่เพียงพอ? → ระยะเวลาเติมน้ำมันนานเกินไป
4. ทำไมระยะเวลาเติมน้ำมันถึงนานเกินไป? → Lubrication interval กำหนดตาม run-hours ไม่ใช่ vibration data
5. ทำไม interval ไม่ได้อิง vibration data? → **Strategy ใน ASM ไม่ได้อัปเดตเมื่อ install vibration sensor**

**Root Cause:** System cause — กระบวนการ ASM ไม่มี feedback loop จาก AHM ไปปรับ lubrication interval โดยอัตโนมัติ

**ขั้นที่ 6 — KM:**
บทเรียน: "สำหรับ assets ที่ใช้ PdM ร่วมกับ TBM, lubrication interval ต้องถูก trigger โดย condition data ไม่ใช่ fixed time-based schedule เพียงอย่างเดียว"
อัปเดต: แก้ไข PM procedure ของ Pump fleet ทั้ง 120 ตัว, อัปเดต FMEA

**ขั้นที่ 7 — ASO:**
Monte Carlo simulation บน failure data ของ pump fleet ทั้งหมดหลัง KM update:
- Optimal lubrication interval: ลดจาก 6 เดือน → 3 เดือน หรือ trigger เมื่อ vibration เกิน threshold
- ผลลัพธ์ที่คาดการณ์: อายุ bearing เพิ่มจาก 18 เดือน → 28 เดือน
- ประหยัดค่า bearing replacement และ downtime: ~$45,000/year/pump fleet

**ผลลัพธ์ ASO → อัปเดต ASM:** กลยุทธ์ใหม่สำหรับ centrifugal pump ทุกตัว ใช้ vibration-triggered lubrication + PdM monitoring แบบ dynamic interval

---

## Comparison / alternatives

### เปรียบเทียบกลยุทธ์การบำรุงรักษา (Maintenance Strategy Matrix)

| ลักษณะ | Reactive (RTF) | Preventive (TBM) | Condition-Based (CBM) | Predictive (PdM) |
|---|---|---|---|---|
| เวลาที่ทำ | หลังเสีย | ตามตาราง | เมื่อ sensor แจ้ง | คาดการณ์ล่วงหน้า |
| ต้นทุน maintenance | ต่ำ (ไม่มี PM) | ปานกลาง | ปานกลาง-สูง | สูง (setup) |
| ต้นทุน downtime | สูงมาก (unplanned) | ต่ำ | ต่ำมาก | ต่ำที่สุด |
| ต้องการข้อมูล | ไม่ต้องการ | น้อย | ปานกลาง | สูงมาก |
| เหมาะกับ ACA Tier | Non-Critical | Semi-Critical | Semi/Critical | Critical |
| ISO 55000 alignment | ต่ำ | ปานกลาง | สูง | สูงมาก |

---

## Open questions / limitations

1. **KPI Benchmarks อาจแตกต่างตามอุตสาหกรรม**: ค่า MTBF, MTTR, OEE ที่แสดงในตารางเป็นค่าอ้างอิงทั่วไป ค่าจริงขึ้นอยู่กับประเภทอุตสาหกรรม ชนิดสินทรัพย์ และสภาพแวดล้อม

2. **ASO ต้องการข้อมูลคุณภาพสูง**: Monte Carlo simulation ใน ASO มีความแม่นยำขึ้นอยู่กับคุณภาพของ failure history data — องค์กรที่ไม่มีระบบ CMMS/EAM ที่ดีอาจไม่สามารถใช้ ASO ได้อย่างมีประสิทธิภาพ

3. **Digital Twin ยังอยู่ในช่วง maturation**: แม้ว่าผลการวิจัยจะมีแนวโน้มดี แต่การ deploy Digital Twin ในสเกลใหญ่ยังมีความท้าทายด้าน data quality, model calibration, และ ROI justification

4. **คำย่อที่อาจสับสน**: AHM บางครั้งหมายถึง "Aircraft Health Monitoring" ในบริบท aviation, ASM อาจหมายถึง "Autonomous Surface Management" ในบริบทอื่น — เอกสารนี้ใช้นิยามในบริบท APM/RE ตลอด

5. **ซอฟต์แวร์มีการพัฒนาอย่างต่อเนื่อง**: Feature และ module ของ GE Vernova APM, IBM Maximo, SAP APM มีการอัปเดตบ่อย ข้อมูลในเอกสารนี้อ้างอิงจากข้อมูลปี 2025-2026

---

## Glossary

| คำศัพท์ | คำย่อ | คำนิยาม |
|---|---|---|
| Asset Performance Management | APM | กรอบงานรวมที่ครอบคลุม ACA, ASM, AHM, WEM, RCA, KM, ASO ใน closed-loop |
| Asset Criticality Analysis | ACA | การจัดลำดับความสำคัญสินทรัพย์ตาม Risk = Likelihood × Consequence |
| Asset Strategy Management | ASM | การกำหนดและบริหารกลยุทธ์การบำรุงรักษาสินทรัพย์ |
| Asset Health Management | AHM | การติดตามและประเมินสุขภาพสินทรัพย์ด้วย real-time condition monitoring |
| Asset Health Index | AHI | คะแนนสุขภาพรวมของสินทรัพย์ (0-100) |
| Work Execution Management | WEM | การบริหารวงจรชีวิต Work Order ตั้งแต่ระบุความต้องการถึงปิดงาน |
| Root Cause Analysis | RCA | กระบวนการระบุสาเหตุรากเหง้าของความล้มเหลวอย่างเป็นระบบ |
| Root Cause Failure Analysis | RCFA | RCA เฉพาะสำหรับความล้มเหลวของสินทรัพย์กายภาพในอุตสาหกรรม |
| Knowledge Management | KM | ระบบจัดเก็บและเผยแพร่บทเรียนจาก RCA ไปยังองค์กร |
| Asset Strategy Optimization | ASO | การปรับปรุงกลยุทธ์ด้วย quantitative modeling (Monte Carlo) |
| Failure Mode and Effects Analysis | FMEA | การวิเคราะห์ failure modes เชิงรุก ก่อนความล้มเหลวเกิดขึ้น |
| Reliability-Centered Maintenance | RCM | วิธีการ systematic เพื่อกำหนด maintenance requirements ที่ดีที่สุด |
| Mean Time Between Failures | MTBF | เวลาเฉลี่ยระหว่างความล้มเหลว = Total Operating Time / # Failures |
| Mean Time To Repair | MTTR | เวลาเฉลี่ยในการซ่อม = Total Repair Time / # Repairs |
| Overall Equipment Effectiveness | OEE | Availability × Performance × Quality; ค่า World-class = 85% |
| Cost of Unreliability | COUR | ต้นทุนรวมของความไม่น่าเชื่อถือ รวม downtime cost + maintenance cost |
| P-F Interval | — | ระยะเวลาระหว่างจุดเริ่มเสื่อม (Potential failure) ถึงจุดล้มเหลว (Functional failure) |
| Monte Carlo Simulation | — | การจำลองสถานการณ์หลายพันครั้งด้วย probability distributions |
| Remaining Useful Life | RUL | อายุการใช้งานที่คาดว่าเหลืออยู่ก่อนล้มเหลว |
| Digital Twin | DT | แบบจำลองเสมือนของสินทรัพย์ที่ sync กับ real-time sensor data |
| MRO | — | Maintenance, Repair and Operations — อะไหล่และวัสดุสำหรับบำรุงรักษา |
| Criticality Register | — | ทะเบียนสินทรัพย์ทั้งหมดพร้อม criticality tier และ risk score |
| Time to Failure | TTF | เวลาที่คาดว่าจะใช้ไปก่อนเกิดความล้มเหลว (ใช้ใน ASO modeling) |
| Time to Repair | TTR | เวลาที่คาดว่าจะใช้ในการซ่อม (ใช้ใน ASO modeling) |

---

*Research compiled by Ravi (Research Analyst, agent-newsroom) — 2026-06-23*
