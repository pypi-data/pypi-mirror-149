# THEMER #
# apps.py #
# COPYRIGHT (c) Jaidan 2022- #

# Imports #
from genericpath import exists
from os import remove
from themer.logger import logger
from themer.typedef import Plist

def __icon_backup_name(plist: Plist) -> str: return str(plist.resource_path + '/' + plist.name + '-' + plist.icon_asset + '-ORIGINAL.icns')

def check(plist: Plist) -> bool: 
    '''Check if an app's original icon has been backed up.'''
    try:
        return exists(__icon_backup_name(plist))
    except:
        logger.error('Could not check if {}\'s original icon has been backed up. ({})'.format(plist.name, plist.path))
        exit(1)

def backup(plist: Plist):
    '''Back up an app's original icon.'''
    try:
        # Check if it's already backed up #
        if check(plist): return
        # Get the app's icon #
        data = open(str(plist.resource_path + '/' + plist.icon_asset + '.icns'), 'rb').read()
        # Write to backup #
        open(__icon_backup_name(plist), 'wb').write(data)
        # Return #
        return
    except:
        logger.error('Unable to back up original icon for {}. ({})'.format(plist.name, plist.path))
        exit(1)

def enact_backup(plist: Plist):
    '''Recover an app's original icon.'''
    try:
        # Check #
        if not check(plist): return
        with open(str(plist.resource_path + '/' + plist.icon_asset + '.icns'), 'wb') as f:
            # Get backup #
            data = open(__icon_backup_name(plist), 'rb').read()
            # Write #
            f.write(data)
            # Delete backup #
            remove(__icon_backup_name(plist))
            # Close #
            f.close()
        # Return #
        return
    except:
        logger.error('Could not reset to original icon for {}. ({})'.format(plist.name, plist.path))
        exit(1)
