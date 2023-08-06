import inspect
import pkgutil
import os
from pathlib import Path

solvers_path = os.environ.get("OPTILOG_SOLVERS", None)
if solvers_path:
    solvers_path = {Path(s) for s in solvers_path.split(":")}
else:
    solvers_path = set()
solvers_path.add((Path(__file__) / "../solvers").resolve())
solvers_path.add((Path.home() / ".optilog_solvers").resolve())
solvers_path = {str(x.as_posix()) for x in solvers_path}
os.environ["OPTILOG_SOLVERS"] = ":".join(solvers_path)

# Import pure-python modules/packages
from . import solverbinder

# import classes from extensions submodule
for name, obj in inspect.getmembers(solverbinder):
    if inspect.isclass(obj) and not name.startswith("_"):
        globals()[name] = obj

del inspect
del pkgutil