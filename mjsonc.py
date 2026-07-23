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
    def strip_comments(self, text):
        text = re.sub(r'/\*.*?\*/', '', text, flags=re.DOTALL)
        lines = []
        for line in text.split('\n'):
            line = re.split(r'(?<!["\'])#', line)[0]  # strip # outside strings
            line = re.split(r'(?<!["\'])//', line)[0] # strip // outside strings
            lines.append(line)
        return '\n'.join(lines)

    def normalize_shorthand(self, text):
        text = re.sub(r'\byes\b', 'true', text)
        text = re.sub(r'\bno\b', 'false', text)
        text = re.sub(r'\b~\b', 'null', text)
        return text

    def transpile(self, mjson_text):
        # Preprocess
        text = self.strip_comments(mjson_text)
        text = self.normalize_shorthand(text)

        # Use Python's YAML-like parsing trick:
        # Replace MJSON syntax with JSON-compatible
        lines = []
        for line in text.split('\n'):
            if ':' in line:
                key, val = line.split(':', 1)
                key = key.strip()
                val = val.strip()
                if not key.startswith('"'):
                    key = f'"{key}"'
                if val and not val.startswith(('true','false','null','[','{','"')) and not val.replace('.','',1).isdigit():
                    val = f'"{val}"'
                line = f'{key}: {val}'
            lines.append(line)

        # Join and wrap root
        body = '\n'.join(lines).strip()
        if not body.startswith('{'):
            body = '{\n' + body + '\n}'

        # Fix arrays of objects (YAML-style)
        body = re.sub(r'-\s*(.*)', r'{\1},', body)

        # Ensure commas between properties
        body = re.sub(r'("\w+": [^,\n]+)(\n\s*")', r'\1,\2', body)

        return body


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
        parsed = json.loads(json_content)
    except json.JSONDecodeError as e:
        print(f"Error: Transpiled output is not valid JSON: {e}")
        print(f"Output:\n{json_content}")
        sys.exit(1)

    output_path = input_path.with_suffix('.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(parsed, f, indent=2)

    print(f"Successfully transpiled {input_path} to {output_path}")
    return output_path


def main():
    if len(sys.argv) != 2:
        print("Usage: python mjsonc.py /path/to/file.mjson")
        sys.exit(1)
    transpile_file(sys.argv[1])


if __name__ == '__main__':
    main()
