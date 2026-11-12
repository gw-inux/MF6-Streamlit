"""ModFlow Newton Lab entry point for the shared MF6-Streamlit repository.

Keep this file beside the MODFLOW_Newton_lab folder.
Run: python -m streamlit run MODFLOW_Newton_lab.py
The shared requirements.txt can include: -r MODFLOW_Newton_lab/requirements.txt
"""

from pathlib import Path
import sys

# Resolve support files relative to this launcher, independently of the working
# directory. Keep the application's existing package and resource paths intact.
APP_DIRECTORY = str(Path(__file__).resolve().parent / "MODFLOW_Newton_lab")
if APP_DIRECTORY not in sys.path:
    sys.path.insert(0, APP_DIRECTORY)

from newton_lab.app import main  # noqa: E402

main()
