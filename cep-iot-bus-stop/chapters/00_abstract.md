# ABSTRACT

Public bus stops in Mumbai frequently experience overcrowding during peak hours, creating discomfort and safety concerns for daily commuters. This Community Engagement Project proposes an **IoT-Based Bus Stop System for Public Transport Overcrowding Prediction Using Machine Learning**, deployed conceptually at **Dindoshi Bus Depot** (General Arun Kumar Vaidya Marg, Malad East, Mumbai 400097), serving **BEST Route 326**.

The system uses an **ESP32 DoIT DevKit V1** with a **VL53L0X** Time-of-Flight sensor to count passenger crossings (two consecutive readings below 400 mm register one passenger), and a **DHT22** sensor for temperature and humidity. Sensor data is published to **Blynk Cloud**. A Python module (`brain.py`) polls Blynk, fetches live weather from the **Open-Meteo** API (no API key required), and computes an overcrowding risk score using a **RandomForestRegressor** (scikit-learn, 100 trees, `random_state=42`) guided by a transparent, locked risk formula.

Risk is computed as:

```
risk = min(98, (passenger_count ÷ 45 × 75) + rain(15) + heat(10) + rush_hour(10))
```

where stop capacity is a reasoned estimate of **45** passengers. Thresholds are: **0–40% NORMAL** (green LED), **41–75% WARNING** (dashboard only), and **>75% CRITICAL** (red LED + Telegram alert with 60-second cooldown). A Blynk push button **V7 “Bus Left (−30)”** subtracts an estimated boarding batch of 30 rather than resetting to zero, preserving stragglers; **V8** shows minutes since the last crossing. Persistent cycles are logged to **`bus_stop_log.csv`**.

The project demonstrates end-to-end sensing, cloud dashboards, ML-assisted risk scoring, and authority alerting, while honestly documenting limitations such as ghost counting, estimated capacity, and synthetic training data pending real CSV-based retraining.

**Keywords:** IoT, ESP32, VL53L0X, Blynk, Open-Meteo, Random Forest, overcrowding prediction, BEST, Dindoshi, Community Engagement Project
