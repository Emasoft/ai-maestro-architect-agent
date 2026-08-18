# Changelog

All notable changes to this project will be documented in this file.
    ## [2.16.0] - 2026-08-18

### Bug Fixes

- Repair the planning-patterns script surface (TRDD-WDM195GD)    
- Reconcile the design-lifecycle state machine with its docs and close the archive bypass (TRDD-QW4ISL8Z)    
- PLW1510 burn-down complete — annotate the 36 audited sites, fix the 3 real defects and the manifest/validator swallows (TRDD-DMIRQOCD steps 2+3a)    

### Documentation

- Decide TRDD-DMIRQOCD — reject ruff 0.16.3, take the 107 via extend-select    
- Record TRDD-DMIRQOCD phase 1a landed and the burn-down paused under TRDD-BRRJK57P    
- Author Phase-2 TRDDs WDM195GD/QW4ISL8Z/HN65IC8P/ET0STPKK from hub-ledgered findings; unpause TRDD-DMIRQOCD per hub phased-adoption ruling    
- Archive-column hygiene + record hub rulings (TRDD-ET0STPKK)    
- Close TRDD-HN65IC8P (completed, impl 9d2c936) + land ET0STPKK's frontmatter that git mv left unstaged    
- Close TRDD-WDM195GD (completed, impl 2ca94c3)    
- Close TRDD-QW4ISL8Z (completed, impl 8ef38f3)    
- Record TRDD-DMIRQOCD 107 burn-down complete + ratchet live; card stays open for the pin bump (impl aa118ea, 0cbcbe5, 9276e2e)    
- Record the Phase-2 remediation outcome in PROJECT wikimem    
- Redact the two absolute home paths from TRDD-DMIRQOCD (CPV strict gate CRITICALs) — the hub repo is named, not pathed    

### Features

- Land the fail-fast ratchet — per-site honest suppressions + extend-select BLE001,S110,PLW1510,TRY004 (TRDD-DMIRQOCD steps 3b+4)    

### Refactor

- State check=False explicitly at publish.py's 10 inspected run() sites (TRDD-DMIRQOCD)    
- Delete lib/report_utils.py — a mandate with zero callers (TRDD-HN65IC8P)    


