#define BLYNK_AUTH_TOKEN "********"
char ssid[] = "********";
char pass[] = "********";

#define DHTPIN 4
#define RED_LED 25
#define GREEN_LED 26
const int CONFIRM_THRESHOLD = 2;
const int DETECTION_THRESHOLD_MM = 400;
const unsigned long TOF_CHECK_INTERVAL = 150;

bool isPersonDetected() {
  VL53L0X_RangingMeasurementData_t measure;
  lox.rangingTest(&measure, false);
  return (measure.RangeStatus != 4 &&
          measure.RangeMilliMeter < DETECTION_THRESHOLD_MM);
}

void checkPassengerCrossing() {
  bool detected = isPersonDetected();
  if (detected) {
    consecutiveDetections++;
    if (consecutiveDetections >= CONFIRM_THRESHOLD && !personInFrame) {
      passengerCount++;
      personInFrame = true;
      lastCrossingTime = millis();
    }
  } else {
    consecutiveDetections = 0;
    personInFrame = false;
  }
}

// V7 Bus Left: subtract 30, never auto-reset to zero
BLYNK_WRITE(V7) {
  if (param.asInt() == 1) {
    passengerCount = max(0, passengerCount - 30);
  }
}

// V3 from Python: red LED only when risk > 75 (CRITICAL)
BLYNK_WRITE(V3) {
  pythonRiskScore = param.asInt();
  if (pythonRiskScore > 75) {
    digitalWrite(RED_LED, HIGH);
    digitalWrite(GREEN_LED, LOW);
  } else {
    digitalWrite(RED_LED, LOW);
    digitalWrite(GREEN_LED, HIGH);
  }
}

void sendDashboardData() {
  Blynk.virtualWrite(V1, passengerCount);
  Blynk.virtualWrite(V4, dht.readTemperature());
  Blynk.virtualWrite(V8, (millis() - lastCrossingTime) / 60000);
}
