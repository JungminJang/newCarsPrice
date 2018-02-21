import sys
from cx_Freeze import setup, Executable

build_exe_options = dict(
        includes=["sys", "bs4", "datetime", "requests", "shutil", "os", "time", "queue", "idna"],
        packages=['idna'],
        include_files=[]
)

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "newCars",
        version = "1.0",
        description = "Parser",
        author = "Kai",
        options = {"build_exe": build_exe_options},
        executables = [Executable("newCarGenesis.py", base = base, targetName="Genesis.exe")]
)