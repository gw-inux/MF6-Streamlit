"""Optional root launcher, matching the MT3D 1D lab layout."""
from pathlib import Path
import runpy
APP_DIRECTORY=Path(__file__).resolve().parent/"MODFLOW_MT3D_2D_lab"
runpy.run_path(str(APP_DIRECTORY/"streamlit_app.py"),run_name="__main__")
