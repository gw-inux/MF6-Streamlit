"""Download the official USGS MODFLOW 6.7.0 Linux executable for deployment.

Run this script ONCE on your local computer from the repository root:

    python download_mf6.py

It downloads the approved MODFLOW 6.7.0 Linux release from the official
MODFLOW-ORG GitHub repository and copies only the ``mf6`` executable to
``bin/mf6``. Commit ``bin/mf6`` to GitHub afterwards.

The Streamlit app does NOT run this downloader during normal operation. This is
intentional: deployment should not depend on an external download being
available each time the app starts.
"""

from __future__ import annotations

from pathlib import Path
import os
import shutil
import stat
import tempfile
import urllib.request
import zipfile

MF6_VERSION = "6.7.0"
DOWNLOAD_URL = (
    "https://github.com/MODFLOW-ORG/modflow6/releases/download/"
    f"{MF6_VERSION}/mf6.{MF6_VERSION}_linux.zip"
)
ARCHIVE_MEMBER = f"mf6.{MF6_VERSION}_linux/bin/mf6"
TARGET = Path(__file__).resolve().parent / "bin" / "mf6"


def main() -> None:
    TARGET.parent.mkdir(parents=True, exist_ok=True)

    print(f"Downloading MODFLOW {MF6_VERSION} Linux release...")
    print(DOWNLOAD_URL)

    with tempfile.TemporaryDirectory(prefix="mf6_download_") as tmp:
        archive = Path(tmp) / "mf6_linux.zip"
        urllib.request.urlretrieve(DOWNLOAD_URL, archive)

        with zipfile.ZipFile(archive) as zf:
            names = set(zf.namelist())
            if ARCHIVE_MEMBER not in names:
                raise RuntimeError(
                    "Expected executable was not found in the downloaded archive: "
                    f"{ARCHIVE_MEMBER}"
                )
            with zf.open(ARCHIVE_MEMBER) as src, TARGET.open("wb") as dst:
                shutil.copyfileobj(src, dst)

    if os.name != "nt":
        mode = TARGET.stat().st_mode
        TARGET.chmod(mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

    print(f"Saved: {TARGET}")
    print(f"Size: {TARGET.stat().st_size / 1024 / 1024:.2f} MB")
    print("\nNext step: commit bin/mf6 to your GitHub repository and redeploy.")


if __name__ == "__main__":
    main()
