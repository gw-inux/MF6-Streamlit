"""Refresh the release line-number contents in the app modules and CODE_MAP.md.

Run after manual edits: python tools/update_code_map.py
Only generated comment blocks and CODE_MAP.md are rewritten.
"""
import ast
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
FILES = ('app.py', 'core.py', 'settings.py', 'controls.py', 'plots.py',
         'content.py', 'streamlit_app.py', 'install_engines.py', 'api_worker.py')
BEGIN = '# BEGIN CODE CONTENTS'
END = '# END CODE CONTENTS'
PATTERN = re.compile(r'\n# BEGIN CODE CONTENTS.*?# END CODE CONTENTS\n', re.S)


def entries(text):
    """Locate definitions and explicit editing landmarks, in source order."""
    tree = ast.parse(text)
    found = []
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            found.append((node.lineno, node.name))
            if isinstance(node, ast.ClassDef):
                for child in node.body:
                    if isinstance(child, ast.FunctionDef):
                        found.append((child.lineno, f'{node.name}.{child.name}'))
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id.isupper():
                    found.append((node.lineno, target.id))
    for number, line in enumerate(text.splitlines(), 1):
        if line.startswith('# EDIT: ') or re.match(r'# [1-7] — ', line):
            found.append((number, line.removeprefix('# EDIT: ').removeprefix('# ')))
    return sorted(found)


def refresh(path):
    original = path.read_text(encoding='utf-8')
    plain = PATTERN.sub('\n', original)
    tree = ast.parse(plain)
    after = tree.body[0].end_lineno if ast.get_docstring(tree) else 0
    lines = plain.splitlines(keepends=True)
    # A stable number of comment lines makes one line-number update sufficient.
    placeholders = [f'#   {name}: line 0' for _, name in entries(plain)]
    # Canonical spacing makes repeated refreshes byte-for-byte idempotent.
    prefix = ''.join(lines[:after]).rstrip('\n')
    suffix = ''.join(lines[after:]).lstrip('\n')
    block = BEGIN+'\n# Manual edits: jump to these release line numbers (refresh with tools/update_code_map.py).\n'+'\n'.join(placeholders)+'\n'+END
    text = (prefix+'\n\n' if prefix else '')+block+'\n\n'+suffix
    found = entries(text)
    final_block = BEGIN+'\n# Manual edits: jump to these release line numbers (refresh with tools/update_code_map.py).\n'+'\n'.join(f'#   {name}: line {number}' for number,name in found)+'\n'+END
    final = text.replace(block, final_block, 1)
    assert entries(final) == found
    path.write_text(final, encoding='utf-8')
    return found


def main():
    document = ['# Code map — MODFLOW solver lab v1.9', '',
        'These line numbers match this release. Open the named file and use your',
        "editor's Go to line command. Each Python module also starts with its own contents.", '',
        'Common edits: solver defaults and cell limit in `core.py`; widget labels and',
        'layout in `app.py`; colours, marker thinning and figures in `plots.py`;',
        'teaching text in `content.py`. Native model construction remains in `build_model`.', '',
        'After manual changes, refresh these references with:', '',
        '```sh', 'python tools/update_code_map.py', '```', '']
    for name in FILES:
        document += [f'## {name}', '', '| Editing location | Line |', '|---|---:|']
        document += [f'| `{label}` | {number} |' for number,label in refresh(ROOT/name)]
        document.append('')
    (ROOT/'CODE_MAP.md').write_text('\n'.join(document), encoding='utf-8')
    print('Updated contents and CODE_MAP.md for', len(FILES), 'modules.')


if __name__ == '__main__':
    main()
