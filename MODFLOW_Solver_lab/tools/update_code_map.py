"""Refresh the release line-number contents in the app modules and CODE_MAP.md.

Run after manual edits: python tools/update_code_map.py
Only generated comment blocks and CODE_MAP.md are rewritten.
"""

# BEGIN CODE CONTENTS
# Manual edits: jump to these release line numbers (refresh with tools/update_code_map.py).
#   ROOT: line 23
#   FILES: line 24
#   BEGIN: line 29
#   END: line 30
#   PATTERN: line 31
#   entries: line 34
#   refresh: line 55
#   main: line 76
# END CODE CONTENTS

import ast
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
FILES = ('__init__.py', 'app.py', 'inputs.py', 'results.py', 'studies.py', 'surfaces.py', 'ui.py',
         'spacing.py', 'diagnostic_guides.py', 'map_rendering.py',
         'core.py', 'settings.py', 'controls.py', 'plots.py',
         'content.py', 'experiments.py', 'assessments.py', 'checklists.py', 'streamlit_app.py', 'install_engines.py', 'api_worker.py',
         'tools/update_code_map.py', '../MODFLOW_Solver_lab.py')
BEGIN = '# BEGIN CODE CONTENTS'
END = '# END CODE CONTENTS'
PATTERN = re.compile(r'(?:\A|\n)# BEGIN CODE CONTENTS.*?# END CODE CONTENTS\n', re.S)


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
    document = ['# Code map — MODFLOW Solver Lab', '',
        'These line numbers match this release. Open the named file and use your',
        "editor's Go to line command. Each Python module also starts with its own contents.", '',
        'Common edits: solver defaults and cell limit in `core.py`; widget labels and',
        'page order in `app.py`; input layout in `inputs.py`; execution and inspection',
        'in `results.py`; grid studies in `studies.py`; surface selection in `surfaces.py`;',
        'web colours in `ui.py`; figures and marker thinning in `plots.py`;',
        'integer spacing steps in `spacing.py`; closure markers in `diagnostic_guides.py`;',
        'the bounded computed-map image cache in `map_rendering.py`;',
        'Markdown text in `assets/md/en/` (see `CONTENT_GUIDE.md`); loading in `content.py`.',
        'Guided experiment tabs and the document-only route in `experiments.py`.',
        'iNUX question blocks in `assessments.py`; Markdown task rendering in `checklists.py`.',
        'The commented FIGS example is in `app.py`. Native construction remains in `build_model`.', '',
        'After manual changes, refresh these references with:', '',
        '```sh', 'python tools/update_code_map.py', '```', '']
    files = (*FILES, *(str(path.relative_to(ROOT)) for path in sorted((ROOT/'tests').glob('*.py'))))
    for name in files:
        document += [f'## {name}', '', '| Editing location | Line |', '|---|---:|']
        document += [f'| `{label}` | {number} |' for number,label in refresh(ROOT/name)]
        document.append('')
    (ROOT/'CODE_MAP.md').write_text('\n'.join(document), encoding='utf-8')
    print('Updated contents and CODE_MAP.md for', len(files), 'Python files.')


if __name__ == '__main__':
    main()
