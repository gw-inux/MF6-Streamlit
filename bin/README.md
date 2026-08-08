# MODFLOW executable

Before deploying, place the **Linux** MODFLOW 6 executable here as:

```
bin/mf6
```

Recommended: from the repository root run:

```bash
python download_mf6.py
```

This downloads the official approved USGS MODFLOW 6.7.0 Linux release and
extracts its `bin/mf6` executable into this directory. Commit `bin/mf6` to the
repository afterwards.

Do **not** use `mf6.exe`; Streamlit Community Cloud runs Debian Linux.
