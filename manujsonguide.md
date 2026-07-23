# ManuScriptJSON (MJSON) Guide

## Overview

ManuScriptJSON (MJSON) is a human-friendly superset of JSON designed for readability and ease of editing. Think of MJSON as Markdown is to HTML — expressive, forgiving, but always compiles back to strict machine format.

### Why MJSON Exists

JSON is excellent for machine-to-machine communication but can be tedious for humans to write and maintain. MJSON addresses these pain points by:

- **Allowing comments** — Document your configuration inline
- **Supporting trailing commas** — Add/remove items without syntax errors
- **Enabling unquoted keys** — Less visual noise
- **Providing shorthand syntax** — `yes/no` for booleans, `~` for null
- **Supporting YAML-style arrays** — Cleaner object lists
- **Being brace-less at root** — Optional outer braces for simple structures

### Key Philosophy

MJSON is **always valid JSON after compilation**. Every MJSON file can be transpiled into strict, standards-compliant JSON. This means you get the best of both worlds: human-friendly editing and machine-readable output.

---

## Strings

### JSON
```json
{
  "name": "Alice",
  "description": "A developer"
}
```

### MJSON
```mjson
name: "Alice"
description: "A developer"
```

**Rules:**
- Strings can be quoted or unquoted if they don't contain special characters
- Unquoted strings cannot contain: `:`, `{`, `}`, `[`, `]`, `,`, `#`, whitespace
- Always quote strings with spaces or special characters

---

## Numbers

### JSON
```json
{
  "count": 42,
  "price": 19.99,
  "scientific": 1.5e10
}
```

### MJSON
```mjson
count: 42
price: 19.99
scientific: 1.5e10
```

**Rules:**
- Numbers work identically to JSON
- Supports integers, floats, and scientific notation

---

## Booleans and Null

### JSON
```json
{
  "active": true,
  "deleted": false,
  "value": null
}
```

### MJSON
```mjson
active: yes
deleted: no
value: ~
```

**Rules:**
- `yes` compiles to `true`
- `no` compiles to `false`
- `~` compiles to `null`
- Standard `true`/`false`/`null` also work

---

## Arrays

### JSON
```json
{
  "tags": ["javascript", "python", "rust"],
  "numbers": [1, 2, 3]
}
```

### MJSON
```mjson
tags: [javascript, python, rust,]
numbers: [1, 2, 3,]
```

**Rules:**
- Trailing commas are allowed in arrays
- Items can be unquoted strings if they don't contain special characters
- Arrays work identically to JSON otherwise

---

## Objects

### JSON
```json
{
  "user": {
    "name": "Bob",
    "age": 30
  }
}
```

### MJSON
```mjson
user:
  name: "Bob"
  age: 30
```

**Rules:**
- Objects can be brace-less (indentation-based)
- Keys don't need quotes if they're valid identifiers
- Colon separates key from value
- Nested objects use indentation (2 spaces recommended)

### With Braces (Optional)
```mjson
user: {
  name: "Bob"
  age: 30
}
```

---

## Array of Objects (YAML-Style Shorthand)

### JSON
```json
{
  "users": [
    {"name": "Alice", "age": 25},
    {"name": "Bob", "age": 30},
    {"name": "Charlie", "age": 35}
  ]
}
```

### MJSON
```mjson
users:
  - name: "Alice"
    age: 25
  - name: "Bob"
    age: 30
  - name: "Charlie"
    age: 35
```

**Rules:**
- Use `-` to denote array items
- Each `-` starts a new object in the array
- Indentation determines nesting
- Trailing commas not needed in this format

### Mixed Example
```mjson
config:
  - name: "production"
    port: 8080
    debug: no
  - name: "development"
    port: 3000
    debug: yes
```

---

## Comments

### JSON
```json
{
  "version": "1.0"
  // Comments not allowed in JSON
}
```

### MJSON
```mjson
# Single-line comments with hash
version: "1.0"  # Inline comments work too

// Double-slash comments also supported
debug: yes  // Enable debug mode

/*
 * Multi-line comments
 * are supported
 */
timeout: 30
```

**Rules:**
- `#` for single-line comments (shell-style)
- `//` for single-line comments (C-style)
- `/* */` for multi-line comments
- Comments are stripped during compilation

---

## Complete Example

### JSON
```json
{
  "name": "MyApp",
  "version": "1.0.0",
  "config": {
    "port": 8080,
    "debug": true,
    "features": ["auth", "logging", "cache"]
  },
  "users": [
    {"name": "Alice", "role": "admin"},
    {"name": "Bob", "role": "user"}
  ],
  "settings": {
    "timeout": null,
    "retries": 3
  }
}
```

