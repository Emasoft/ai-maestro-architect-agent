# LSP Troubleshooting: Extended Languages

Troubleshooting guide for Java, Kotlin, C/C++, C#, PHP, Ruby, and cross-language issues.

---

## Table of Contents

- [Java (jdtls) Issues](#java-jdtls-issues)
  - ["Cannot resolve symbol" for imported classes](#cannot-resolve-symbol-for-imported-classes)
  - ["Project build path is incomplete"](#project-build-path-is-incomplete)
- [Kotlin Issues](#kotlin-issues)
  - ["Unresolved reference" for standard library](#unresolved-reference-for-standard-library)
  - ["Type mismatch" with Java interop](#type-mismatch-with-java-interop)
- [C/C++ (clangd) Issues](#cc-clangd-issues)
  - ["'file.h' file not found"](#fileh-file-not-found)
  - ["Unknown argument '-std=c++20'"](#unknown-argument--stdc20)
- [C# (OmniSharp) Issues](#c-omnisharp-issues)
  - ["The type or namespace could not be found"](#the-type-or-namespace-could-not-be-found)
  - ["Nullable warnings everywhere"](#nullable-warnings-everywhere)
- [PHP (Intelephense) Issues](#php-intelephense-issues)
  - ["Undefined function/class"](#undefined-functionclass)
  - ["Method not found" for Laravel facades](#method-not-found-for-laravel-facades)
- [Ruby (Solargraph) Issues](#ruby-solargraph-issues)
  - ["Undefined method" for valid code](#undefined-method-for-valid-code)
  - ["LoadError: cannot load such file"](#loaderror-cannot-load-such-file)
- [Cross-Language Issues](#cross-language-issues)
  - ["LSP installed but features not working"](#lsp-installed-but-features-not-working)
  - ["Multiple LSP errors after git branch switch"](#multiple-lsp-errors-after-git-branch-switch)
- [Official Documentation](#official-documentation)

---

## Java (jdtls) Issues

### "Cannot resolve symbol" for imported classes

**Cause:** Build path not configured or dependencies not resolved

**Solution:**
```bash
# For Maven projects
mvn dependency:resolve
mvn clean install -DskipTests

# For Gradle projects
./gradlew dependencies
./gradlew clean build -x test

# Verify Java version
java --version  # Should be JDK 11+

# Restart jdtls (usually automatic after build)
```

### "Project build path is incomplete"

**Cause:** Missing JDK or incorrect JAVA_HOME

**Solution:**
```bash
# Set JAVA_HOME
export JAVA_HOME=$(/usr/libexec/java_home -v 17)  # macOS
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk    # Linux

# Verify path
echo $JAVA_HOME
$JAVA_HOME/bin/java --version

# Add to shell profile
echo 'export JAVA_HOME=$(/usr/libexec/java_home -v 17)' >> ~/.zshrc
```

---

## Kotlin Issues

### "Unresolved reference" for standard library

**Cause:** Kotlin compiler version mismatch or missing stdlib

**Solution:**
```bash
# For Gradle projects
./gradlew clean
./gradlew kotlinDslAccessors  # Regenerate accessors

# Check Kotlin version consistency in build.gradle.kts
grep kotlin build.gradle.kts

# Verify JDK compatibility
java --version  # JDK 11+ required
```

### "Type mismatch" with Java interop

**Cause:** Platform types and nullability annotations

**Solution:**
```kotlin
// Add explicit null checks for Java types
val result: String? = javaMethod()  // nullable
val safe: String = javaMethod() ?: ""  // with default

// Use @Nullable/@NotNull annotations in Java code
// or configure strict mode in build.gradle.kts
```

---

## C/C++ (clangd) Issues

### "'file.h' file not found"

**Cause:** Missing compile_commands.json or incorrect include paths

**Solution:**
```bash
# Generate compile_commands.json for CMake
cmake -DCMAKE_EXPORT_COMPILE_COMMANDS=ON -B build
ln -sf build/compile_commands.json .

# For Make projects, use Bear
bear -- make

# Verify compilation database
cat compile_commands.json | head -50
```

### "Unknown argument '-std=c++20'"

**Cause:** Clangd version doesn't support C++20

**Solution:**
```bash
# Update clangd/LLVM
brew upgrade llvm  # macOS
sudo apt update && sudo apt upgrade clangd  # Linux

# Or use older standard in CMakeLists.txt
set(CMAKE_CXX_STANDARD 17)
```

---

## C# (OmniSharp) Issues

### "The type or namespace could not be found"

**Cause:** NuGet packages not restored or project not built

**Solution:**
```bash
# Restore packages
dotnet restore

# Rebuild solution
dotnet clean
dotnet build

# Verify .NET SDK version
dotnet --version  # .NET 6.0+ required

# Check project file
cat *.csproj | grep -A5 ItemGroup
```

### "Nullable warnings everywhere"

**Cause:** Nullable reference types enabled without annotations

**Solution:**
```csharp
// Option 1: Disable nullable in project file
// <Nullable>disable</Nullable>

// Option 2: Add proper nullable annotations
public string? OptionalValue { get; set; }
public string RequiredValue { get; set; } = "";

// Option 3: Suppress specific warnings
#pragma warning disable CS8618
```

---

## PHP (Intelephense) Issues

### "Undefined function/class"

**Cause:** Missing autoload or incorrect namespace

**Solution:**
```bash
# Regenerate autoload
composer dump-autoload

# Verify autoload in composer.json
cat composer.json | jq '.autoload'

# Check namespace matches directory structure
ls -la src/
head -5 src/YourClass.php  # Should show namespace
```

### "Method not found" for Laravel facades

**Cause:** IDE helper files not generated

**Solution:**
```bash
# Install Laravel IDE helper
composer require --dev barryvdh/laravel-ide-helper

# Generate helper files
php artisan ide-helper:generate
php artisan ide-helper:models --nowrite
php artisan ide-helper:meta

# Add to .gitignore
echo "_ide_helper*.php" >> .gitignore
```

---

## Ruby (Solargraph) Issues

### "Undefined method" for valid code

**Cause:** Missing YARD documentation or gem stubs

**Solution:**
```bash
# Download core documentation
solargraph download-core

# Generate documentation for gems
yard gems

# Create .solargraph.yml
cat > .solargraph.yml <<EOF
include:
  - "**/*.rb"
exclude:
  - vendor/**/*
  - spec/**/*
reporters:
  - rubocop
EOF

# Rebuild index
solargraph clear
solargraph bundle
```

### "LoadError: cannot load such file"

**Cause:** Bundler environment not active

**Solution:**
```bash
# Always run in bundle context
bundle exec solargraph stdio

# Or set in plugin config to use bundler
# command: ["bundle", "exec", "solargraph", "stdio"]

# Verify gem paths
bundle show solargraph
```

---

## Cross-Language Issues

### "LSP installed but features not working"

**Cause:** Plugin not properly connected to LSP binary

**Solution:**
```bash
# Verify plugin configuration
/plugin list -v

# Check plugin points to correct binary
cat ~/.claude/plugins/<lsp-name>/plugin.json

# Test binary directly
<lsp-binary> --version

# Reinstall plugin
/plugin uninstall <lsp-name>
/plugin install <lsp-name>
```

### "Multiple LSP errors after git branch switch"

**Cause:** Dependencies or types changed between branches

**Solution:**
```bash
# Reinstall dependencies for current branch

# Python
pip install -r requirements.txt

# TypeScript/JavaScript
npm install  # or pnpm install

# Rust
cargo update

# Go
go mod download

# Java/Kotlin
./gradlew dependencies  # or mvn dependency:resolve

# C/C++
cmake -B build  # Regenerate compile_commands.json

# C#
dotnet restore

# PHP
composer install

# Ruby
bundle install

# Restart all LSP servers
/plugin reload pyright-lsp
/plugin reload typescript-lsp
/plugin reload rust-lsp
/plugin reload gopls-lsp
/plugin reload jdtls-lsp
/plugin reload kotlin-lsp
/plugin reload clangd-lsp
/plugin reload omnisharp-lsp
/plugin reload intelephense-lsp
/plugin reload solargraph-lsp
```

---

## Official Documentation

**Always refer to official documentation for the latest LSP server configurations.**

- [Claude Code LSP Servers Documentation](https://docs.anthropic.com/en/docs/claude-code/mcp#lsp-servers)
- [Claude Code Plugin System](https://docs.anthropic.com/en/docs/claude-code/plugins)
- [Claude Code Best Practices](https://docs.anthropic.com/en/docs/claude-code/best-practices)

The official Anthropic documentation is the authoritative source for:
- LSP enforcement requirements and recommendations
- Verification and validation procedures
- Installation troubleshooting guides
- Integration with remote agent workflows
- LSP error handling and recovery strategies
