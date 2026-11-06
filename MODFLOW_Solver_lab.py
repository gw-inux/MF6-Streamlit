"""MODFLOW Solver lab — entrypoint for the existing MF6-Streamlit repository.

Keep this file and the MODFLOW_Solver_lab folder beside the shared bin folder.
Start from the repository root: python -m streamlit run MODFLOW_Solver_lab.py
"""

# BEGIN CODE CONTENTS
# Manual edits: jump to these release line numbers (refresh with tools/update_code_map.py).
#   APP_DIRECTORY: line 15
# END CODE CONTENTS

from pathlib import Path
import runpy

APP_DIRECTORY = Path(__file__).resolve().parent / "MODFLOW_Solver_lab"
runpy.run_path(str(APP_DIRECTORY / "streamlit_app.py"), run_name="__main__")
