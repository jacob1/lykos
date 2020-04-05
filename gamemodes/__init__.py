# Imports all custom and built-in gamemode definitions
# To implement custom roles, rename this file to __init__.py
import os.path
import glob
import importlib

# get built-in modes
import src.gamemodes

path = os.path.dirname(os.path.abspath(__file__))
search = os.path.join(path, "*.py")

for f in glob.iglob(search):
    f = os.path.basename(f)
    n, _ = os.path.splitext(f)
    if f.startswith("_"):
        continue
    importlib.import_module("." + n, package="gamemodes")

# Important: if this isn't defined, built-in gamemodes will
# be imported. Normally this isn't an issue, but if you
# are attempting to suppress the import of built-in modes
# then that might be an issue for you.
CUSTOM_MODES_DEFINED = True

