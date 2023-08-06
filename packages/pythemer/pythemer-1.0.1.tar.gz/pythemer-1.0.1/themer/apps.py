# THEMER #
# apps.py #
# COPYRIGHT (c) Jaidan 2022- #

# Imports #
from os import getuid
from glob import glob
from plistlib import loads
from themer.elevate import elevate
from themer.logger import logger

async def plist(app_name: str, apps: list[dict]):
    '''Read an app's plist.'''
    app_obj = None
    for app in apps:
        if app.get('name') == app_name:
            app_obj = app
    if app_obj is None:
        return None
    try:
        with open(app_obj.get('path') + '/Contents/Info.plist', 'rb') as f:
            try:
                plist = loads(f.read())
            except:
                logger.error('Could not parse {}\'s Info.plist.'.format(app_name))
                exit(1)
    except:
        logger.error('Error reading {}\'s Info.plist'.format(app_name))
        exit(1)
    try:
        return_value = {
            'CFBundleName': plist.get('CFBundleName'),
            'CFBundleIconFile': plist.get('CFBundleIconFile'),
            'CFBundleTypeIconFile': plist.get('CFBundleTypeIconFile'),
            'CFBundleExecutable': plist.get('CFBundleExecutable'),
            'AppPath': app_obj.get('path')
        }
    except:
        logger.error('Error reading {}\'s Info.plist'.format(app_name))
        exit(1)
    
    return return_value

def get_apps() -> list[dict]:
    '''Get all installed apps.'''
    try:
        apps = []
        if getuid() != 0:
            logger.info('Requesting root privileges to read and modify system applications.')
            elevate()
        for app in glob('/System/Applications/*.app'): apps.append({'name': app.split('/')[-1].replace('.app', ''), 'path': app})
        for app in glob('/Applications/*.app'): apps.append({'name': app.split('/')[-1].replace('.app', ''), 'path': app})
        for app in glob('/Applications/*/*.app'): apps.append({'name': app.split('/')[-1].replace('.app', ''), 'path': app})
        return apps
    except:
        logger.error('Could not get app list.')
        exit(1)