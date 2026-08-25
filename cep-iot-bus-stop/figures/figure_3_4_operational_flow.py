"""
Figure 3.4 — Functional Requirement Operational Flow
Visual layout matched to the Smart Umbrella System diagram (grouped
dashed boxes, colour-coded cards, labelled arrows, grey canvas).
Content locked to the 11 Aug 2026 master project spec.
"""
import os
import matplotlib.pyplot as plt
from matplotlib.patches import (
    Rectangle, FancyBboxPatch, FancyArrowPatch, Circle, Arc, Polygon,
)

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
PNG = os.path.join(OUT_DIR, "Figure_3_4.png")
ART = "/opt/cursor/artifacts/Figure_3_4.png"

fig, ax = plt.subplots(figsize=(18.4, 12.6))
ax.set_xlim(0, 18.4)
ax.set_ylim(0, 12.6)
ax.axis("off")
fig.patch.set_facecolor("white")

# Caption outside the border
ax.text(9.2, 12.38, "Figure 3.4: Functional Requirement Operational Flow",
        ha="center", va="center", fontsize=16.5, fontweight="bold",
        color="#111", clip_on=False)

# Main grey canvas
ax.add_patch(Rectangle((0.30, 0.22), 17.80, 11.78,
                       facecolor="#E9E9E9", edgecolor="black", lw=1.45, zorder=0))

# System header
ax.add_patch(FancyBboxPatch(
    (5.35, 11.18), 7.70, 0.62,
    boxstyle="round,pad=0.015,rounding_size=0.10",
    facecolor="#0B3A75", edgecolor="none", zorder=5,
))
ax.text(9.20, 11.49, "SMART BUS STOP SYSTEM",
        ha="center", va="center", color="white", fontsize=17, fontweight="bold", zorder=6)


def group(x, y, w, h, title, color):
    ax.add_patch(Rectangle((x, y), w, h, fill=False, edgecolor=color,
                           lw=1.65, linestyle=(0, (6, 3.2)), zorder=1))
    ax.text(x + w / 2, y + h, title, ha="center", va="center",
            color=color, fontsize=10, fontweight="bold", zorder=6,
            bbox=dict(facecolor="#E9E9E9", edgecolor="none", pad=1.8))


def box(x, y, w, h, edge, fill, z=3):
    ax.add_patch(Rectangle((x, y), w, h, facecolor=fill, edgecolor=edge, lw=2.05, zorder=z))
    return x + w / 2, y + h / 2


def t(x, y, s, **kw):
    kw.setdefault("zorder", 6)
    kw.setdefault("ha", "center")
    kw.setdefault("va", "center")
    ax.text(x, y, s, **kw)


def arr(p1, p2, color, lw=2.05, ls="-", rad=0):
    ax.add_patch(FancyArrowPatch(
        p1, p2, arrowstyle="-|>", mutation_scale=13.5, lw=lw,
        color=color, linestyle=ls, connectionstyle=f"arc3,rad={rad}",
        zorder=4, shrinkA=1, shrinkB=1,
    ))


# ---------- icons ----------
def ic_tof(cx, cy, c):
    ax.add_patch(FancyBboxPatch((cx - 0.30, cy - 0.14), 0.60, 0.28,
                                boxstyle="round,pad=0.01,rounding_size=0.05",
                                facecolor=c, edgecolor="none", zorder=6))
    ax.add_patch(Circle((cx - 0.11, cy), 0.085, facecolor="white", edgecolor="none", zorder=7))
    ax.add_patch(Circle((cx + 0.13, cy), 0.085, facecolor="white", edgecolor="none", zorder=7))
    for r in (0.26, 0.38):
        ax.add_patch(Arc((cx, cy + 0.16), r * 2, r * 1.05, theta1=25, theta2=155,
                         color=c, lw=1.7, zorder=6))


def ic_thermo(cx, cy, c):
    ax.add_patch(FancyBboxPatch((cx - 0.065, cy - 0.02), 0.13, 0.38,
                                boxstyle="round,pad=0.008,rounding_size=0.05",
                                facecolor="white", edgecolor=c, lw=2.0, zorder=6))
    ax.add_patch(Circle((cx, cy - 0.14), 0.145, facecolor=c, edgecolor=c, lw=1.4, zorder=7))
    ax.plot([cx, cx], [cy - 0.04, cy + 0.28], color=c, lw=2.1, zorder=7)
    for yy in (0.06, 0.16, 0.26):
        ax.plot([cx + 0.09, cx + 0.17], [cy + yy, cy + yy], color=c, lw=1.25, zorder=7)


