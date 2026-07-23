# ManuScriptJSON (MJSON)

**ManuScriptJSON (MJSON)** is a human-friendly superset of JSON designed for readability and ease of editing. Think of MJSON as Markdown is to HTML — expressive, forgiving, but always compiles back to strict machine format.

## Introduction

JSON is excellent for machine-to-machine communication but can be tedious for humans to write and maintain. MJSON addresses these pain points by providing a more ergonomic syntax while maintaining full compatibility with JSON through compilation.

### Philosophy

MJSON is to JSON what Markdown is to HTML:

- **Expressive** — Write configuration files naturally with comments and shorthand
- **Forgiving** — Trailing commas, unquoted keys, and flexible formatting
- **Compatible** — Always compiles to strict, standards-compliant JSON
- **Human-first** — Designed for people to read and edit

Every MJSON file can be transpiled into valid JSON, ensuring you get the best of both worlds: human-friendly editing and machine-readable output.

## Features

### Comments
Document your configuration inline with three comment styles:

```mjson
# Single-line hash comment
key: "value"  # Inline comment

// C-style single-line comment
debug: yes

/*
 * Multi-line comments
 * for detailed documentation
 */
```

### Shorthand Syntax
Reduce visual noise with convenient shorthand:

```mjson
# Booleans
active: yes      # compiles to true
deleted: no      # compiles to false

# Null
value: ~         # compiles to null
```

### Trailing Commas
Add or remove items without syntax errors:

```mjson
tags: [javascript, python, rust,]
```

### Unquoted Keys
Less visual noise for simple identifiers:

```mjson
name: "Alice"
age: 25
city: "San Francisco"
```

### YAML-Style Arrays
Cleaner object lists with dash notation:

```mjson
users:
  - name: "Alice"
    role: "admin"
  - name: "Bob"
    role: "user"
```

### Brace-less Objects
Optional outer braces for simple structures:

```mjson
name: "MyApp"
version: "1.0.0"
port: 8080
```

## Installation

### Prerequisites
- Python 3.6 or higher
- No external dependencies (uses Python standard library only)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/live-by-unix/manujson.git
cd manujson
```

2. The transpiler is ready to use:
```bash
python mjsonc.py /path/to/file.mjson
```

3. (Optional) Make it executable:
```bash
chmod +x mjsonc.py
```

## Usage

### Basic Transpilation

Convert a `.mjson` file to `.json`:

```bash
python mjsonc.py config.mjson
```

This produces `config.json` in the same directory.

### Example: Input MJSON

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

### Example: Output JSON

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

## Examples

### Configuration File

**config.mjson:**
```mjson
# Server Configuration
server:
  host: "localhost"
  port: 3000
  ssl: no

# Database Settings
database:
  name: "mydb"
  user: "admin"
  password: ~  # Use environment variable

# Feature Flags
features:
  - name: "authentication"
    enabled: yes
  - name: "rate-limiting"
    enabled: no
```

**config.json (compiled):**
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
  },
  "features": [
    {"name": "authentication", "enabled": true},
    {"name": "rate-limiting", "enabled": false}
  ]
}
```

### Data Fixture

**users.mjson:**
```mjson
# Seed data for testing
users:
  - id: 1
    name: "Alice Johnson"
    email: "alice@example.com"
    active: yes
  - id: 2
    name: "Bob Smith"
    email: "bob@example.com"
    active: yes
  - id: 3
    name: "Charlie Brown"
    email: "charlie@example.com"
    active: no
```

## Compilation Rules

The transpiler applies these transformations:

1. **Strip Comments** — Remove `#`, `//`, and `/* */` comments
2. **Normalize Booleans** — `yes` → `true`, `no` → `false`
3. **Normalize Null** — `~` → `null`
4. **Remove Trailing Commas** — Strip commas before `]` or `}`
5. **Quote Keys** — Wrap unquoted keys in double quotes
6. **Quote String Values** — Wrap unquoted string values in double quotes
7. **Convert YAML-Style Arrays** — Transform `- key: value` into `[{"key": "value"}]`
8. **Wrap Root in Braces** — Add outer `{}` if root is brace-less
9. **Validate Output** — Ensure result is valid JSON via `json.loads()`

## Documentation

For a complete syntax guide with examples and practice exercises, see [manujsonguide.md](manujsonguide.md).

## Roadmap

### Phase 1: Core (Current)
- ✅ Basic syntax support
- ✅ Comment stripping
- ✅ Shorthand normalization
- ✅ YAML-style arrays
- ✅ Transpiler CLI tool

### Phase 2: Enhanced
- ⏳ Schema annotations (embed type hints, version info)
- ⏳ Error-tolerant parsing (auto-fix missing commas, quotes)
- ⏳ Domain-specific extensions (dates, units, enums)
- ⏳ Editor integration (syntax highlighting, linting)

### Phase 3: Ecosystem
- ⏳ Multi-format converters (mjson → yaml, mjson → toml)
- ⏳ Validation tools
- ⏳ Schema generation
- ⏳ Documentation site

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

**live-by-unix**

## Acknowledgments

- Inspired by the elegance of Markdown for HTML
- Built for developers who value human-readable configuration
