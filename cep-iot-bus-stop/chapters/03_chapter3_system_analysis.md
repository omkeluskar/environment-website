# CHAPTER 3 — SYSTEM ANALYSIS

## 3.1 Introduction

This chapter analyses the existing situation at a busy BEST context (Dindoshi / Route 326), states functional and non-functional requirements, and records feasibility and design decisions that are now **locked** in the Master Project Document.

## 3.2 Existing System

Today, overcrowding at many Mumbai bus stops is managed by:

- Visual judgement by conductors / depot staff,
- Informal passenger self-organisation,
- Schedule knowledge without a live shelter-edge risk score.

There is typically **no low-cost public dashboard** that fuses local passenger-crossing count, temperature, rain, and rush hour into a single risk percentage with LED and Telegram escalation.

## 3.3 Proposed System

An ESP32-based IoT node counts crossings (VL53L0X), reads climate (DHT22), and streams data to **Blynk Cloud**. Python **`brain.py`** enriches with **Open-Meteo** weather, computes risk (formula + RandomForestRegressor), updates Blynk (including status colour), logs CSV rows, and triggers **Telegram** when risk **> 75%**. Operators use **V7** to subtract an estimated boarding of **30** and consult **V8** for minutes since last crossing.

## 3.4 Requirement Analysis

### 3.4.1 Functional Requirements

| ID | Requirement |
|----|-------------|
| FR1 | Detect passenger crossing when two consecutive ToF readings are < 400 mm |
| FR2 | Read temperature/humidity from DHT22 on GPIO4 |
| FR3 | Write passenger count to Blynk **V1**; temperature to **V4** |
| FR4 | Python writes weather (**V2**), ML risk (**V3**), day/time (**V5**), status colour (**V6**) |
| FR5 | Support **V7** push button: `passengerCount = max(0, passengerCount - 30)` |
| FR6 | Publish **V8** = minutes since last confirmed crossing |
| FR7 | Compute risk with locked formula; cap at **98%** |
| FR8 | Map risk to NORMAL / WARNING / CRITICAL with specified LED / Telegram behaviour |
| FR9 | Append each cycle to `bus_stop_log.csv` |
| FR10 | Keep buzzer **firmware-disabled** despite being wired |

### 3.4.2 Non-Functional Requirements

| ID | Requirement |
|----|-------------|
| NFR1 | Operate on ESP32 **3.3 V** rail for all peripherals |
| NFR2 | Telegram CRITICAL alerts use **60 s cooldown** |
| NFR3 | Transparent thresholds suitable for viva defence |
| NFR4 | Logging must survive simple demo (file-based DB) |
| NFR5 | Public-facing audible alarm must not panic commuters |

## 3.5 Feasibility Study

### Technical feasibility
ESP32 + VL53L0X + DHT22 + Blynk + Python scikit-learn is well within student capability and available libraries.

### Economic feasibility
Components are low-cost relative to commercial APC. Open-Meteo requires **no API key**. Blynk Cloud free tier is adequate for prototype pins V1–V8.

### Operational feasibility
Dashboard is usable by a supervisor with minimal training: watch gauges, check V8, press V7 after a bus leaves.

### Schedule feasibility
Fits Semester V CEP timeline: prototype → dashboard → demo script → documentation.

## 3.6 Stakeholders

- **Commuters** at Dindoshi / Route 326 (indirect beneficiaries).
- **Transit / depot staff** (alert recipients via Telegram; Blynk operators).
- **Students & guide** (implementers / evaluators).
- **College CEP coordinators** (academic compliance).

## 3.7 Use Cases (summary)

1. **Passenger crosses sensing zone** → count increments → risk may rise → LEDs/dashboard update.
2. **Rain / heat / rush hour** → contextual bonuses applied in risk formula.
3. **Risk exceeds 75%** → red LED + Telegram (if cooldown elapsed).
4. **Bus departs** → operator reviews V8 → presses V7 → count drops by 30 (floored at 0).
5. **Analyst opens CSV** → inspects timestamped history for demo / future retraining.

## 3.8 Data Dictionary (core fields)

| Field | Source | Notes |
|-------|--------|-------|
| passengers | VL53L0X via ESP32 → V1 | Crossing count, not net occupancy |
| temp | DHT22 → V4 | Heat if ≥ 33°C |
| weather | Open-Meteo → V2 | Rain / Clear (+ emoji display) |
| risk | brain.py → V3 | 0–98 |
| status | derived | NORMAL / WARNING / CRITICAL |
| V8 minutes | ESP32 | Time since last crossing |
| timestamp | brain.py | CSV column |

## 3.9 Risk Formula Analysis (why these weights)

Inputs (exactly four):

1. **Passenger count** — primary; maps to at most **75%** of risk (`count/45 × 75`).
2. **Rain** — **+15%** when raining (shelter clustering).
3. **Heat** — **+10%** when temperature ≥ **33°C**.
4. **Rush hour** — **+10%** during **8–9 AM** and **6–7 PM**.

Design properties:

- Count alone **cannot** reach CRITICAL without a weather/time bonus (75% passenger cap).
- Global cap **98%** avoids claiming absolute certainty.
- At **exactly 75.0** → **WARNING**, not CRITICAL (strictly greater than 75 for CRITICAL).

## 3.10 Rejected Alternatives (important for viva)

| Idea tested / considered | Why rejected |
|--------------------------|--------------|
| Reset count to 0 on “bus left” | Erases stragglers; single ToF does not see exits |
| Automatic timer decay of count | Can wipe a real crowd mid-rush or decay during the moment an alarm is needed |
| Audible buzzer at stop | Panic / nuisance risk in public space |
| Firebase as IoT backend | Locked platform is **Blynk Cloud** |
| OpenWeatherMap | Locked weather source is **Open-Meteo** |
| Presenting 25 synthetic surveys as real | Integrity violation — Option A or B only |

## 3.11 Summary

System analysis locks requirements around a transparent risk model, Blynk pins V1–V8, manual −30 boarding correction, CSV persistence, and community-safe alerting — setting the stage for detailed design in Chapter 4.