def ic_rain(cx, cy, c):
    ax.add_patch(Circle((cx - 0.16, cy + 0.02), 0.15, facecolor=c, edgecolor="none", zorder=6))
    ax.add_patch(Circle((cx + 0.02, cy + 0.08), 0.18, facecolor=c, edgecolor="none", zorder=6))
    ax.add_patch(Circle((cx + 0.20, cy + 0.01), 0.14, facecolor=c, edgecolor="none", zorder=6))
    ax.add_patch(Rectangle((cx - 0.28, cy - 0.08), 0.54, 0.15, facecolor=c, edgecolor="none", zorder=6))
    for dx in (-0.16, 0.00, 0.16):
        ax.plot([cx + dx, cx + dx - 0.05], [cy - 0.12, cy - 0.28], color=c, lw=1.8, zorder=6)


def ic_chip(cx, cy):
    ax.add_patch(Circle((cx, cy), 0.30, facecolor="#0B7A75", edgecolor="none", zorder=6))
    t(cx, cy, "∞", color="white", fontsize=15, fontweight="bold")
    t(cx - 0.15, cy + 0.01, "+", color="white", fontsize=7, fontweight="bold")
    t(cx + 0.15, cy + 0.01, "−", color="white", fontsize=8, fontweight="bold")


def ic_batt(cx, cy, c):
    ax.add_patch(FancyBboxPatch((cx - 0.26, cy - 0.13), 0.46, 0.26,
                                boxstyle="round,pad=0.008,rounding_size=0.04",
                                facecolor=c, edgecolor="none", zorder=6))
    ax.add_patch(Rectangle((cx + 0.20, cy - 0.06), 0.08, 0.12, facecolor=c, edgecolor="none", zorder=6))
    ax.add_patch(Rectangle((cx - 0.18, cy - 0.06), 0.10, 0.12, facecolor="white", edgecolor="none", zorder=7))
    ax.add_patch(Rectangle((cx - 0.04, cy - 0.06), 0.10, 0.12, facecolor="white", edgecolor="none", zorder=7))


def ic_33(cx, cy, c):
    ax.add_patch(FancyBboxPatch((cx - 0.22, cy - 0.14), 0.44, 0.28,
                                boxstyle="round,pad=0.008,rounding_size=0.05",
                                facecolor=c, edgecolor="none", zorder=6))
    t(cx, cy, "3.3V", color="white", fontsize=8, fontweight="bold")


def ic_shield(cx, cy, c):
    verts = [(cx, cy + 0.24), (cx + 0.20, cy + 0.14), (cx + 0.20, cy - 0.04),
             (cx, cy - 0.22), (cx - 0.20, cy - 0.04), (cx - 0.20, cy + 0.14)]
    ax.add_patch(Polygon(verts, closed=True, facecolor=c, edgecolor="none", zorder=6))
    ax.plot([cx - 0.07, cx - 0.01, cx + 0.10], [cy + 0.02, cy - 0.07, cy + 0.11],
            color="white", lw=2.15, zorder=7, solid_capstyle="round")


def ic_led(cx, cy, c):
    ax.add_patch(Circle((cx, cy + 0.05), 0.145, facecolor=c, edgecolor="none", zorder=6))
    ax.add_patch(Rectangle((cx - 0.045, cy - 0.16), 0.09, 0.13, facecolor=c, edgecolor="none", zorder=6))
    for a, b in ((-0.20, 0.10), (-0.24, 0.18), (0.20, 0.10), (0.24, 0.18)):
        ax.plot([cx, cx + a], [cy + 0.10, cy + b], color=c, lw=1.25, zorder=6)


def ic_plane(cx, cy, c):
    verts = [(cx - 0.26, cy - 0.10), (cx + 0.26, cy + 0.04), (cx - 0.05, cy + 0.02),
             (cx - 0.14, cy + 0.15), (cx - 0.09, cy + 0.00)]
    ax.add_patch(Polygon(verts, closed=True, facecolor=c, edgecolor="none", zorder=6))


