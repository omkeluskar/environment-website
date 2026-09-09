# CHAPTER 5 — IMPLEMENTATION

## 5.1 Introduction

This chapter describes how the locked design was implemented in Arduino firmware and Python (`brain.py`), including Blynk integration, Telegram alerting, and CSV logging.

## 5.2 Development Environment

| Layer | Tools / Libraries |
|-------|-------------------|
| Firmware | Arduino IDE / ESP32 core, Blynk, Adafruit / Pololu VL53L0X, DHT library |
| Cloud | Blynk Cloud (virtual pins V1–V8) |
| Brain | Python 3, `requests` (Open-Meteo), scikit-learn (`RandomForestRegressor`), Blynk HTTP/API client as used in project, Telegram Bot API |
| Storage | `bus_stop_log.csv` in working directory of `brain.py` |

## 5.3 Arduino Firmware (ESP32)

### 5.3.1 Boot behaviour

On successful init of Wi-Fi, Blynk, VL53L0X, and DHT22, Serial prints **`System Ready`** (demo checkpoint).

### 5.3.2 Crossing detection

Pseudo-logic:

1. Read ToF distance.
2. If current and previous readings both **< 400 mm** and a new crossing is confirmed → `passengerCount++`, set `lastCrossingTime = millis()`.
3. Debounce / state machine prevents double-count on a single pass (as implemented in the `.ino`).

### 5.3.3 Dashboard publish

`sendDashboardData()` (or equivalent periodic routine):

- `Blynk.virtualWrite(V1, passengerCount);`
- `Blynk.virtualWrite(V4, temperature);`
- `Blynk.virtualWrite(V8, (millis() - lastCrossingTime) / 60000);`

### 5.3.4 Bus Left (−30)

```cpp
BLYNK_WRITE(V7) {
  if (param.asInt() == 1) {
    passengerCount = max(0, passengerCount - 30);
    Serial.println(">>> BUS DEPARTED: estimated 30 passengers boarded");
  }
}
```

### 5.3.5 LED control

Driven from risk/status path consistent with thresholds:

- NORMAL → green LED on (GPIO26), red off
- WARNING → dashboard emphasis; LED policy as implemented for demo (warning is primarily dashboard)
- CRITICAL → red LED on (GPIO25)

Exact WARNING LED behaviour should match the flashed firmware used in the Tuesday demo; thresholds for Telegram remain **> 75**.

### 5.3.6 Buzzer

Physically wired via NPN transistor; **no firmware tone/alarm calls** — documented as **wired but firmware-disabled**.

## 5.4 Python Brain (`brain.py`)

### 5.4.1 Responsibilities each cycle

1. Read passenger count / temperature from Blynk (values originated by ESP32).
2. Fetch weather from **Open-Meteo**; map WMO code → Rain/Clear.
3. Determine rush-hour flag from local clock (8–9 AM, 6–7 PM).
4. Determine heat flag (temp ≥ 33°C).
5. Compute `risk_score` via locked formula / RF regressor path.
6. Derive `status` string: NORMAL / WARNING / CRITICAL.
7. Write V2, V3, V5, V6 (including status colour).
8. If `risk_score > 75` and cooldown elapsed → Telegram alert.
9. Append CSV row.

### 5.4.2 CSV bootstrap + append

```python
import csv, os
from datetime import datetime

LOG_FILE = "bus_stop_log.csv"
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w", newline="") as f:
        csv.writer(f).writerow(
            ["timestamp", "passengers", "temp", "weather", "risk", "status"]
        )

# inside main loop, right after risk_score is computed:
with open(LOG_FILE, "a", newline="") as f:
    csv.writer(f).writerow([
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        passenger_count, temp, weather, f"{risk_score:.1f}", status
    ])
```

### 5.4.3 Weather & status colour writes

```python
weather_display = "🌧 Rain" if weather == "Rain" else "☀️ Clear"
Blynk.virtualWrite(V2, weather_display)

status_color = "#FF0000" if risk_score > 75 else "#00AA00"
Blynk.virtualWrite(V6, status_color)
```

### 5.4.4 Random Forest

```python
RandomForestRegressor(n_estimators=100, random_state=42)
```

Features align to the four locked inputs. Prototype training uses formula-consistent synthetic samples; live CSV is the path to real retraining.

## 5.5 Telegram Alert Path

- Trigger: **risk > 75** (strict).
- Cooldown: **60 seconds** between alerts.
- Recipient: transit authority bot chat configured for the project.
- Content: include risk %, passenger count, weather, timestamp (as implemented).

## 5.6 Open-Meteo Integration

- No API key.
- Location near depot coordinates ≈ 19.176°N, 72.864°E.
- Rain if WMO code ∈ {61–67, 80–82, 95–99}; else Clear.

## 5.7 Implementation Status vs Spec

| Spec item | Status |
|-----------|--------|
| ESP32 + VL53L0X + DHT22 pinout | Implemented |
| Blynk V1–V8 | Implemented |
| V7 −30 / V8 minutes | Implemented |
| Open-Meteo (not OWM) | Implemented |
| Formula + RF(100, 42) | Implemented |
| CSV logging | Implemented |
| Telegram >75 + 60 s | Implemented |
| Buzzer firmware-disabled | Implemented |
| Dual-sensor net occupancy | Future work |
| Cloud DB | Future work |

## 5.8 Summary

Implementation realises a closed loop: sense → Blynk → brain → risk/status/alerts/CSV → operator V7 correction, matching the locked software and hardware contracts.
