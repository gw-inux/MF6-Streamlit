"""Launch the Solver Lab as a package, avoiding generic module-name conflicts.

Keep all support files together in MODFLOW_Solver_lab, including __init__.py.
The numerical model and interface are shared with the local app.
"""

# BEGIN CODE CONTENTS
# Manual edits: jump to these release line numbers (refresh with tools/update_code_map.py).
#   APP_ROOT: line 18
#   PACKAGE_PARENT: line 23
# END CODE CONTENTS

from pathlib import Path
import runpy
import sys
import streamlit as st

APP_ROOT = Path(__file__).resolve().parent
if not (APP_ROOT / "__init__.py").is_file():
    st.error("Incomplete Solver Lab upload: __init__.py is missing. Replace the complete "
             "MODFLOW_Solver_lab folder from the latest ZIP, then reboot the app.")
    st.stop()
PACKAGE_PARENT = str(APP_ROOT.parent)
if PACKAGE_PARENT in sys.path:
    sys.path.remove(PACKAGE_PARENT)
sys.path.insert(0, PACKAGE_PARENT)
runpy.run_module("MODFLOW_Solver_lab.app", run_name="__main__")
