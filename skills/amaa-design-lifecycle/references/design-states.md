# Design States

## Table of Contents

- State Definitions

## State Definitions

| State | Description | Transitions |
|-------|-------------|-------------|
| DRAFT | Initial creation | -> REVIEW |
| REVIEW | Under review | -> APPROVED / -> DRAFT |
| APPROVED | Ready for implementation | -> IMPLEMENTING |
| IMPLEMENTING | Being implemented | -> COMPLETED |
| COMPLETED | Fully implemented | -> ARCHIVED |
| ARCHIVED | Historical reference | (terminal) |
