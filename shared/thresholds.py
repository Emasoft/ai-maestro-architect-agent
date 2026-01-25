"""
thresholds.py - Shared constants for Architect Agent.

These thresholds configure behavior for design documents,
requirements analysis, and planning workflows.
"""

# Design document limits
MAX_DESIGN_DOC_SIZE_KB = 500
MAX_REQUIREMENTS_PER_MODULE = 50

# Planning thresholds
MAX_MODULES_PER_PLAN = 20
MIN_MODULE_DESCRIPTION_LENGTH = 100

# API research limits
MAX_API_RESEARCH_DEPTH = 3
API_RESEARCH_TIMEOUT_SECONDS = 120

# Hypothesis verification
MAX_VERIFICATION_ATTEMPTS = 3
VERIFICATION_TIMEOUT_SECONDS = 300

# Documentation generation
MAX_DOC_SECTIONS = 20
DOC_GENERATION_TIMEOUT_SECONDS = 180
