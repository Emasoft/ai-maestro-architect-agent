# Changelog

All notable changes to this project will be documented in this file.
    ## [2.4.3] - 2026-04-10

### Bug Fixes

- Add AMP communication restriction to all sub-agents    
- Correct communication rules in main-agent    
- Publish.py runs CPV validation remotely + pre-push enforces --strict    
- Ruff F541 — remove extraneous f-prefix in publish.py    
- Remove CPV_PUBLISH_PIPELINE bypass from pre-push hook — CPV --strict always runs    
- Publish.py + pre-push use cpv-remote-validate via uvx    
- CPV --strict validation — add 'Loaded by' to all skill descriptions + update workflow    
- Publish.py — strict no-skip policy (propagated from ai-maestro-plugin)    

### Features

- Add compatible-titles and compatible-clients to agent profile    
- Add communication permissions from title-based graph    
- Add smart publish pipeline + pre-push hook enforcement    

### Miscellaneous

- Update uv.lock    