def ic_doc(cx, cy, c):
    ax.add_patch(FancyBboxPatch((cx - 0.16, cy - 0.20), 0.32, 0.42,
                                boxstyle="round,pad=0.006,rounding_size=0.03",
                                facecolor="white", edgecolor=c, lw=1.7, zorder=6))
    ax.add_patch(Polygon([(cx + 0.02, cy + 0.22), (cx + 0.16, cy + 0.22), (cx + 0.16, cy + 0.08)],
                         closed=True, facecolor=c, edgecolor="none", zorder=7, alpha=0.38))
    for yy in (-0.06, 0.04, 0.13):
        ax.plot([cx - 0.09, cx + 0.09], [cy + yy, cy + yy], color=c, lw=1.2, zorder=7)


def ic_dash(cx, cy, c):
    ax.add_patch(FancyBboxPatch((cx - 0.28, cy - 0.13), 0.56, 0.26,
                                boxstyle="round,pad=0.008,rounding_size=0.04",
                                facecolor=c, edgecolor="none", zorder=6))
    t(cx, cy, "V1–V8", color="white", fontsize=7.2, fontweight="bold")


# ============================================================
# INPUT & SENSING
# ============================================================
group(2.45, 7.78, 13.50, 2.92, "INPUT & SENSING FUNCTIONS", "#1A73E8")

# Passenger
cx, _ = box(2.68, 7.92, 3.85, 2.52, "#1E8E3E", "#EAF6EC")
ic_tof(cx, 10.10, "#1E8E3E")
t(cx, 9.72, "PASSENGER DETECTION", color="#1E8E3E", fontsize=9.4, fontweight="bold")
t(cx, 8.72,
  "VL53L0X Time-of-Flight Sensor\n"
  "I2C  ·  SDA GPIO21 / SCL GPIO22\n"
  "2 consecutive readings < 400 mm\n"
  "count as 1 passenger crossing",
  fontsize=7.7, linespacing=1.32)

# Temperature
cx, _ = box(7.28, 7.92, 3.85, 2.52, "#E65100", "#FFF4E5")
ic_thermo(cx, 10.12, "#E65100")
t(cx, 9.72, "TEMPERATURE MONITORING", color="#E65100", fontsize=8.9, fontweight="bold")
t(cx, 8.72,
  "DHT22 Temperature Sensor\n"
  "GPIO4  ·  3.3 V rail (built-in pull-up)\n"
  "Continuously measures temperature\n"
  "Heat bonus if temp ≥ 33 °C  →  V4",
  fontsize=7.7, linespacing=1.32)

# Weather
cx, _ = box(11.88, 7.92, 3.85, 2.52, "#6A1B9A", "#F4E8F8")
ic_rain(cx, 10.12, "#6A1B9A")
t(cx, 9.72, "WEATHER INTEGRATION", color="#6A1B9A", fontsize=9.4, fontweight="bold")
t(cx, 8.72,
  "OpenWeatherMap Current API\n"
  "Dindoshi  19.1753°N, 72.8649°E\n"
  "Rain if main ∈ Rain / Drizzle /\n"
  "Thunderstorm / Shower  →  V2",
  fontsize=7.7, linespacing=1.32)

# ============================================================
# POWER (left)
# ============================================================
group(0.48, 3.62, 3.42, 3.62, "POWER SUPPLY", "#6A1B9A")

cx, _ = box(0.64, 5.42, 3.10, 1.58, "#1E8E3E", "#EAF6EC")
ic_batt(cx, 6.68, "#1E8E3E")
t(cx, 6.32, "USB 5 V POWER", color="#1E8E3E", fontsize=9.0, fontweight="bold")
t(cx, 5.82, "USB 5 V powers the ESP32\n(on-board regulator only)", fontsize=7.5, linespacing=1.28)

