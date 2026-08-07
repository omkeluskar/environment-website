# CHAPTER 2 — SYSTEM ANALYSIS / LITERATURE REVIEW

> Formatted to match college `chp2 (4).pdf` structure (sections 2.1–2.13, Paper 1–10 style).  
> **PDF:** [`Chapter2_System_Analysis_Literature.pdf`](./Chapter2_System_Analysis_Literature.pdf)

**Project title (page header):** IoT-Based Bus Stop System for Public Transport Overcrowding Prediction Using Machine Learning

## 2.1 Introduction
Links Chapter 1 (Dindoshi / Route 326 overcrowding) to planning work: literature, gaps, requirements, feasibility, HW/SW, schedule, Agile methodology. Names locked stack: ESP32, VL53L0X, DHT22, Blynk, Open-Meteo, brain.py, RF(100, 42), Telegram; honest estimates capacity **45** and V7 **−30**.

## 2.2 Literature Review
Ten papers/sources in **Title / Authors / summary + However** format:

1. Arabghalizi & Labrinidis (2020) — crowding prediction models  
2. Nitti et al. (2020) — iABACUS Wi-Fi APC  
3. Tao et al. (2018) — weather & travel  
4. Rowe et al. (2022) — ML ridership + extreme weather  
5. Kniess et al. (2021) — IoT transport passenger counting (vision)  
6. Oregon DOT / Trillium (2021) — APC/AFC white paper  
7. DCMS (2008) — Guide to Safety at Sports Grounds (density analogy → capacity 45)  
8. The Hindu (2017) — Dindoshi scale  
9. Times of India (2016) — high-commuter depot context  
10. bestpedia.in + MMRDA Bus-Q (existence only; not dimensions)

Closes with synthesis paragraph → need for stop-edge IoT + locked formula + V7/V8 + CSV.

## 2.3 Comparative Analysis of Existing System
Table: Manual visual | Camera APC | Fleet AVL–APC | **Proposed system**

## 2.4 Research Gap Identification
Fleet vs stop-edge; unsafe reset/decay; missing rain/heat/rush in demos; opaque scores / no CSV.

## 2.5 Requirement Gathering Methodology
Observation (Dindoshi, geo-tagged photos) · Interview · Survey (**in progress — no synthetic-as-real**) · Tools

## 2.6 Stakeholder Analysis
Commuters · Depot staff · CEP coordinators · Students · Guide · Co-ordinator

## 2.7 Functional Requirements
FR-1 … FR-10 (crossing rule, Blynk V1–V8, formula/thresholds, Telegram, CSV, buzzer firmware-disabled)

## 2.8 Non-Functional Requirements
NFR-1 … NFR-9 (performance, public-safety UX, usability, transparency, availability, compatibility, scalability, maintainability, cost)

## 2.9 Feasibility Study
Technical · Economic · Operational · Schedule

## 2.10 Software Requirement
Arduino IDE, Blynk, Python 3, scikit-learn, Open-Meteo, Telegram, CSV, editor

## 2.11 Hardware Requirement
ESP32, VL53L0X (21/22), DHT22 (4), LEDs 25/26 + 220Ω, buzzer wired firmware-disabled

## 2.12 Project Schedule
Phased CEP timeline + demo milestones + **Figure 2.1 Gantt chart** (`gantt_chart_2_12.png`, embedded in PDF)

## 2.13 Development Methodology
Agile / iterative; rejected auto-decay and reset-to-zero
