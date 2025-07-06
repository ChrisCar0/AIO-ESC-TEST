# 70 A BLDC ESC – Requirements & TODO

## Project Goal
> Design, build, and validate a standalone 70 A sensor‑less ESC that can later be integrated into a drone all‑in‑one power board.


## Requirements
1. **Battery** – 4 S – 6 S Li‑Po (≈ 14 – 25 V)  
2. **Current** – 70 A continuous, 80 A peak (< 10 s)  
3. **Control** – Sensor‑less trapezoidal / 6‑step (BEMF zero‑cross)  
4. **I/O** – PWM input @ 500 Hz  
   - *Stretch goal*: DSHOT‑300  
5. **Measurement bandwidth** – Current‑sense bandwidth ≫ voltage‑sense bandwidth  
6. **Protections** – OCP, OVP, OTP (trip < 2 µs)  
7. **Thermal target** – < 100 °C case @ 70 A, 25 °C ambient  
8. **Form factor** – ≤ 50 mm × 50 mm, weight ≤ 75 g  
9. **Cost goal** – < Not determined  


| Item                  | Determines                                                    | Target                                                     |
|-----------------------|---------------------------------------------------------------|------------------------------------------------------------|
| Battery               | MOSFET V<sub>DS</sub>, gate‑driver bootstrap margin           | 4 S – 6 S Li‑Po (≈ 14 – 25 V)                              |
| Current               | FET, shunt, copper sizing; thermal design                     | 70 A continuous, 80 A peak                                 |
| Control               | Firmware and sensing architecture                             | Sensor‑less **trapezoidal (6‑step)** using BEMF zero‑cross |
| I/O                   | Interface to flight controller                                | 500 Hz PWM (or DSHOT‑300) plus “throttle‑cal” routine      |
| Protections           | Trip time needed to save FETs                                 | OCP, OVP, OTP (< 2 µs)                                     |
| Measurement bandwidth | Peak‑current limiting & commutation‑timing accuracy           | Current ≫ Voltage (tens kHz vs a few kHz)                  |



## TODO (ordered)
1. Pick MOSFETs (≤ 2 mΩ, 40 V class)  
2. Select gate‑driver (e.g. DRV832x, LMG1205)  
3. Choose shunt topology (2‑shunt vs 3‑shunt) & sense amps  
4. Decide on MCU (STM32 G431 / G474)  
5. Design input TVS + LC filter  
6. Draft schematic in KiCad  
7. Run LTspice power‑stage & OCP simulations  
8. Lay out 4‑layer, 2‑oz PCB with thermal vias  
9. Order prototypes + stencil  
10. Bring‑up firmware: open‑loop ramp → zero‑cross detect  
11. Bench spin test @ 12 V  
12. Dyno test 70 A continuous, log shunt vs ADC  
13. Thermal soak & EMI scan  
14. Merge design into the AIO drone board  
15. Tag and archive **v1.0** release (schematic, layout, firmware)
