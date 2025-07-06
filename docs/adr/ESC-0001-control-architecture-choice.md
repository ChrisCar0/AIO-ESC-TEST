# ADR_ESC‑0001  Control Architecture Choice

*Decider*: Chris C.  
*Date*: 2025‑05‑19  

## Context
I need an ESC that is reliable for student use, dynamic, and easier to debug/work with.

## Decision
Adopt **sensor‑less trapezoidal (square‑wave) commutation**, but integrate optional access to sensored F.O.C.  
Documented advantages:
- Motor agnostic, robust, simpler firmware, broad flight‑stack support.  

Potential drawbacks of FOC (tuning, complexity, higher hardware specs) outweigh its efficiency gain for the time being. (Will want to implement this as a option though, so the higher hardware specs shouldn't be considered.)

## Consequences
+ Faster bring‑up; new students can swap motors without retuning.  
− Torque ripple and efficiency slightly worse than well‑tuned FOC.  
+ Optional F.O.C. use.  

> Next step: leave spare ADC pins and MCU head‑room so a future firmware can migrate to sinusoidal or FOC if needed.