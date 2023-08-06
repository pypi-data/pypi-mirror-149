# THEMER #
# types.py #
# COPYRIGHT (c) Jaidan 2022- #

# Imports #
from asyncio import run
from themer.apps import (get_apps, plist)

class Plist():
    def __init__(self, app_name: str, app_list: list[dict]):
        # Plist #
        plist_obj = run(plist(app_name, app_list))
        # App name #
        self.name = app_name
        # App icon asset #
        self.icon_asset = str(plist_obj.get(
            'CFBundleIconFile')).replace('.icns', '') if plist_obj else None
        # App path #
        self.path = str(plist_obj.get('AppPath')) if plist_obj else None
        # App resource path #
        self.resource_path = self.path + '/Contents/Resources' if self.path else None
        # App executable
        self.executable = plist_obj.get('CFBundleExecutable') if plist_obj else None

class Icon():
    def __init__(self, dict: dict, apps: list[dict]):
        # App name #
        self.name = dict.get('name')
        # App icon relative path #
        self.img = dict.get('img')
        # App icon data #
        self.data = None
        # Plist #
        self.plist = Plist(dict.get('name'), apps)

class Theme():
    def __init__(self, dict: dict):
        # Theme name #
        self.name = dict.get('name')
        # Icons object #
        self.icons: list[Icon] = []
        # Icons #
        app_list = get_apps()
        for icon in dict.get('icons'):
            self.icons.append(Icon(icon, app_list))
