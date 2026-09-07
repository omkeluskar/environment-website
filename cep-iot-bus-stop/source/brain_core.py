import os, csv, time, requests, numpy as np
from datetime import datetime
from sklearn.ensemble import RandomForestRegressor

BLYNK_AUTH_TOKEN = "********"
BLYNK_URL = "https://blynk.cloud/external/api"
TELEGRAM_BOT_TOKEN = "********"
TELEGRAM_CHAT_ID = "********"
OPENWEATHER_API_KEY = "********"

BUS_STOP = {
    "id": "BEST-DIN-001",
    "name": "Dindoshi Bus Depot",
    "lat": 19.1753,
    "lon": 72.8649,
    "assigned_route": "Route 326",
}

STOP_CAPACITY = 45  # reasoned stand-capacity estimate

def calculate_synthetic_risk(hour, is_raining, passenger_count, temperature):
    passenger_ratio = min(1.0, passenger_count / STOP_CAPACITY)
    passenger_component = passenger_ratio * 75
    rain_bonus = 15 if is_raining else 0
    heat_bonus = 10 if temperature >= 33 else 0
    rush_hour_bonus = 10 if hour in [8, 9, 18, 19] else 0
    return min(98, passenger_component + rain_bonus + heat_bonus + rush_hour_bonus)

hours_to_sample = list(range(0, 24))
passenger_counts = list(range(0, 101))
weather_options = [0, 1]
temperature_options = [20, 24, 28, 30, 32, 33, 34, 35, 38]

X_train_list, y_train_list = [], []
for hour in hours_to_sample:
    for count in passenger_counts:
        for rain in weather_options:
            for temperature in temperature_options:
                risk = calculate_synthetic_risk(hour, rain, count, temperature)
                X_train_list.append([hour, rain, count, temperature])
                y_train_list.append(risk)

X_train, y_train = np.array(X_train_list), np.array(y_train_list)
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
