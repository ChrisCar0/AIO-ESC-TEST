# {{ADR‑nnnn: concise title}}

*Status*: Proposed / Accepted / Superseded / Deprecated  
*Deciders*: {{names}}  
*Date*: {{YYYY‑MM‑DD}}

## Context
Briefly explain the problem or driver for this decision.

## Options
1. **Option A** – summary, pros/cons  
2. **Option B** – summary, pros/cons  
3. **Option C** – …

## Decision
State which option you picked and why.

## Consequences
*Positive*  
- …

*Negative / debts*  
- …

## References
- ST AN5555 section 4.2 – BEMF sampling
- LTspice sim: `hardware/sims/bemf_filter.asc`

## Related ADRs
- ADR‑0002: Shunt topology
- ADR‑0005: Gate‑driver selection


cp docs/adr/_adr-template.md ("docs/adr/" + (Get-Date -Format "yyyy-MM-dd") + ".md")
^copy-rename templates