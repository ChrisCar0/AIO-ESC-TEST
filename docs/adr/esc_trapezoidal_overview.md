# Sensorless Trapezoidal ESC – Design Rationale & Theory

This document encapsulates the design principles that detail the **sensor‑less trapezoidal Electronic Speed Controller (ESC)** for Brushless DC (BLDC) motors that will be integrated into the Drone All-In-One (AIO) board.  It records *why* each subsystem is required and the main trade‑offs behind the recommended implementation so future students can trace schematic or firmware decisions back to first principles.

---

## 1  Power Stage (3‑Phase Inverter)

| Goal                                                    | Notes                                                                                                             |
| ------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| Efficiently switch battery power into a 3‑phase winding | Use a 6‑switch half‑bridge topology (low‑side + high‑side MOSFET per phase).                                      |
| Prevent shoot‑through                                   | Add **dead‑time** in PWM generation or use a gate‑driver with built‑in dead‑time insertion.                       |
| Handle inductive energy                                 | Body diodes usually suffice for BLDC currents; add RC or RCD **snubbers** if ringing > 10 % of bus.               |
| Minimise losses                                         | Choose ≤ 2 mΩ, 40 V FETs, strong gate drivers (≈ 1‑2 Ω pull‑down) to keep switching loss manageable at 30‑50 kHz. |

---

## 2  Motor Commutation

**120° six‑step (trapezoidal) scheme**

* Only two phases conduct at any instant; the third phase floats.
* Commutation every 60 electrical degrees → six distinct states.
* Rotor position is inferred from the **zero‑crossing** of the floating phase’s back EMF (BEMF).
* Simple, CPU‑light, and robust at the cost of higher torque ripple vs FOC.

---

## 3  BEMF Zero‑Crossing Detection Methods

| ID     | Method                                         | Duty‑cycle ceiling | Hardware complexity                             | Low‑speed sensitivity               |
| ------ | ---------------------------------------------- | ------------------ | ----------------------------------------------- | ----------------------------------- |
| **3a** | *Sampling at end of PWM OFF* (ST “3‑resistor”) | \~95 %             | 3 × 100 k–200 k resistors wired to MCU ADC pins | **Highest** – minimal filtering     |
| **3b** | *Sampling during PWM ON* (analog RC filter)    | 100 %              | Voltage divider + RC per phase                  | Moderate                            |
| **3c** | *Digital filter* (TI)                          | 100 %              | Same analog front‑end as 3b + DSP filtering     | Good                                |
| **3d** | *Mixed* (3a → 3b at speed)                     | 100 %              | Firmware switching logic                        | Best overall, added code complexity |

> **Recommendation:** Prototype with **3a** for bring‑up simplicity, then implement **3d** so the ESC can reach 100 % duty without losing zero‑cross events.

---

## 4  Virtual Neutral Reconstruction

Many outrunners do **not expose the star centre**.  Reconstruct the neutral voltage digitally:

$$
V_\text{n} = \frac{V_a + V_b + V_c}{3}
$$

The BEMF of the floating phase is then

$$
E_{\text{phase}} = V_{\text{floating}} - V_\text{n}.
$$

Subtracting in firmware removes common‑mode bus ripple and improves zero‑cross detection in noisy environments.

---

## 5  Commutation Timing Logic

1. Detect BEMF zero‑cross on the floating phase.
2. Wait **30° electrical** (1 ⁄ 6 of the last electrical period) – this aligns the next state so active windings coincide with peak phase voltage.
3. Schedule the commutation ISR to toggle the appropriate MOSFET pair.
4. Update period estimate → feeds rotor speed & open‑loop start‑up ramp.

---

## 6  Control Loops

| Loop                      | Function                                                | Typical rate               |
| ------------------------- | ------------------------------------------------------- | -------------------------- |
| **Open‑loop start‑up**    | Aligns rotor, ramps PWM duty until BEMF is detectable.  | Once at boot               |
| **Commutation ISR**       | Executes six‑step state changes; must be deterministic. | Event‑driven (≈ 10‑50 kHz) |
| **Current PI (optional)** | Limits phase current during acceleration / stall.       | 5 – 10 kHz                 |
| **Speed PI (optional)**   | Maintains commanded RPM.                                | 1 kHz                      |

Open‑loop only is acceptable for drones (throttle‑based control), but adding a current PI loop greatly improves fault resilience at 70 A.

---

## 7  Microcontroller Selection Criteria

* **ADC resources** – min 3 channels with simultaneous sampling or interleaved at ≥ 200 ksps.
* **Advanced PWM timers** – centre‑aligned, dead‑time insertion, and edge‑triggered ADC sync.
* **Fast comparators / op‑amps on‑chip** – shortcut over‑current and BEMF conditioning.
* **Example MCUs**:

  * **STM32G431/G474** – 170 MHz M4F, 4 MSPS ADC, 3 advanced timers.
  * **STM32F103** – budget choice; adequate for ≤ 30 kHz PWM.
  * **TI F2803x** – C28x core with dedicated PWM & comparator subsystem.

---

## 8  Additional Protections & Features

* **Over‑current (OCP)** – shunt + fast comparator + gate‑driver cycle‑by‑cycle latch (< 2 µs).
* **Over‑voltage (OVP)** – comparator on Vbus, disable PWM when > 26 V.
* **Over‑temperature (OTP)** – NTC on FET tab → derate duty or shut down at 100 °C.
* **Braking / freewheeling** – optional PWM mode to absorb kinetic energy during descent.
* **Telemetry** – if DShot is implemented, stream phase current & FET temp back to flight controller.

---

## 9 Control‑Architecture Options

| Strategy | Rotor sensing | Pros | Cons | Typical use case |
|----------|---------------|------|------|------------------|
| **Six‑step trapezoidal (baseline)** | Sensor‑less BEMF zero‑cross | Simple firmware, low CPU, works from very low speed with 3‑resistor method | High torque ripple, EMI, acoustics | Quadcopter ESCs where flight controller closes outer loop |
| **Sinusoidal (SVM / 180° conduction)** | BEMF amplitude or sensor‑less PLL | Lower torque ripple, smoother acoustics | More complex ISR timing, needs precise phase angle | Gimbals, low‑noise drones |
| **FOC (Field‑Oriented Control)** | Sensor‑based (Hall, encoder) or sensor‑less observer | Maximum efficiency, full torque control, true closed‑loop current | Highest computational load, complex tuning, needs clean current feedback | EVTOL, robotics, high‑performance e‑bike ESCs |
| **Hybrid path** | Start in open‑loop six‑step; transition to sinusoidal or FOC once speed/EMF sufficient | Leverages strength of each regime (robust start‑up and high‑efficiency cruise) | Firmware state‑machine complexity | Versatile AIO drone power boards |

> **Adoption plan:** Release v1 with trapezoidal control only. Keep ADC resources and MCU head‑room so a future firmware can overlay a Clarke/Park transform for sinusoidal or FOC without hardware changes.


---

## 10  References

* STMicroelectronics **UM3259** – *Trapezoidal control with zero‑cross detection on STM32G4*.
* TI Application Report **SLVA749** – *Sensorless trapezoidal control using digital filtering*.
* “AN/UM” design files for **STEVAL‑ESC001V1** reference board.

---

*Last updated: 2025‑05‑19*