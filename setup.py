# setup file
import sys
from cx_Freeze import setup, Executable
import os

#executables = [cx_Freeze.Executable("ATR2.py")]
base = None
if sys.platform == "win32":
    base = "Win32gui"


PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')

setup(
    name="ATRobots",
    options={"build_exe": {"packages": ["pygame", "time", "os", "pdb", "sys"],
                           "include_files": ["ATR2FUNC.py", "ATRLOCK.py", "atrobots.png",
                                                                     "graphix.py", "README.md", "SNIPER.AT2",
                                                                     "T-ROBOTS.bmp"]}},
    description="ATR2 Game",
    executables=[Executable("ATR2.py", base=base)],
    version="1.0.0"
    )
