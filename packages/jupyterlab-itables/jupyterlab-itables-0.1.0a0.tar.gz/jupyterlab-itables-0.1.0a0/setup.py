from pathlib import Path
from setuptools import setup
from jupyter_packaging import (
    wrap_installers,
    npm_builder,
)


NAME = "jupyterlab_itables"
here = Path(__file__).absolute().parent
version = "0.1.0a0"

jstargets = [
    here.joinpath(NAME, "static", "jquery", "LICENSE.txt"),
    here.joinpath(NAME, "static", "jquery", "dist", "jquery.js"),
    here.joinpath(NAME, "static", "datatables.net-dt", "License.txt"),
    here.joinpath(NAME, "static", "datatables.net-dt", "css", "jquery.dataTables.min.css"),
    here.joinpath(NAME, "static", "datatables.net-dt", "js", "dataTables.dataTables.min.js"),
    here.joinpath(NAME, "static", "datatables.net-dt", "types", "dataTables.dataTables.d.ts")
]

# Handle datafiles
builder = npm_builder(here)
cmdclass = wrap_installers(
    pre_develop=builder,
    pre_dist=builder,
    ensured_targets=jstargets
)

setup_args = dict(
    version=version,
    cmdclass=cmdclass,
)

if __name__ == "__main__":
    setup(**setup_args)
