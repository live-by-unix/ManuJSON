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

    def __init__(self):
        self.lines = []
        self.indent_level = 0
        self.in_array = False
        self.array_items = []

    def strip_comments(self, text):
        """Remove all comments from MJSON text."""
        # Remove multi-line comments /* */
        text = re.sub(r'/\*.*?\*/', '', text, flags=re.DOTALL)
        
        # Remove single-line comments (// and #)
        lines = text.split('\n')
        cleaned_lines = []
        for line in lines:
            # Handle // comments
            if '//' in line:
                # Check if // is inside a string
                in_string = False
                escape = False
                new_line = []
                for char in line:
                    if escape:
                        new_line.append(char)
                        escape = False
                        continue
                    if char == '\\':
                        escape = True
                        new_line.append(char)
                        continue
                    if char == '"' or char == "'":
                        in_string = not in_string
                        new_line.append(char)
                        continue
                    if not in_string and char == '/' and len(new_line) > 0 and new_line[-1] == '/':
                        new_line.pop()  # Remove the previous /
                        break  # Rest of line is comment
                    new_line.append(char)
                line = ''.join(new_line)
            
            # Handle # comments (only if not in string)
            in_string = False
            escape = False
            new_line = []
            for char in line:
                if escape:
                    new_line.append(char)
                    escape = False
                    continue
                if char == '\\':
                    escape = True
                    new_line.append(char)
                    continue
                if char == '"' or char == "'":
                    in_string = not in_string
                    new_line.append(char)
                    continue
                if not in_string and char == '#':
                    break  # Rest of line is comment
                new_line.append(char)
            line = ''.join(new_line)
            
            cleaned_lines.append(line)
        
        return '\n'.join(cleaned_lines)

    def normalize_shorthand(self, text):
        """Convert MJSON shorthand to JSON equivalents."""
        # yes/no → true/false
        text = re.sub(r'\byes\b', 'true', text)
        text = re.sub(r'\bno\b', 'false', text)
        
        # ~ → null
        text = re.sub(r'\b~\b', 'null', text)
        
        return text

    def remove_trailing_commas(self, text):
        """Remove trailing commas before ] or }."""
        # Remove commas before ] or }
        text = re.sub(r',(\s*[}\]])', r'\1', text)
        return text

    def quote_unquoted_strings(self, text):
        """Quote unquoted string values and keys."""
        # This is a simplified approach - we'll use a more robust method
        # by parsing and reconstructing
        return text

    def convert_yaml_arrays(self, text):
        """Convert YAML-style arrays to JSON arrays."""
        lines = text.split('\n')
        result = []
        i = 0
        
        while i < len(lines):
            line = lines[i]
            stripped = line.lstrip()
            
            # Check for YAML array item (- key: value)
            if stripped.startswith('- '):
                # Collect all consecutive array items
                array_items = []
                current_item = []
                base_indent = len(line) - len(stripped)
                
                while i < len(lines):
                    line = lines[i]
                    if line.strip() == '':
                        i += 1
                        continue
                    
                    line_indent = len(line) - len(line.lstrip())
                    
                    # New array item at same or less indent
                    if line.lstrip().startswith('- ') and line_indent <= base_indent:
                        if current_item:
                            array_items.append('\n'.join(current_item))
                        current_item = []
                        base_indent = line_indent
                    
                    # End of array (dedent past base)
                    if not line.lstrip().startswith('- ') and line_indent < base_indent:
                        if current_item:
                            array_items.append('\n'.join(current_item))
                        break
                    
                    current_item.append(line)
                    i += 1
                
                if current_item:
                    array_items.append('\n'.join(current_item))
                
                # Convert to JSON array
                json_objects = []
                for item in array_items:
                    # Remove the leading - and convert to object
                    obj_lines = []
                    for obj_line in item.split('\n'):
                        if obj_line.lstrip().startswith('- '):
                            # First line of item
                            rest = obj_line.lstrip()[2:]  # Remove '- '
                            obj_lines.append('  ' + rest)
                        else:
                            obj_lines.append(obj_line)
                    
                    # Wrap in braces and convert
                    obj_text = '{\n' + '\n'.join(obj_lines) + '\n}'
                    json_objects.append(obj_text)
                
                result.append('[' + ', '.join(json_objects) + ']')
            else:
                result.append(line)
                i += 1
        
        return '\n'.join(result)

    def quote_keys_and_values(self, text):
        """Quote unquoted keys and string values."""
        lines = text.split('\n')
        result = []
        
        for line in lines:
            if ':' in line and not line.strip().startswith('#'):
                parts = line.split(':', 1)
                if len(parts) == 2:
                    key = parts[0].strip()
                    value = parts[1].strip()
                    
                    # Quote key if not already quoted
                    if not (key.startswith('"') and key.endswith('"')) and not (key.startswith("'") and key.endswith("'")):
                        # Check if it's a valid identifier
                        if key.replace('_', '').replace('-', '').isalnum() or key.replace('_', '').replace('-', '').isidentifier():
                            key = f'"{key}"'
                    
                    # Quote value if it's an unquoted string
                    if value and not value.startswith('[') and not value.startswith('{') and not value in ['true', 'false', 'null']:
                        try:
                            # Try to parse as number
                            float(value)
                        except ValueError:
                            # Not a number, quote it if not already quoted
                            if not (value.startswith('"') and value.endswith('"')) and not (value.startswith("'") and value.endswith("'")):
                                value = f'"{value}"'
                    
                    result.append(f'{key}: {value}')
                else:
                    result.append(line)
            else:
                result.append(line)
        
        return '\n'.join(result)

    def wrap_root_in_braces(self, text):
        """Wrap root-level content in braces if not already wrapped."""
        text = text.strip()
        if not text.startswith('{'):
            text = '{\n' + text + '\n}'
        return text

    def transpile(self, mjson_text):
        """Convert MJSON text to JSON text."""
        # Step 1: Strip comments
        text = self.strip_comments(mjson_text)
        
        # Step 2: Normalize shorthand
        text = self.normalize_shorthand(text)
        
        # Step 3: Remove trailing commas
        text = self.remove_trailing_commas(text)
        
        # Step 4: Convert YAML-style arrays
        text = self.convert_yaml_arrays(text)
        
        # Step 5: Quote keys and values
        text = self.quote_keys_and_values(text)
        
        # Step 6: Wrap root in braces
        text = self.wrap_root_in_braces(text)
        
        return text


