from .app import DataTablesExtension


def _jupyter_server_extension_points():
    return [
        {"module": "jupyterlab_itables", "app": DataTablesExtension},
    ]
