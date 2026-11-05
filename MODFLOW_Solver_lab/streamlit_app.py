"""Streamlit Cloud entrypoint; physics and UI are shared with the local app."""

# BEGIN CODE CONTENTS
# Manual edits: jump to these release line numbers (refresh with tools/update_code_map.py).
#   APP_ROOT: line 12
# END CODE CONTENTS

from pathlib import Path
import runpy
import sys

APP_ROOT = Path(__file__).resolve().parent
if str(APP_ROOT) not in sys.path:
    sys.path.insert(0, str(APP_ROOT))
runpy.run_path(str(APP_ROOT / "app.py"), run_name="__main__")
