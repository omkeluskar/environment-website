# CHAPTER 2 — LITERATURE REVIEW

## 2.1 Introduction

This chapter surveys research that motivates an IoT + ML approach to **bus-stop / bus crowding prediction**, passenger counting, and weather-sensitive ridership. The review is selective: it supports design choices in this CEP without claiming that every cited system was reproduced.

## 2.2 Crowding Prediction Models

**Arabghalizi & Labrinidis (2020)** study data-driven bus crowding prediction in *ACM Transactions on Data Science*. Their work shows that crowding can be forecast from operational and contextual features rather than treated as a purely reactive observation. This CEP borrows the **prediction mindset** — combining count with context (weather, heat, rush hour) — while remaining a **stop-edge IoT prototype**, not a full fleet AVL/APC analytics stack.

## 2.3 Automatic Passenger Counting (APC)

**Nitti, Girau & Floris (2020)** present **iABACUS**, a Wi-Fi-based automatic bus passenger counting system (*Energies*). Wi-Fi probing can estimate occupancy without a break-beam sensor, but depends on device carriage, MAC randomisation, and privacy policy. For a student CEP at a public shelter, a **short-range ToF crossing counter (VL53L0X)** was chosen for deterministic local sensing and simpler ethics messaging.

Camera-based APC reviews (e.g. **Kniess, 2021**, IFIP/IEEE context; **Oregon DOT, 2021**, APC white-paper tradition) emphasise accuracy potential alongside **cost, lighting, occlusion, and privacy** limitations. Those limitations justify avoiding CCTV as the primary CEP sensor.

## 2.4 Weather and Ridership

**Tao et al. (2018)** (“To travel or not to travel: ‘Weather’ is the question”, *Transportation Research Part C*) link weather to travel decisions. **Rowe, Mahony & Tao (2022)** assess ML algorithms for near-real-time bus ridership prediction during extreme weather (arXiv:2204.09792). Together they support treating **rain as a crowding amplifier** at stops (passengers cluster under shelter). This project encodes rain as a **binary +15%** term via **Open-Meteo** WMO weather codes (61–67, 80–82, 95–99 → Rain; else Clear). Older draft documents that mentioned OpenWeatherMap are **incorrect** relative to the locked implementation.

## 2.5 Sensing and Embedded IoT Platforms

Low-cost microcontroller platforms (ESP32 class) with I2C distance sensors are widely used in academic prototypes for presence and crossing detection. The **VL53L0X** provides millimetre-class ranging suitable for a narrow gate/crossing zone. Pairing with **DHT22** enables a local heat feature (≥ 33°C → +10%), reasoned for Mumbai summers (honest caveat: not taken from one specific paper’s threshold).

## 2.6 Safety Density Guidance

The UK **Department for Culture, Media and Sport (2008)** *Guide to Safety at Sports Grounds* (5th ed.) provides density bands used here only as an **analogy for congestion risk**, not as a claim that a bus shelter is a sports ground. Combined with an **≈16 sq m** estimated shelter area, this underpins capacity **45** (see Chapter 1 / Chapter 4). **MMRDA Bus-Q Shelter** material is cited for **programme existence only**, not for measured shelter dimensions used in this report.

## 2.7 Local Context Sources

- *The Hindu* (2017): BEST terminal makeovers; Dindoshi scale ≈3,243 sq m, ≈8,500 passengers/day.
- *Times of India* (2016): Dindoshi among high-commuter depot reports (≈1.47 lakh daily in that reporting).
- bestpedia.in: Dindoshi ≈3,242.9 sq m, ≈8,331 passengers/day.

These sources establish **community scale**; they do not replace the reasoned shelter capacity of 45.

## 2.8 Research Gap Addressed by This Project

| Gap in typical literature / practice | This CEP response |
|--------------------------------------|-------------------|
| Fleet-scale models need rich AVL/APC feeds | Single-stop IoT node with Blynk |
| Camera APC costly / privacy-sensitive | VL53L0X crossing count |
| Weather ignored in many student IoT demos | Open-Meteo rain feature |
| Opaque “ML scores” | Locked transparent formula + RF regressor |
| Reset-to-zero after bus departure | V7 subtract 30 + V8 evidence |
| No persistence | `bus_stop_log.csv` every cycle |

## 2.9 Summary

Literature supports (i) predicting crowding from context, (ii) careful APC choice, and (iii) weather sensitivity. This project operationalises those ideas in a **community-deployable prototype** with explicit honesty about estimates and sensor limits.
