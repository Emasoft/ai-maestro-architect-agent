# Changelog

All notable changes to this project will be documented in this file.
    ## [2.17.0] - 2026-08-18

### Bug Fixes

- Set the executable bit on the 17 shebang-carrying files EXE001 flags (TRDD-DMIRQOCD tail, increment 2) — includes scripts/amaa_self_id.py (axis3 C4)    

### Documentation

- Close TRDD-DMIRQOCD (completed) — ruff+CPV adoption done end to end, pin at 0.16.3    

### Features

- Bump the native ruff gate pin 0.15.20 → 0.16.3 (TRDD-DMIRQOCD, final increment)    

### Refactor

- PEP-585/604 modernization — 119 UP fixes + the 21 knock-on F401 unused-typing imports (TRDD-DMIRQOCD tail burn-down, increment 1)    
- Burn the auto-fixable 0.16.3 tail + move E402 suppression to per-file-ignores (TRDD-DMIRQOCD tail, increment 3)    
- Simplification tail — 14 unsafe-fix SIM/C4/PIE/PLC transforms, diff-reviewed (TRDD-DMIRQOCD tail, increment 4a)    


