import os

from vistas import constants

ASSETS_PATH = constants.ASSETS_PATH


def get_asset_path(type, name):
    try:
        project_path = "assets/"
        return f'{project_path}{type}/{name}'
    except Exception as e:
        print(f"\nError getting asset path: {e}")
        return None
