"""MODFLOW Solver lab — entrypoint for the existing MF6-Streamlit repository.

Keep this file and the MODFLOW_Solver_lab folder beside the shared bin folder.
Start from the repository root: python -m streamlit run MODFLOW_Solver_lab.py

Contents for manual edits:
  Imports: line 11
  Application folder: line 14
  Launch the unchanged application: line 15
"""
from pathlib import Path
import runpy

APP_DIRECTORY = Path(__file__).resolve().parent / "MODFLOW_Solver_lab"
runpy.run_path(str(APP_DIRECTORY / "streamlit_app.py"), run_name="__main__")
