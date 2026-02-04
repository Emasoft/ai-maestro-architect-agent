# LSP Post-Assignment Verification & Enforcement

After remote agent completes work, orchestrator MUST verify LSP compliance.

## Table of Contents

- [Post-Assignment Verification](#post-assignment-verification)
  - [1. LSP Diagnostics Check](#1-lsp-diagnostics-check)
  - [2. Type Safety Verification](#2-type-safety-verification)
  - [3. Code Navigation Test](#3-code-navigation-test)
  - [4. Quality Gates](#4-quality-gates)
- [Orchestrator Enforcement](#orchestrator-enforcement)
- [Rejection Criteria](#rejection-criteria)
- [Benefits Tracked](#benefits-tracked)

---

## Post-Assignment Verification

### 1. LSP Diagnostics Check
```bash
# Review LSP errors in modified files
/plugin errors

# Expected: No errors in changed files
# If errors found: Request fixes before PR approval
```

### 2. Type Safety Verification

**Python:**
```bash
# Run pyright on changed files
pyright src/module.py
# Expected: 0 errors, 0 warnings
```

**TypeScript:**
```bash
# Run tsc on changed files
npx tsc --noEmit src/module.ts
# Expected: no errors
```

**Rust:**
```bash
# Run cargo check on changed files
cargo check
# Expected: no errors
```

**Go:**
```bash
# Run gopls check on changed files
gopls check ./...
# Expected: no errors
```

**Java:**
```bash
# Run jdtls check on changed files (via build tool)
./gradlew compileJava
# or
mvn compile
# Expected: BUILD SUCCESS
```

**Kotlin:**
```bash
# Run Kotlin compiler check
./gradlew compileKotlin
# or
kotlinc -Werror src/main.kt
# Expected: no errors
```

**C/C++:**
```bash
# Run clang-tidy on changed files
clang-tidy -p compile_commands.json src/module.cpp
# Expected: no warnings or errors
```

**C#:**
```bash
# Run dotnet build to verify types
dotnet build --no-restore
# Expected: Build succeeded
```

**PHP:**
```bash
# Run phpstan for static analysis
vendor/bin/phpstan analyse src/
# Expected: no errors found
```

**Ruby:**
```bash
# Run solargraph type checking
solargraph typecheck
# Expected: no problems found
```

### 3. Code Navigation Test

Verify LSP features work on modified code:
- [ ] Go to definition works for new symbols
- [ ] Find references finds all usages
- [ ] Hover shows correct type information
- [ ] Auto-complete suggests appropriate symbols

### 4. Quality Gates

Before accepting agent's work:
- [ ] All LSP diagnostics resolved
- [ ] Type checking passes for all languages
- [ ] No "any" types in TypeScript (unless explicitly allowed)
- [ ] No "type: ignore" in Python (unless documented)
- [ ] Rust code has no unsafe blocks (unless justified)
- [ ] Go code follows official style guide (verified by gopls)
- [ ] Java code has no raw types (unless justified)
- [ ] Kotlin code uses null-safety properly (no `!!` abuse)
- [ ] C/C++ code passes clang-tidy with no warnings
- [ ] C# code has no nullable reference warnings (unless documented)
- [ ] PHP code passes phpstan at level 6+ (or configured level)
- [ ] Ruby code has YARD documentation for public methods

## Orchestrator Enforcement

The orchestrator MUST:

1. **Before task assignment**: Run LSP verification script
2. **On failure**: Block assignment until LSP installed
3. **In task instructions**: Include "Ensure LSP diagnostics pass"
4. **On PR review**: Verify no LSP errors in changed files

## Rejection Criteria

Reject remote agent assignment if:
- LSP binaries not installed for project languages
- /plugin errors shows LSP failures
- Agent reports "executable not found" errors

## Benefits Tracked

Track LSP benefits in progress reports:
- Type errors caught before PR submission
- Reduced review cycles due to fewer basic errors
- Faster navigation to definitions/references

---

**Next**: See [lsp-enforcement-checklist-part4-troubleshooting-core.md](lsp-enforcement-checklist-part4-troubleshooting-core.md) for troubleshooting common LSP issues.
