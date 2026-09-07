def get_weather():
    try:
        url = (f"https://api.openweathermap.org/data/2.5/weather"
               f"?lat={BUS_STOP['lat']}&lon={BUS_STOP['lon']}"
               f"&appid={OPENWEATHER_API_KEY}&units=metric")
        data = requests.get(url, timeout=10).json()
        main = data["weather"][0]["main"]
        if main in ("Rain", "Drizzle", "Thunderstorm", "Shower"):
            return "Rain"
        return "Clear"
    except Exception:
        return "Clear"   # fallback: Clear, 28.0 C used if DHT22 missing

def get_blynk_value(pin):
    res = requests.get(
        f"{BLYNK_URL}/get?token={BLYNK_AUTH_TOKEN}&pin={pin}", timeout=5)
    val = res.text.strip('[]" \n')
    if "error" in val.lower() or not val:
        return None
    return float(val)

if not os.path.exists("bus_stop_log.csv"):
    with open("bus_stop_log.csv", "w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow(
            ["timestamp", "passengers", "temp", "weather", "risk", "status"])

while True:
    weather_status = get_weather()
    is_raining = 1 if weather_status == "Rain" else 0
    passenger_count = int(float(get_blynk_value("V1") or 0))
    temp_value = float(get_blynk_value("V4") or 28.0)
    features = np.array([[datetime.now().hour, is_raining,
                          passenger_count, temp_value]])
    risk_score = model.predict(features)[0]

    # <=40 NORMAL | 41-75 WARNING | >75 CRITICAL (exactly 75 = WARNING)
    if risk_score > 75:
        csv_status = "CRITICAL"
        if time.time() - last_telegram_alert_time > 60:
            send_telegram_alert(BUS_STOP, passenger_count, risk_score, weather_status)
            last_telegram_alert_time = time.time()
    elif risk_score > 40:
        csv_status = "WARNING"
    else:
        csv_status = "NORMAL"

    with open("bus_stop_log.csv", "a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            passenger_count, f"{temp_value:.1f}", weather_status,
            f"{risk_score:.1f}", csv_status])
    time.sleep(5)
