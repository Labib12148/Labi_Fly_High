import sys
import os
from cx_Freeze import setup, Executable

SETUP_DIR = os.path.dirname(sys.executable)
os.environ['TCL_LIBRARY'] = os.path.join(SETUP_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(SETUP_DIR, 'tcl', 'tk8.6')

include_files = [
    (os.path.join(SETUP_DIR, 'DLLs', 'tk86t.dll'), os.path.join('lib', 'tk86.dll')),
    (os.path.join(SETUP_DIR, 'DLLs', 'tcl86t.dll'), os.path.join('lib', 'tcl86.dll')),
    ('assets', 'assets')
]
ICON_PATH = "assets\icon.ico"

base = "Win32GUI" if sys.platform == "win32" else None

executables = [Executable("Labi_Fly_High.py",base=base,icon= ICON_PATH,
                            shortcut_name="Labi Fly High",
                            shortcut_dir="DesktopFolder")]

setup(
    name="Labi Fly High",
    version="1.0.0",
    author="Sadman Labib",
    description="This is a game made with pygame. You might have seen a similar game called \"Flappy Bird\". It is Labi Fly High, my version of Flappy Bird.",
    options={"build_exe": {"include_files": include_files}},
    executables=executables
)
