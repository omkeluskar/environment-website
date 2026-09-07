def send_telegram_alert(stop, passengers, risk, weather):
    message = (
        f"HIGH OVERCROWDING ALERT\n"
        f"Stop Name: {stop['name']}\n"
        f"Stop ID: {stop['id']}\n"
        f"Live Passenger Count: {passengers}\n"
        f"AI Risk Score: {risk:.1f}%\n"
        f"Weather: {weather}\n"
        f"Action: Dispatch extra feeder bus on {stop['assigned_route']}."
    )
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    requests.post(url, json=payload, timeout=10)

# Blynk writes after each 5-second cycle (Python owns V2, V3, V5, V6)
requests.get(f"{BLYNK_URL}/update?token={BLYNK_AUTH_TOKEN}"
             f"&pin=V2&value={'Rain' if is_raining else 'Clear'}", timeout=5)
requests.get(f"{BLYNK_URL}/update?token={BLYNK_AUTH_TOKEN}"
             f"&pin=V3&value={int(risk_score)}", timeout=5)
requests.get(f"{BLYNK_URL}/update?token={BLYNK_AUTH_TOKEN}"
             f"&pin=V5&value={current_datetime_str}", timeout=5)
requests.get(f"{BLYNK_URL}/update?token={BLYNK_AUTH_TOKEN}"
             f"&pin=V6&value={status_emoji}", timeout=5)
