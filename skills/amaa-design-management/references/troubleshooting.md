# Troubleshooting

This document provides solutions for common issues when working with design document management tools.

## Contents

- 6.1 UUID Generation Issues
- 6.2 Creation Failures
- 6.3 Search Issues
- 6.4 Frontmatter Parsing Issues
- 6.5 Directory Structure Issues
- 6.6 Permission Issues
- 6.7 Encoding Issues

---

## 6.1 UUID Generation Issues

### Duplicate UUID Generated

**Symptom:** Script reports UUID already exists or creates document with conflicting UUID.

**Cause:** UUID sequence scanning failed to find all existing UUIDs.

**Solution:**

1. Search for existing UUIDs manually:
   ```bash
   grep -r "GUUID-$(date +%Y%m%d)" design/
   ```

2. Find the highest sequence number:
   ```bash
   python scripts/eia_design_search.py --pattern "**/*.md" | grep "GUUID-$(date +%Y%m%d)" | sort
   ```

3. Manually specify next sequence if needed by editing the created file.

### UUID Not Following Format

**Symptom:** Validation rejects UUID format.

**Cause:** Manually created UUID doesn't match GUUID-YYYYMMDD-NNNN format.

**Solution:**

Check format requirements:
```
Valid:   GUUID-20250129-0001
         GUUID-20251231-9999

Invalid: UUID-20250129-0001    (wrong prefix)
         GUUID-2025129-0001    (date too short)
         GUUID-20250129-1      (sequence not 4 digits)
         GUUID-20250129-0000   (sequence must be >= 1)
```

---

## 6.2 Creation Failures

### "Design directory not found"

**Symptom:** Script reports design directory doesn't exist.

**Cause:** Running from wrong location or design/ not created.

**Solution:**

1. Create the design directory structure:
   ```bash
   mkdir -p design/{pdr,spec,feature,decision,architecture,template}
   ```

2. Or specify the path explicitly:
   ```bash
   python scripts/eia_design_create.py \
     --type pdr \
     --title "Test" \
     --design-dir /full/path/to/design
   ```

### "Failed to write file: Permission denied"

**Symptom:** Cannot create file in design directory.

**Cause:** Directory permissions prevent writing.

**Solution:**

1. Check permissions:
   ```bash
   ls -la design/
   ```

2. Fix permissions:
   ```bash
   chmod 755 design/
   chmod 755 design/pdr/
   ```

### File Created But Validation Fails

**Symptom:** Document created but validation reports errors.

**Cause:** Bug in template or frontmatter generation.

**Solution:**

1. Check the created file:
   ```bash
   head -20 design/pdr/my-document.md
   ```

2. Validate and view errors:
   ```bash
   python scripts/eia_design_validate.py design/pdr/my-document.md --format text
   ```

3. Fix the frontmatter manually if needed.

---

## 6.3 Search Issues

### No Results Returned

**Symptom:** Search returns empty results when documents exist.

**Causes and solutions:**

1. **Wrong directory**
   ```bash
   # Check design directory location
   ls -la design/

   # Specify correct path
   python scripts/eia_design_search.py --design-dir /correct/path/design
   ```

2. **Documents have no frontmatter**
   ```bash
   # Check if files have frontmatter
   head -5 design/pdr/*.md
   ```

3. **Status filter too restrictive**
   ```bash
   # Try without status filter first
   python scripts/eia_design_search.py --type pdr
   ```

4. **Keyword not in title or content**
   ```bash
   # Try partial keyword
   python scripts/eia_design_search.py --keyword "auth"
   ```

### Search Errors on Valid UUID

**Symptom:** Error "Invalid UUID format" for valid-looking UUID.

**Cause:** UUID has invisible characters or wrong encoding.

**Solution:**

1. Check the exact UUID:
   ```bash
   python -c "print(repr('GUUID-20250129-0001'))"
   ```

2. Re-type the UUID manually instead of copy-paste.

---

## 6.4 Frontmatter Parsing Issues

### "Missing frontmatter opening delimiter"

**Symptom:** Validation reports no frontmatter even though file has it.

**Causes:**

