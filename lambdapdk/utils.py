import subprocess
import os.path
import glob


def format_verilog(path: str, verible_bin: str):
    """Format Verilog files using Verible."""
    if os.path.isfile(path):
        paths = [os.path.abspath(path)]
    elif os.path.isdir(path):
        paths = glob.glob(os.path.join(path, '*.v'))
        paths.extend(glob.glob(os.path.join(path, '*.vh')))

    for f in paths:
        print(f"Formatting: {f}")
        subprocess.run([verible_bin, '--inplace', f])
