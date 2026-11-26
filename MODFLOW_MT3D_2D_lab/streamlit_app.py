"""Load one consistent Cloud source revision, including after an in-place update.

The source-derived package name avoids stale imported helpers without deleting
modules that may still be used by another session or by an existing saved run.
Normal widget reruns reuse the same modules and class identities.
"""
from pathlib import Path
import hashlib
import importlib
import importlib.util
import inspect
import runpy
import sys

APP_DIRECTORY=Path(__file__).resolve().parent
REQUIRED_FILES=('__init__.py','app.py','transport_lab/__init__.py',
                'transport_lab/controls.py','transport_lab/plots.py')


def incomplete_update(files):
    import streamlit as st
    st.error('The deployed app files are incomplete or from different versions. '
             'Replace the entire MODFLOW_MT3D_2D_lab folder with the folder from '
             'one release ZIP, then reboot the app in Streamlit Community Cloud.')
    st.caption('Files to replace: '+', '.join(files))
    st.stop()


missing=[name for name in REQUIRED_FILES if not (APP_DIRECTORY/name).is_file()]
if missing:incomplete_update(missing)

digest=hashlib.sha256(str(APP_DIRECTORY).encode('utf-8'))
source_files=[APP_DIRECTORY/name for name in ('__init__.py','app.py','streamlit_app.py')]
source_files+=list((APP_DIRECTORY/'transport_lab').glob('*.py'))
for source in sorted(source_files):
    digest.update(source.relative_to(APP_DIRECTORY).as_posix().encode('utf-8')+b'\0')
    digest.update(source.read_bytes()+b'\0')
namespace='_mt3d2d_cloud_'+digest.hexdigest()[:24]
if namespace not in sys.modules:
    importlib.invalidate_caches()
    spec=importlib.util.spec_from_file_location(namespace,APP_DIRECTORY/'__init__.py',
                                              submodule_search_locations=[str(APP_DIRECTORY)])
    package=importlib.util.module_from_spec(spec)
    sys.modules[namespace]=package
    try:
        spec.loader.exec_module(package)
    except BaseException:
        sys.modules.pop(namespace,None)
        raise

controls=importlib.import_module(namespace+'.transport_lab.controls')
plots=importlib.import_module(namespace+'.transport_lab.plots')
incompatible=[]
if any(not callable(getattr(controls,name,None)) for name in
       ('model_inputs','navigation','panel','page_width_control','page_width_css','run_label_css')):
    incompatible.append('transport_lab/controls.py')
plume=getattr(plots,'plume_figure',None)
if not callable(plume) or not {'show_grid','relative'}.issubset(inspect.signature(plume).parameters):
    incompatible.append('transport_lab/plots.py')
if incompatible:incomplete_update(incompatible)

runpy.run_module(namespace+'.app',run_name='__main__')