### MJSON
```mjson
# Application Configuration
name: "MyApp"
version: "1.0.0"

config:
  port: 8080
  debug: yes
  features: [auth, logging, cache,]

# User definitions
users:
  - name: "Alice"
    role: "admin"
  - name: "Bob"
    role: "user"

settings:
  timeout: ~  # No timeout
  retries: 3
```

---

## Compilation Rules

MJSON → JSON transformations applied by the transpiler:

1. **Strip Comments**
   - Remove `#`, `//`, and `/* */` comments

2. **Normalize Booleans**
   - `yes` → `true`
   - `no` → `false`

3. **Normalize Null**
   - `~` → `null`

4. **Remove Trailing Commas**
   - Strip commas before `]` or `}`

5. **Quote Keys**
   - Wrap unquoted keys in double quotes

6. **Quote String Values**
   - Wrap unquoted string values in double quotes

7. **Convert YAML-Style Arrays**
   - Transform `- key: value` into `[{"key": "value"}]`

8. **Wrap Root in Braces**
   - Add outer `{}` if root is brace-less

9. **Validate Output**
   - Ensure result is valid JSON via `json.loads()`

---

## Practice Exercises

### Exercise 1: JSON → MJSON

Convert this JSON to MJSON:
```json
{
  "server": {
    "host": "localhost",
    "port": 3000,
    "ssl": false
  },
  "database": {
    "name": "mydb",
    "user": "admin",
    "password": null
  }
}
```

**Solution:**
```mjson
server:
  host: "localhost"
  port: 3000
  ssl: no

database:
  name: "mydb"
  user: "admin"
  password: ~
```

### Exercise 2: MJSON → JSON

Convert this MJSON to JSON:
```mjson
# Shopping list
items:
  - name: "Apples"
    quantity: 5
    price: 2.99
  - name: "Bread"
    quantity: 1
    price: 3.50

total: 18.45
paid: yes
```

**Solution:**
```json
{
  "items": [
    {"name": "Apples", "quantity": 5, "price": 2.99},
    {"name": "Bread", "quantity": 1, "price": 3.50}
  ],
  "total": 18.45,
  "paid": true
}
```

### Exercise 3: Advanced MJSON

Write MJSON for a configuration with:
- Comments explaining each section
- YAML-style array for environments
- Shorthand booleans and null
- Trailing commas in arrays

**Solution:**
```mjson
# Application Configuration
app_name: "MyService"  # Display name
version: "2.0.0"

# Environment configurations
environments:
  - name: "production"
    url: "https://api.example.com"
    debug: no
  - name: "staging"
    url: "https://staging.example.com"
    debug: yes
  - name: "local"
    url: "http://localhost:8080"
    debug: yes

# Feature flags
features: [auth, rate-limiting, caching,]

# Optional settings
api_key: ~  # Not set in development
timeout: 30
```

---

## Advanced Features

### Schema Annotations (Planned)

Future versions will support embedded type hints:

```mjson
# @type string
name: "Alice"
# @type integer
age: 25
# @type array<string>
tags: [developer, python,]
```

### Error-Tolerant Parsing (Planned)

The transpiler will auto-fix common mistakes:

- Missing commas between array items
- Unquoted keys with special characters
- Inconsistent indentation

### Domain-Specific Extensions (Planned)

Special syntax for common data types:

```mjson
created_at: @date "2024-01-15"
duration: @duration "5m"
size: @bytes "1GB"
enum: @enum "red|green|blue" "green"
```

### Editor Integration (Planned)

- Syntax highlighting for VS Code, Vim, Emacs
- Linting with real-time error detection
- Auto-completion for schema-annotated files

### Conversion Tools (Planned)

- `mjson → yaml` converter
- `mjson → toml` converter
- `json → mjson` converter (with formatting)

---

## Roadmap

### Phase 1: Core (Current)
- ✅ Basic syntax support
- ✅ Comment stripping
- ✅ Shorthand normalization
- ✅ YAML-style arrays
- ✅ Transpiler CLI tool

### Phase 2: Enhanced
- ⏳ Schema annotations
- ⏳ Error-tolerant parsing
- ⏳ Domain-specific extensions
- ⏳ Editor plugins

### Phase 3: Ecosystem
- ⏳ Multi-format converters
- ⏳ Validation tools
- ⏳ Schema generation
- ⏳ Documentation site

---

## Conclusion

MJSON bridges the gap between human-friendly configuration and machine-readable data. By adopting MJSON, you get:

- **Readability** — Cleaner, more maintainable configuration files
- **Flexibility** — Comments and shorthand for faster editing
- **Compatibility** — Always compiles to valid JSON
- **Adoption** — Easy migration from existing JSON files

Start using MJSON today for your configuration files, data fixtures, and any JSON data that humans need to read or edit.

For the transpiler tool and installation instructions, see the main README.md.
