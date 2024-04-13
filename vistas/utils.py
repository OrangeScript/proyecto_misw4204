import os

from vistas import constants

ASSETS_PATH = constants.ASSETS_PATH

def get_asset_path(type, name):
    try:
        project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        return os.path.join(project_path, ASSETS_PATH, type, name)
    except Exception as e:
        print(f"\nError getting asset path: {e}")
        return None