cx, _ = box(0.64, 3.78, 3.10, 1.58, "#6A1B9A", "#F4E8F8")
ic_33(cx, 5.04, "#6A1B9A")
t(cx, 4.68, "3.3 V SENSOR RAIL", color="#6A1B9A", fontsize=8.8, fontweight="bold")
t(cx, 4.18, "All peripherals on 3.3 V only\nNever 5 V / VIN for logic", fontsize=7.5, linespacing=1.28)

# ============================================================
# CPU (center)
# ============================================================
box(4.18, 3.62, 7.42, 3.62, "#1565C0", "#E3F2FD")
ic_chip(7.89, 6.82)
t(7.89, 6.38, "CENTRAL PROCESSING UNIT", color="#0D47A1", fontsize=12.0, fontweight="bold")
t(7.89, 6.06, "ESP32 DoIT DevKit V1   &   Python brain.py", color="#1565C0",
  fontsize=8.6, fontweight="bold")
t(7.89, 4.88,
  "•  Receives data from all sensors & weather API\n"
  "•  Processes 4-feature array via RandomForestRegressor\n"
  "     (100 trees, random_state=42)   hour · rain · count · temperature\n"
  "•  Decides: NORMAL (≤40)  /  WARNING (41–75)  /  CRITICAL (>75)\n"
  "     risk = min(98, count÷45×75 + rain 15 + heat 10 + rush 10)\n"
  "•  Sends control signals to LEDs, Telegram, V6 status text\n"
  "•  Monitors V7 operator pin for manual interrupt  (−30)",
  fontsize=7.55, linespacing=1.30)

# ============================================================
# OPERATOR CONTROL (right)
# ============================================================
group(13.88, 3.62, 3.88, 3.62, "OPERATOR CONTROL  (INTERRUPT)", "#C62828")

cx, _ = box(14.04, 5.42, 3.56, 1.58, "#C62828", "#FFFFFF")
t(cx, 6.68, "V8  TIME SINCE LAST CROSSING", color="#C62828", fontsize=7.6, fontweight="bold")
t(cx, 5.92,
  "Continuously reports minutes since\n"
  "the last confirmed ToF crossing.\n"
  "Evidence for the operator — not\n"
  "automatic bus detection.",
  fontsize=7.35, linespacing=1.25)

cx, _ = box(14.04, 3.78, 3.56, 1.58, "#C62828", "#FDECEE")
ic_shield(cx, 5.06, "#C62828")
t(cx, 4.68, "When pressed, ESP32 immediately", color="#B71C1C", fontsize=7.3)
t(cx, 4.18,
  "V7 Push  “Bus Left (−30)”\n"
  "passengerCount = max(0, count − 30)",
  fontsize=7.5, fontweight="bold", color="#B71C1C", linespacing=1.28)

# ============================================================
# OUTPUT group
# ============================================================
group(4.18, 0.42, 13.58, 2.72, "OUTPUT & LOGGING MODULES", "#5F6368")

cx, _ = box(4.36, 0.58, 3.18, 2.28, "#F9A825", "#FFF8E1")
ic_led(cx, 2.50, "#F9A825")
t(cx, 2.18, "ON-SITE AWARENESS", color="#E65100", fontsize=8.6, fontweight="bold")
t(cx, 1.92, "Red LED GPIO25  ·  Green LED GPIO26", color="#BF360C", fontsize=6.6)
t(cx, 1.22,
  "Red LED  = CRITICAL  (> 75)\n"
  "Green LED = NORMAL  (≤ 40)\n"
  "Buzzer wired, firmware-disabled",
  fontsize=7.35, linespacing=1.28)

cx, _ = box(7.70, 0.58, 3.18, 2.28, "#2E7D32", "#EAF6EC")
ic_plane(cx, 2.50, "#2E7D32")
t(cx, 2.18, "REMOTE ALERTS (TELEGRAM)", color="#1B5E20", fontsize=7.9, fontweight="bold")
t(cx, 1.22,
  "Fires only if risk > 75% (strict)\n"
  "60-second cooldown\n"
  "count, risk %, weather, Maps link",
  fontsize=7.35, linespacing=1.28)

