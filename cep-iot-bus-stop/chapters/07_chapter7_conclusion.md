# CHAPTER 7 — CONCLUSION AND FUTURE WORK

## 7.1 Conclusion

This Community Engagement Project designed and demonstrated an **IoT-Based Bus Stop System for Public Transport Overcrowding Prediction Using Machine Learning** for the community context of **Dindoshi Bus Depot / BEST Route 326**.

The prototype integrates:

- **ESP32** sensing (VL53L0X crossings, DHT22 climate),
- **Blynk Cloud** visualisation (V1–V8),
- **Open-Meteo** rain context,
- a transparent risk formula capped at **98%** with passenger contribution capped at **75%**,
- **RandomForestRegressor** (100 trees, `random_state=42`),
- **Telegram** escalation for risk **> 75%**,
- operator **V7 (−30)** / **V8** evidence workflow, and
- persistent **`bus_stop_log.csv`** logging.

The work shows that a low-cost student system can surface overcrowding risk early enough for an authority-side response, while remaining honest about what a single crossing sensor can and cannot measure.

## 7.2 Objectives — Attainment

| Objective | Attainment |
|-----------|------------|
| Hardware prototype on ESP32 3.3 V rail | Achieved |
| Crossing rule < 400 mm × 2 | Achieved |
| Blynk V1–V8 map | Achieved |
| brain.py + Open-Meteo + RF | Achieved |
| Locked formula & thresholds | Achieved |
| Telegram + LED CRITICAL path | Achieved |
| V7 −30 / V8 minutes | Achieved |
| CSV logging | Achieved |
| Honest CEP documentation | Achieved |

## 7.3 Honest Limitations (state proactively in viva)

1. **Ghost counting:** sensor counts crossings, not net occupancy → dual ToF entry/exit is future work.
2. **Synthetic training data:** formula-generated, grounded in research features; CSV now collects real cycles; **retraining is the next step** (point at the CSV during viva).
3. **Capacity 45** is estimated, not measured.
4. **Subtract-30** is an estimate of boarding batch size, not measured.
5. **File-based logging** is implemented; a cloud database remains future work.
6. Buzzer is present in wiring but **firmware-disabled** by design.

## 7.4 Future Work

1. Two-sensor entry/exit for true occupancy.
2. Retrain Random Forest on weeks/months of `bus_stop_log.csv`.
3. Measure shelter area on site (replace estimated 16 sq m if survey allows).
4. Calibrate boarding batch size for V7 from conductor observations.
5. Multi-stop Blynk / backend with role-based alerts.
6. Optional privacy-preserving APC alternatives after ethics review.

## 7.5 Community Impact

For Kandivali–Malad East commuters using Dindoshi, even a prototype risk signal can:

- help staff prioritise dispatch attention,
- make overcrowding discussable with **shared numbers**, and
- create a data trail (CSV) for college–community follow-up under NEP-2020 CEP spirit.

## 7.6 Closing Statement

The project delivers a complete, demo-ready IoT + ML overcrowding prediction loop with locked parameters, community-safe alerting, and transparent limitations — suitable for internal submission and implementation demonstration.
