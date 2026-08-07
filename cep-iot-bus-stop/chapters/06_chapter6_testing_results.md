# CHAPTER 6 — TESTING AND RESULTS

## 6.1 Introduction

Testing verifies that the prototype behaves according to the locked thresholds, pin map, and operator workflow. Results below describe the intended demo outcomes used for the implementation viva.

## 6.2 Test Environment

- ESP32 node powered; Serial Monitor open.
- `brain.py` running with network access (Blynk + Open-Meteo + Telegram).
- Blynk dashboard showing Dindoshi Route 326 layout.
- Excel / spreadsheet available to open `bus_stop_log.csv`.

## 6.3 Test Cases

### TC1 — Boot

| Step | Expected |
|------|----------|
| Power ESP32 / reset | Serial: **System Ready** |
| Start `brain.py` | Cycle loop runs; CSV header exists or is created |

**Result:** Pass (demo script step 1–2).

### TC2 — Crossing increments count

| Step | Expected |
|------|----------|
| Wave hand / object through ToF zone (< 400 mm, two consecutive reads) | V1 passenger count increases |
| Observe V8 | Minutes-since-crossing resets toward 0 after a new crossing |

**Result:** Pass — count climbs on dashboard.

### TC3 — Risk rises toward CRITICAL

| Step | Expected |
|------|----------|
| Continue crossings and/or contextual bonuses | V3 risk increases per formula |
| When risk **> 75** | Red LED + Telegram alert; V6 colour `#FF0000` |
| Immediate second CRITICAL within 60 s | No duplicate Telegram (cooldown) |

**Boundary check:** If risk computes to **exactly 75.0** → WARNING only (no Telegram).

**Result:** Pass when risk crosses above 75.

### TC4 — Bus Left (−30)

| Step | Expected |
|------|----------|
| Note count C (≥ 30 preferred) | — |
| Tap V7 Push “Bus Left (−30)” | Count becomes `max(0, C - 30)` |
| Serial | `>>> BUS DEPARTED: estimated 30 passengers boarded` |
| Risk | Falls accordingly on next brain cycle |

**Result:** Pass — count drops by 30, not to zero (unless C < 30).

### TC5 — CSV persistence

| Step | Expected |
|------|----------|
| Open `bus_stop_log.csv` | Rows with timestamp, passengers, temp, weather, risk, status |
| Multiple cycles | New rows appended (file-based DB working) |

**Result:** Pass — live rows visible in Excel.

### TC6 — Weather display

| Step | Expected |
|------|----------|
| Open-Meteo returns rain codes | V2 shows `🌧 Rain`; rain bonus active in risk |
| Clear codes | V2 shows `☀️ Clear` |

**Result:** Pass under live API conditions.

### TC7 — Buzzer silence

| Step | Expected |
|------|----------|
| Drive system into CRITICAL | Buzzer remains silent; Telegram carries alert |

**Result:** Pass — firmware-disabled as designed.

## 6.4 Sample Risk Walkthrough (illustrative)

Assume capacity 45, no rain, no heat, not rush hour:

| Passengers | Passenger component | Risk | Status |
|------------|---------------------|------|--------|
| 0 | 0 | 0 | NORMAL |
| 18 | 18/45×75 = 30 | 30 | NORMAL |
| 27 | 45 | 45 | WARNING |
| 45 | 75 | 75 | WARNING (boundary) |
| 45 + rain | 75+15 = 90 | 90 | CRITICAL |

With heat (+10) and rush (+10) the same passenger level escalates faster — showing why count alone is capped at 75%.

## 6.5 Demo Script (Tuesday)

1. Boot ESP32 → Serial **System Ready**
2. Run `brain.py` → CSV logging live
3. Show Blynk dashboard live
4. Wave at sensor → count climbs → risk **> 75** → red LED + Telegram
5. Tap V7 **Bus Left (−30)** → count −30 → risk falls
6. Open `bus_stop_log.csv` in Excel → show real rows

## 6.6 Results Discussion

The prototype meets CEP demonstration goals: **sensing, cloud visualisation, contextual risk, authority alert, operator correction, and persistent logging**. Quantitative “accuracy vs true occupancy” is **not** claimed, because a single ToF measures crossings, not net headcount. CSV logging is the bridge from synthetic training to future real-data evaluation.

## 6.7 Summary

All critical path tests required for the viva demo are defined and aligned with locked behaviour, including the 75.0 WARNING boundary and V7 subtract-30 semantics.
