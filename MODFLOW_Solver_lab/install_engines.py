"""Explicit, platform-aware installation of the tested MODFLOW distribution."""

# BEGIN CODE CONTENTS
# Manual edits: jump to these release line numbers (refresh with tools/update_code_map.py).
#   main: line 16
# END CODE CONTENTS

import argparse
import hashlib
import json
import platform
from pathlib import Path
import flopy


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--with-api", action="store_true", help="Also install libmf6 for optional outer-head recording")
    parser.add_argument("--release", default="30.0", help="MODFLOW-ORG/executables release; default 30.0 was tested")
    parser.add_argument("--bin", default=str(Path(__file__).resolve().parent / "bin"))
    args = parser.parse_args()
    folder = Path(args.bin).resolve()
    folder.mkdir(parents=True, exist_ok=True)
    subset = {"mf2005", "mf2005dbl", "mfnwt", "mfnwtdbl", "mf6"}
    if args.with_api:
        subset.add("libmf6")
    # Pin the distribution for reproducibility; allow an explicit later release.
    flopy.utils.get_modflow(folder, release_id=args.release, subset=subset)
    manifest = dict(release=args.release, platform=platform.platform(), flopy=flopy.__version__, files={})
    for path in sorted(folder.iterdir()):
        if path.is_file() and path.name != "installation.json":
            manifest["files"][path.name] = hashlib.sha256(path.read_bytes()).hexdigest()
    (folder / "installation.json").write_text(json.dumps(manifest, indent=2))
    print("Installed in", folder)
    print("Start with: python -m streamlit run app.py")


if __name__ == "__main__":
    main()
