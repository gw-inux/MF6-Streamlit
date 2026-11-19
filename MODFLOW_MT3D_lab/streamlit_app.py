"""Run the Transport Lab with its own package namespace and dependency file.

Community Cloud main file: MODFLOW_MT3D_lab/streamlit_app.py
Shared Linux executables: bin/mf2005 and bin/mt3dms in the repository root.
"""
from pathlib import Path
import runpy
import sys

PACKAGE_PARENT = str(Path(__file__).resolve().parent.parent)
if PACKAGE_PARENT in sys.path:
    sys.path.remove(PACKAGE_PARENT)
sys.path.insert(0, PACKAGE_PARENT)
runpy.run_module("MODFLOW_MT3D_lab.app", run_name="__main__")
