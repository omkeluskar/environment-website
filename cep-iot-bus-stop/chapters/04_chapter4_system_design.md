# CHAPTER 4 — SYSTEM DESIGN

## 4.1 Introduction

This chapter details hardware architecture, software architecture, Blynk pin map, ML/risk design, dashboard layout, and capacity rationale — all aligned to the locked Master Project Document.

## 4.2 System Architecture

```
[VL53L0X ToF] --I2C--> \
[DHT22] ------GPIO4-->  ESP32 DoIT DevKit V1 --WiFi--> Blynk Cloud
[Green LED GPIO26] <--/                              ^
[Red LED GPIO25]   <--/                              |
[Buzzer via NPN] (wired, firmware-DISABLED)          |
                                                     |
                              brain.py <-------------+
                                 |  polls V1/V4, writes V2/V3/V5/V6
                                 |-- Open-Meteo (weather)
                                 |-- RandomForestRegressor (100 trees, rs=42)
                                 |-- Telegram (if risk > 75)
                                 |-- bus_stop_log.csv (append each cycle)
```

**Deployment narrative coordinates:** ≈ **19.176°N, 72.864°E** (Dindoshi Bus Depot area).

## 4.3 Hardware Design

| Component | Role | Connection |
|-----------|------|------------|
| ESP32 DoIT DevKit V1 | MCU / Wi-Fi | 3.3 V rail for peripherals |
| VL53L0X | Crossing detection | I2C SDA=GPIO21, SCL=GPIO22 |
| DHT22 | Temperature / humidity | GPIO4 |
| Red LED | CRITICAL indication | GPIO25 via 220 Ω |
| Green LED | NORMAL indication | GPIO26 via 220 Ω |
| Buzzer + NPN | Hardware path only | **Firmware-disabled**; Telegram used instead |

### 4.3.1 Passenger crossing rule

Two consecutive VL53L0X readings **< 400 mm** ⇒ **+1 passenger**.  
On confirmation, firmware updates `lastCrossingTime = millis()` for V8.

### 4.3.2 Why firmware-disable the buzzer

An audible alarm at a public stop could panic or irritate commuters. Design decision: keep the transistor wiring for completeness of the schematic, but **do not sound it in firmware**; escalate silently to the authority Telegram chat.

## 4.4 Software Design — Blynk Virtual Pins

| Pin | Direction | Meaning |
|-----|-----------|---------|
| V1 | Arduino → Blynk | Passenger count |
| V2 | Python → Blynk | Weather (`🌧 Rain` / `☀️ Clear`) |
| V3 | Python → Blynk | ML risk score |
| V4 | Arduino → Blynk | Temperature |
| V5 | Python → Blynk | Day / time |
| V6 | Python → Blynk | System status **colour** (`#00AA00` / `#FF0000`) |
| V7 | Blynk → Arduino | “Bus Left (−30)” push button |
| V8 | Arduino → Blynk | Minutes since last crossing |

### 4.4.1 V7 / V8 logic (locked)

```cpp
BLYNK_WRITE(V7) {
  if (param.asInt() == 1) {
    passengerCount = max(0, passengerCount - 30);
    Serial.println(">>> BUS DEPARTED: estimated 30 passengers boarded");
  }
}
```

- **Subtract 30, do not reset to 0.** A single ToF counts arrivals, not exits; reset would erase stragglers. **30** = reasoned estimate of typical boarding at one stop (**not measured**).
- **V8** = `(millis() - lastCrossingTime) / 60000` — helps the operator decide when a bus has likely come and gone before pressing V7.
- Automatic timer resets / decay were tested and **rejected**.

## 4.5 ML Parameters & Risk Formula (LOCKED)

**Exactly four inputs**

| Input | Source | Encoding |
|-------|--------|----------|
| Passenger count | VL53L0X | Continuous; highest weight |
| Rain | Open-Meteo | Binary; **+15** if Rain |
| Heat | DHT22 | Binary; **+10** if temp ≥ **33°C** |
| Rush hour | System clock | Binary; **+10** if 8–9 AM or 6–7 PM |

**Formula**

```
risk = min(98, (passenger_count ÷ 45 × 75) + rain(15) + heat(10) + rush_hour(10))
```

**Model:** `RandomForestRegressor` — scikit-learn, **100 trees**, `random_state=42`.  
Training data for the prototype is **formula-grounded / synthetic**, with research-backed feature choices; **`bus_stop_log.csv`** enables future retraining on real cycles.

### Decision thresholds (constants; model outputs a number)

| Risk | Status | Action |
|------|--------|--------|
| 0–40% | NORMAL | Green LED |
| 41–75% | WARNING | Dashboard warning; **no** phone alert |
| **> 75%** | CRITICAL | Red LED + Telegram (60 s cooldown) |

**Boundary:** risk **== 75.0** → **WARNING**, not CRITICAL.

**Status colour write:** `#FF0000` if risk > 75 else `#00AA00`.

## 4.6 Stop Capacity = 45

| Step | Value |
|------|-------|
| Estimated shelter area | ≈16 sq m (≈6.0 m × 2.7 m) |
| Congestion guidance | 3–4 people/m² (UK Green Guide analogy) |
| Chosen operating density | ≈2.78 / m² |
| Capacity | 16 × 2.78 ≈ **45** |

Honest phrasing for viva: **“45 is a reasoned, conservative estimate — not a measured number.”**  
Cite **MMRDA Bus-Q Shelter** only for programme existence, **not** for these dimensions.

## 4.7 Blynk Dashboard Layout (final)

1. Location label: **📍 Dindoshi Bus Depot — Route 326**
2. **V7** “Bus Left (−30)” — Push mode, near top, visually distinct
3. **V8** “Time Since Last Crossing”
4. Passenger Count gauge (**V1**): min 0, max **45**, colour zones
5. ML Risk gauge (**V3**): min 0, max **98**; zones green 0–40 / yellow 41–75 / red 76–98
6. System Status tile (**V6**) — green/red via colour write
7. Weather (**V2**) + Temperature (**V4**)
8. SuperChart: count + risk over time

## 4.8 Logging Design

File: **`bus_stop_log.csv`** (implemented file-based database).

Header:

```
timestamp, passengers, temp, weather, risk, status
```

Each `brain.py` cycle appends one row after `risk_score` is computed.

## 4.9 Weather Design

- API: **Open-Meteo** (free, no key).
- WMO codes **61–67, 80–82, 95–99** → Rain; else Clear.
- Display string: `🌧 Rain` or `☀️ Clear` on V2.

## 4.10 Summary

Design freezes hardware pins, Blynk map, formula, thresholds, V7/V8 behaviour, dashboard, and CSV schema so implementation (Chapter 5) cannot drift from the locked spec.
