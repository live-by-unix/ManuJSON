#!/usr/bin/env python3
"""
ManuScriptJSON (MJSON) Transpiler
Compiles .mjson files to strict .json format.

Usage:
    python mjsonc.py /path/to/file.mjson
    Produces /path/to/file.json
"""

import sys
import re
import json
from pathlib import Path


class MJSONTranspiler:
    """Transpiler for converting MJSON to JSON."""

    def strip_comments(self, text):
        """Remove all comments from MJSON text."""
        text = re.sub(r'/\*.*?\*/', '', text, flags=re.DOTALL)
        lines = []
        for line in text.split('\n'):
            # Remove // comments outside strings
            if '//' in line:
                in_string = False
                new_line = []
                for i, ch in enumerate(line):
                    if ch in ['"', "'"]:
                        in_string = not in_string
                    if not in_string and ch == '/' and i+1 < len(line) and line[i+1] == '/':
                        break
                    new_line.append(ch)
                line = ''.join(new_line)
            # Remove # comments outside strings
            if '#' in line:
                in_string = False
                new_line = []
                for ch in line:
                    if ch in ['"', "'"]:
                        in_string = not in_string
                    if not in_string and ch == '#':
                        break
                    new_line.append(ch)
                line = ''.join(new_line)
            lines.append(line)
        return '\n'.join(lines)

    def normalize_shorthand(self, text):
        text = re.sub(r'\byes\b', 'true', text)
        text = re.sub(r'\bno\b', 'false', text)
        text = re.sub(r'\b~\b', 'null', text)
        return text

    def remove_trailing_commas(self, text):
        return re.sub(r',(\s*[}\]])', r'\1', text)

    def convert_yaml_arrays(self, text):
        """Convert YAML-style arrays (- key: value) into JSON arrays."""
        lines = text.split('\n')
        result = []
        i = 0
        while i < len(lines):
            line = lines[i]
            if line.lstrip().startswith('- '):
                items = []
                while i < len(lines) and lines[i].lstrip().startswith('- '):
                    obj_line = lines[i].lstrip()[2:]
                    obj = '{' + obj_line + '}'
                    items.append(obj)
                    i += 1
                result.append('[' + ', '.join(items) + ']')
            else:
                result.append(line)
                i += 1
        return '\n'.join(result)

    def quote_keys_and_values(self, text):
        """Quote unquoted keys and string values."""
        lines = []
        for line in text.split('\n'):
            if ':' in line and not line.strip().startswith('#'):
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip()
                if not (key.startswith('"') and key.endswith('"')):
                    key = f'"{key}"'
                if value and not value.startswith(('true', 'false', 'null', '[', '{')) and not value.replace('.', '', 1).isdigit():
                    if not (value.startswith('"') and value.endswith('"')):
                        value = f'"{value}"'
                line = f'{key}: {value}'
            lines.append(line)
        return '\n'.join(lines)

    def insert_commas_between_properties(self, text):
        """Ensure commas between JSON object properties."""
        lines = text.split('\n')
        result = []
        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped and ':' in stripped and not stripped.endswith(','):
                j = i + 1
                while j < len(lines) and not lines[j].strip():
                    j += 1
                if j < len(lines):
                    nxt = lines[j].strip()
                    if nxt and not nxt.startswith(('}', ']')):
                        line = line + ','
            result.append(line)
        return '\n'.join(result)

    def wrap_root_in_braces(self, text):
        text = text.strip()
        if not text.startswith('{'):
            text = '{\n' + text + '\n}'
        return text

    def transpile(self, mjson_text):
        text = self.strip_comments(mjson_text)
        text = self.normalize_shorthand(text)
        text = self.remove_trailing_commas(text)
        text = self.convert_yaml_arrays(text)
        text = self.quote_keys_and_values(text)
        text = self.insert_commas_between_properties(text)
        text = self.wrap_root_in_braces(text)
        return text


def transpile_file(input_path):
    input_path = Path(input_path)
    if not input_path.exists():
        print(f"Error: File not found: {input_path}")
        sys.exit(1)
    if input_path.suffix != '.mjson':
        print("Error: Input file must have .mjson extension")
        sys.exit(1)

    with open(input_path, 'r', encoding='utf-8') as f:
        mjson_content = f.read()

    transpiler = MJSONTranspiler()
    json_content = transpiler.transpile(mjson_content)

    try:
        json.loads(json_content)
    except json.JSONDecodeError as e:
        print(f"Error: Transpiled output is not valid JSON: {e}")
        print(f"Output:\n{json_content}")
        sys.exit(1)

    output_path = input_path.with_suffix('.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(json_content)

    print(f"Successfully transpiled {input_path} to {output_path}")
    return output_path


def main():
    if len(sys.argv) != 2:
        print("Usage: python mjsonc.py /path/to/file.mjson")
        sys.exit(1)
    transpile_file(sys.argv[1])


if __name__ == '__main__':
    main()
