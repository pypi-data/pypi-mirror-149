from pathlib import Path
from shutil import rmtree, copytree

node_modules = Path(__file__).parent / "node_modules"
static = Path(__file__).parent / "jupyterlab_itables" / "static"

if static.exists():
    rmtree(static)

for library in ['jquery', 'datatables.net-dt']:
    copytree(node_modules / library, static / library)