def transpile_file(input_path):
    """Transpile a .mjson file to .json."""
    input_path = Path(input_path)
    
    if not input_path.exists():
        print(f"Error: File not found: {input_path}")
        sys.exit(1)
    
    if input_path.suffix != '.mjson':
        print(f"Error: Input file must have .mjson extension")
        sys.exit(1)
    
    # Read MJSON file
    with open(input_path, 'r', encoding='utf-8') as f:
        mjson_content = f.read()
    
    # Transpile
    transpiler = MJSONTranspiler()
    json_content = transpiler.transpile(mjson_content)
    
    # Validate JSON
    try:
        json.loads(json_content)
    except json.JSONDecodeError as e:
        print(f"Error: Transpiled output is not valid JSON: {e}")
        print(f"Output:\n{json_content}")
        sys.exit(1)
    
    # Write JSON file
    output_path = input_path.with_suffix('.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(json_content)
    
    print(f"Successfully transpiled {input_path} to {output_path}")
    return output_path


def main():
    """Main entry point."""
    if len(sys.argv) != 2:
        print("Usage: python mjsonc.py /path/to/file.mjson")
        print("Produces /path/to/file.json")
        sys.exit(1)
    
    input_path = sys.argv[1]
    transpile_file(input_path)


if __name__ == '__main__':
    main()
