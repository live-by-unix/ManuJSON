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
            line = re.split(r'(?<!["\'])#', line)[0]
            line = re.split(r'(?<!["\'])//', line)[0]
            lines.append(line)
        return '\n'.join(lines)

    def normalize_shorthand(self, text):
        text = re.sub(r'\byes\b', 'true', text)
        text = re.sub(r'\bno\b', 'false', text)
        text = re.sub(r'\b~\b', 'null', text)
        return text

    def parse_value(self, v):
        v = v.strip()
        if v in ('true', 'false', 'null'):
            return json.loads(v)
        try:
            return int(v)
        except ValueError:
            try:
                return float(v)
            except ValueError:
                if v.startswith('[') and v.endswith(']'):
                    inner = v[1:-1].strip()
                    if not inner:
                        return []
                    return [self.parse_value(x.strip().strip(',')) for x in inner.split(',') if x.strip()]
                return v.strip('"')

    def parse(self, text):
        """Parse MJSON into Python objects using indentation."""
        lines = [l for l in text.split('\n') if l.strip()]
        root = {}
        stack = [(0, root)]

        for line in lines:
            indent = len(line) - len(line.lstrip())
            content = line.strip()

            # Array item
            if content.startswith('- '):
                kv = content[2:]
                item = {}
                if ':' in kv:
                    k, v = kv.split(':', 1)
                    item[k.strip()] = self.parse_value(v.strip())
                # Find nearest list container
                while stack and not isinstance(stack[-1][1], list):
                    stack.pop()
                if not stack:
                    raise ValueError("Array item without parent list")
                stack[-1][1].append(item)
                stack.append((indent, item))
                continue

            # Key: value
            if ':' in content:
                k, v = content.split(':', 1)
                k = k.strip()
                v = v.strip()
                val = self.parse_value(v) if v else {}
                # Dedent
                while stack and indent < stack[-1][0]:
                    stack.pop()
                container = stack[-1][1]
                if isinstance(container, dict):
                    container[k] = val
                elif isinstance(container, list):
                    container[-1][k] = val
                if isinstance(val, dict):
                    stack.append((indent, val))
                elif isinstance(val, list):
                    stack.append((indent, val))
        return root

    def transpile(self, mjson_text):
        text = self.strip_comments(mjson_text)
        text = self.normalize_shorthand(text)
        data = self.parse(text)
        return json.dumps(data, indent=2)


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
