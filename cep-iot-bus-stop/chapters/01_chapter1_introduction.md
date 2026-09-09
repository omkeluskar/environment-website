# CHAPTER 1 — INTRODUCTION

## 1.1 Background

Mumbai’s Brihanmumbai Electric Supply and Transport (BEST) undertaking moves lakhs of passengers daily. Depot-level hubs such as **Dindoshi Bus Depot** concentrate boarding demand for multiple routes, including **Route 326**. Published reporting has described Dindoshi as a high-throughput terminal: *The Hindu* (2017) noted a makeover context with Dindoshi on the order of **≈3,243 sq m** and **≈8,500 passengers/day**; *Times of India* (2016) reported Dindoshi among depots with very high daily footfall (**≈1.47 lakh** across reporting of bus-depot commuters); independent station summaries (e.g. bestpedia.in) cite **≈3,242.9 sq m** and **≈8,331 passengers/day**. Exact contemporaneous counts vary by source and year; the consistent takeaway is that Dindoshi is a **busy community transit node**, not a low-traffic stop.

Overcrowding at the **shelter / boarding edge** is different from depot-wide footfall. A typical Mumbai/MMRDA-type roadside shelter footprint is on the order of **≈16 sq m** (≈6.0 m × 2.7 m — **estimated**; the exact MMRDA shelter dimension was never verifiable for this project). The UK *Guide to Safety at Sports Grounds* (5th ed., 2008) treats **3–4 people/m²** as congested, with **4/m²** as an upper safe reference. Using **16 m² × 2.78 ≈ 45 people** yields density **≈2.78/m²**, conservatively inside the congested band. Therefore this project adopts **stop capacity = 45** as a **reasoned, conservative estimate — not a measured field survey of the exact shelter**.

Community members — students, workers, elderly passengers — experience this crowding first-hand. A low-cost IoT node that estimates boarding-edge pressure and warns operators before conditions become critical is a practical CEP contribution.

## 1.2 Problem Statement

At Dindoshi (serving BEST Route 326), operators and passengers lack a **local, real-time, low-cost indicator** of shelter overcrowding risk that combines:

1. **Passenger crossing count** from a physical sensor,
2. **Weather stress** (rain increases waiting discomfort and clustering),
3. **Heat stress** (Mumbai summers), and
4. **Rush-hour timing**.

Without such a signal, crowding is noticed only after it becomes severe. Camera-based Automatic Passenger Counting (APC) systems exist in literature but raise cost, privacy, and maintenance barriers for a student CEP deployment. The problem addressed here is:

> **Design and demonstrate an ESP32 + ToF + DHT22 IoT system, with Blynk Cloud, Open-Meteo weather, Random Forest–assisted risk scoring, Telegram alerts, and CSV logging, to predict overcrowding risk at a public bus stop with transparent thresholds and honest limitations.**

## 1.3 Objectives

1. Build a hardware prototype on **ESP32 DoIT DevKit V1** (3.3 V rail) with **VL53L0X** (I2C: GPIO21 SDA / GPIO22 SCL) and **DHT22** (GPIO4).
2. Count passengers using the rule: **two consecutive ToF readings < 400 mm = 1 passenger**.
3. Publish live values to **Blynk Cloud** virtual pins **V1–V8** as specified in the locked software design.
4. Implement **`brain.py`** to poll Blynk, fetch **Open-Meteo** weather, run **RandomForestRegressor** (100 trees, `random_state=42`), and write risk/status back to Blynk.
5. Apply the locked risk formula with capacity **45** and thresholds **NORMAL / WARNING / CRITICAL**.
6. Alert transit authority via **Telegram** when risk **> 75%** (60 s cooldown); drive **green LED (GPIO26)** / **red LED (GPIO25)** accordingly.
7. Provide operator control **V7 “Bus Left (−30)”** and evidence pin **V8** (minutes since last crossing).
8. Persist every cycle to **`bus_stop_log.csv`**.
9. Document community context, limitations, and future work for viva integrity.

## 1.4 Scope

**In scope**

- Single-node prototype for one boarding edge / stop context (Dindoshi Route 326 narrative).
- Crossing-based count (not true entry–exit occupancy).
- Formula-grounded ML risk score with four binary/continuous inputs as locked.
- Blynk dashboard + Telegram + local CSV logging.
- Buzzer hardware present but **firmware-disabled** (public-stop panic risk; alerts go to Telegram).

**Out of scope (documented future work)**

- Dual ToF entry/exit net occupancy.
- Cloud database / multi-stop fleet dashboard.
- Retraining Random Forest on months of real CSV field data.
- Measured (tape-survey) shelter area and measured boarding batch size for the −30 rule.

## 1.5 Community Engagement Relevance (CEP)

Under NEP-2020 Community Engagement Project expectations, this work:

- Addresses a **local public-transport pain point** experienced by Kandivali–Malad East communities using Dindoshi.
- Keeps cost and complexity appropriate for student implementation and depot-side demonstration.
- Produces an artefact (dashboard + CSV + alert path) that a transit supervisor could conceptually use.
- States limitations honestly so community trust is not built on overstated accuracy.

## 1.6 Organisation of the Report

- **Chapter 2** reviews related research (bus crowding prediction, APC, weather–ridership).
- **Chapter 3** analyses requirements, feasibility, and existing vs proposed system.
- **Chapter 4** presents architecture, pin map, ML formula, and dashboard layout.
- **Chapter 5** describes implementation (Arduino firmware, `brain.py`, logging).
- **Chapter 6** covers testing, demo script, and results.
- **Chapter 7** concludes with limitations and future work.