cx, _ = box(11.04, 0.58, 3.18, 2.28, "#424242", "#F3F3F3")
ic_doc(cx, 2.50, "#424242")
t(cx, 2.18, "DATA STORAGE (CSV)", color="#212121", fontsize=8.6, fontweight="bold")
t(cx, 1.92, "bus_stop_log.csv", color="#424242", fontsize=7.0)
t(cx, 1.22,
  "Every 5 s cycle appends\n"
  "timestamp, passengers, temp,\n"
  "weather, risk, status (plain text)",
  fontsize=7.35, linespacing=1.28)

# Dashboard as the far-right "mechanism" (dashed like the umbrella)
ax.add_patch(Rectangle((14.42, 0.58), 3.12, 2.28, fill=False,
                       edgecolor="#1565C0", lw=1.7, linestyle=(0, (4, 2.5)), zorder=3))
cx = 15.98
ic_dash(cx, 2.46, "#1565C0")
t(cx, 2.14, "BLYNK DASHBOARD", color="#0D47A1", fontsize=8.4, fontweight="bold")
t(cx, 1.22,
  "Dindoshi Depot — Route 326\n"
  "V1 gauge 0–45  ·  V3 0–98\n"
  "V6  RED / AMBER / GREEN text",
  fontsize=7.25, linespacing=1.28)


# ============================================================
# ARROWS
# ============================================================
# Inputs → CPU (colour matched)
arr((4.60, 7.92), (5.55, 7.24), "#1E8E3E")
arr((9.20, 7.92), (8.20, 7.24), "#E65100")
arr((13.80, 7.92), (10.55, 7.24), "#6A1B9A")
t(12.55, 7.48, "HTTPS (JSON)", color="#6A1B9A", fontsize=7.3, fontweight="bold",
  bbox=dict(facecolor="#E9E9E9", edgecolor="none", pad=0.7))

# Power → CPU
arr((3.74, 6.20), (4.18, 5.85), "#1E8E3E")
t(3.92, 6.38, "5V USB", color="#1E8E3E", fontsize=7.3, fontweight="bold")

arr((3.74, 4.55), (4.18, 4.85), "#6A1B9A")
t(3.90, 4.38, "3.3V DC", color="#6A1B9A", fontsize=7.3, fontweight="bold")

# 3.3V rail also feeds the sensing group (upward, like 12V going to actuator side
# but here sensors sit above — draw a short labelled stub into the group)
arr((2.19, 7.00), (2.19, 7.78), "#6A1B9A", lw=1.7, ls=(0, (4, 2.8)))
t(2.19, 7.38, "3.3V", color="#6A1B9A", fontsize=7.0, fontweight="bold",
  bbox=dict(facecolor="#E9E9E9", edgecolor="none", pad=0.5), rotation=90)

# Operator interrupt (dashed red) — photo style
arr((14.04, 4.55), (11.60, 5.05), "#C62828", lw=2.0, ls=(0, (4.5, 2.8)))
t(12.78, 5.28, "Interrupt Signals\n(Digital V7)", color="#C62828",
  fontsize=7.4, fontweight="bold",
  bbox=dict(facecolor="#E9E9E9", edgecolor="none", pad=0.7))

arr((14.04, 6.20), (11.60, 6.00), "#C62828", lw=1.55, ls=(0, (3.2, 2.4)))
t(12.78, 6.38, "V8 evidence", color="#C62828", fontsize=7.1, fontweight="bold")

# CPU → outputs
arr((5.95, 3.62), (5.95, 2.86), "#1565C0")
arr((7.89, 3.62), (9.29, 2.86), "#1565C0")
arr((10.20, 3.62), (12.63, 2.86), "#1565C0")
t(8.55, 3.22, "GPIO & cloud writes", color="#1565C0", fontsize=7.3, fontweight="bold",
  bbox=dict(facecolor="#E9E9E9", edgecolor="none", pad=0.55))

# CSV → Blynk (dashed, like motor → umbrella)
arr((14.22, 1.72), (14.42, 1.72), "#1565C0", lw=1.7, ls=(0, (4, 2.5)))
t(15.98, 2.86, "V1–V8 live pins", color="#1565C0", fontsize=7.0, fontweight="bold")

plt.tight_layout(pad=0.15)
fig.savefig(PNG, dpi=300, bbox_inches="tight", facecolor="white")
fig.savefig(ART, dpi=300, bbox_inches="tight", facecolor="white")
print("saved", PNG)
print("saved", ART)
