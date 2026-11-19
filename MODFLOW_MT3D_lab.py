"""Transport Lab launcher for the existing MF6-Streamlit repository.

Keep this file and MODFLOW_MT3D_lab beside the shared bin folder.
Local launch: python -m streamlit run MODFLOW_MT3D_lab.py
Community Cloud main file: MODFLOW_MT3D_lab/streamlit_app.py
The folder entry point lets Community Cloud use this lab's requirements.txt.
"""
from pathlib import Path
import runpy

APP_DIRECTORY = Path(__file__).resolve().parent / "MODFLOW_MT3D_lab"
runpy.run_path(str(APP_DIRECTORY / "streamlit_app.py"), run_name="__main__")
