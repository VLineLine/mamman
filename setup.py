import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os", "queue"],
                     'include_files': [('res/logo.png', 'res/logo.png'), ('res/logo_red.png', 'res/logo_red.png')],
					 'bin_path_includes': ['res'],
                     }#, "excludes": ["tkinter"]}
					 
base = None
if sys.platform == "win32":
    base = "Win32GUI"

# GUI applications require a different base on Windows (the default is for a
# console application).
#base = None
#if sys.platform == "win32":
#    base = "Win32GUI"

setup(  name = "mamman",
        version = "0.1",
        description = "LTS AS - Mamman",
        options = {"build_exe": build_exe_options},
        executables = [Executable("main.py")])
