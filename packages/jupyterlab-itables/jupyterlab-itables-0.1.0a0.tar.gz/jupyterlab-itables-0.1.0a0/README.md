# A (tentative) Jupyter Lab extension for itables

This extension exposes the [jquery](https://jquery.com/) and 
[datatables.net](https://datatables.net/) libraries
as static libraries in Jupyter Lab.

The purpose of doing this is to allow the 
[itables](https://mwouts.github.io/itables) package to have an
[offline mode](https://github.com/mwouts/itables/issues/70) in Jupyter Lab.

Install it in the Python environment you use to launch Jupyter Lab with:
```shell
pip install jupyterlab-itables==0.1.0a0
```

Then relaunch Jupyter Lab with
```shell
jupyter lab
```

Assuming that Jupyter Lab is running on port 8888, you will be able to access the static files at e.g.
```shell
http://localhost:8888/static/itables/jquery/README.md
```

# How to develop this extension

You can create a minimal Jupyter Lab environment with
```shell
mamba env create --file environment.yml
```
or update it with
```shell
mamba env update --file environment.yml
```

Activate that environment with
```shell
conda activate jupyterlab_itables-dev
```

Then build the extension in development mode with
```shell
pip install -ve .
```

In development mode the extension needs to be enabled manually with:
```shell
jupyter server extension enable --py jupyterlab_itables
```

# How to release a new version manually

Clean the project files with
```shell
rm -rf node_modules jupyterlab_itables/static dist build package-lock.json
```

Upgrade the version number in `setup.py`, then:
```shell
python setup.py sdist bdist_wheel
```

Check the size and the contents of the `.tar.gz` file in the `dist` folder, 
and then upload it to [pypi](https://pypi.org/) with

```shell
twine upload
```