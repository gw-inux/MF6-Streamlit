"""Isolated, optional capture of actual MODFLOW 6 outer-solve head vectors."""

# BEGIN CODE CONTENTS
# Manual edits: jump to these release line numbers (refresh with tools/update_code_map.py).
#   main: line 14
# END CODE CONTENTS

import sys
from pathlib import Path
import numpy as np
from modflowapi import ModflowApi


def main(library, directory):
    mf = ModflowApi(str(Path(library).resolve()), working_directory=str(Path(directory).resolve()))
    mf.initialize()
    try:
        address = mf.get_var_address("X", "FLOW")
        maximum = int(mf.get_value(mf.get_var_address("MXITER", "SLN_1"))[0])
        mf.prepare_time_step(mf.get_time_step())
        mf.prepare_solve(1)
        heads = [mf.get_value(address).copy()]
        converged = False
        for _ in range(maximum):
            converged = mf.solve(1)
            heads.append(mf.get_value(address).copy())
            if converged:
                break
        mf.finalize_solve(1)
        mf.finalize_time_step()
        np.savez_compressed(Path(directory) / "snapshots.npz", heads=np.asarray(heads),
                            iterations=np.arange(len(heads)), converged=np.array(bool(converged)),
                            version=np.array(mf.get_version()))
    finally:
        mf.finalize()


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