1. **BOM (Byte Order Mark) before frontmatter**
   ```bash
   # Check for BOM
   head -c 3 design/pdr/doc.md | xxd
   # If you see "ef bb bf", there's a BOM
   ```

   **Fix:** Remove BOM:
   ```bash
   sed -i '1s/^\xEF\xBB\xBF//' design/pdr/doc.md
   ```

2. **Whitespace before opening `---`**
   ```bash
   # Check first line
   head -1 design/pdr/doc.md | cat -A
   ```

   **Fix:** Remove leading whitespace.

3. **Wrong dash characters**
   ```bash
   # Check dashes are ASCII hyphen-minus (0x2D)
   head -1 design/pdr/doc.md | xxd
   ```

   **Fix:** Replace with regular hyphens `---`.

### "Invalid format, expected 'key: value'"

**Symptom:** Frontmatter line not parsed correctly.

**Causes:**

1. **Missing colon**
   ```yaml
   # Wrong
   status draft

   # Correct
   status: draft
   ```

2. **Special characters in unquoted value**
   ```yaml
   # Wrong
   title: My: Document

   # Correct
   title: "My: Document"
   ```

3. **Tabs instead of spaces**
   ```yaml
   # Wrong (tab character)
   title:	"Test"

   # Correct (space)
   title: "Test"
   ```

---

## 6.5 Directory Structure Issues

### Type Mismatch Warning

**Symptom:** Warning about type not matching folder.

**Cause:** Document's `type` field differs from parent directory name.

**Solution:**

Either move the file:
```bash
mv design/pdr/my-feature.md design/feature/my-feature.md
```

Or update the frontmatter:
```yaml
# If file is in design/pdr/
type: pdr  # Change this to match directory
```

### Document in Wrong Directory

**Symptom:** PDR document in spec/ directory or similar.

**Cause:** Manual file creation in wrong location.

**Solution:**

1. Identify correct directory based on document type
2. Move the file:
   ```bash
   mv design/spec/my-pdr.md design/pdr/my-pdr.md
   ```
3. Update the `type` field in frontmatter if needed

---

## 6.6 Permission Issues

### Cannot Create Files

**Symptom:** "Permission denied" when creating documents.

**Solution:**

```bash
# Check ownership
ls -la design/

# Fix ownership (replace USER with your username)
sudo chown -R USER:USER design/

# Fix permissions
chmod -R 755 design/
```

### Cannot Read Files

**Symptom:** Search/validation fails to read existing files.

**Solution:**

```bash
# Make files readable
chmod 644 design/**/*.md
```

---

## 6.7 Encoding Issues

### UnicodeDecodeError

**Symptom:** Script fails with encoding error.

**Cause:** File not saved as UTF-8.

**Solution:**

1. Check encoding:
   ```bash
   file design/pdr/doc.md
   ```

2. Convert to UTF-8:
   ```bash
   iconv -f ISO-8859-1 -t UTF-8 design/pdr/doc.md > design/pdr/doc-utf8.md
   mv design/pdr/doc-utf8.md design/pdr/doc.md
   ```

### Special Characters Corrupted

**Symptom:** Characters like ` ` or emojis appear as `???` or garbage.

**Cause:** Editor saved file with wrong encoding.

**Solution:**

1. Re-save file as UTF-8 from your editor
2. Or use a tool:
   ```bash
   # Install uchardet if needed
   uchardet design/pdr/doc.md
   # Convert based on detected encoding
   ```

---

## General Debugging Tips

### Enable Verbose Output

Most scripts support verbose output:
```bash
python scripts/eia_design_validate.py --all --verbose --format text
```

### Check Script Location

Scripts expect to be run from the plugin root:
```bash
# Correct
cd /path/to/emasoft-integrator-agent
python scripts/eia_design_create.py --type pdr --title "Test"

# Also correct (explicit path)
python scripts/eia_design_create.py \
  --type pdr \
  --title "Test" \
  --design-dir /explicit/path/to/design
```

### Validate After Any Manual Edit

Always validate after manually editing frontmatter:
```bash
python scripts/eia_design_validate.py design/pdr/my-doc.md
```

---

## See Also

- [UUID Specification](uuid-specification.md) - UUID format details
- [Validating Documents](validating-documents.md) - Validation error reference
- [Creating Documents](creating-documents.md) - Proper document creation
