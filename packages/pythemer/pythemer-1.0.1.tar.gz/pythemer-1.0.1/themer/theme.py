# THEMER #
# main.py #
# COPYRIGHT (c) Jaidan 2022- #

# Imports #
import zipfile
from os import (system, unlink)
from themer.logger import logger
from themer.recovery import (backup, enact_backup)
from themer.typedef import Theme
from yaml import (FullLoader, load)

def unpack(path: str) -> dict:
    '''Unpacks a theme file and provides all of it's data.'''
    try:
        # Open zip file #
        with zipfile.ZipFile(path, 'r') as zip:
            # Initialize theme object #
            theme_obj = None
            # Loop through files #
            for file in zip.filelist:
                # If the file ends with .yaml #
                if file.filename.endswith('.yml'):
                    # Get the directory in the zip #
                    directory = file.filename.split('/')[0]
                    # Read the yaml #
                    yaml_obj = load(zip.read(file).decode(
                        'utf-8'), Loader=FullLoader)
                    # Assign the theme object #
                    theme_obj = Theme(yaml_obj)
                    # Loop through icons #
                    for icon in theme_obj.icons:
                        try:
                            # Read icon data #
                            icon.data = zip.read(directory + '/' + icon.img)
                        except:
                            logger.error(
                                'Could not read {}\'s icon.'.format(icon.name))
                            exit(1)
            if theme_obj is None:
                logger.logger('Could not find theme manifest.')
                exit(1)
            else:
                # Return #
                return {'theme': theme_obj, 'zip': zip}
    except zipfile.BadZipFile:
        logger.error('Invalid zip file.')
        exit(1)
            
def refresh_cache():
    system('killall Finder')
    system('killall Dock')
            
def activate_theme(path: str):
    '''Activate a theme.'''
    # Get theme package #
    theme_pack = unpack(path)
    # Parse to object #
    theme: Theme = theme_pack.get('theme')
    # Print theme name #
    logger.info('Activating \'{}\'.'.format(theme.name))
    # Loop through icons #
    for icon in theme.icons:
        if icon.plist.icon_asset is None:
            continue
        # Make icon backup #
        backup(icon.plist)
        # Replace icon #
        with open(str(icon.plist.resource_path + '/' + icon.plist.icon_asset + '.icns'), 'wb') as img:
            img.write(icon.data)
            system('touch {}'.format(str(icon.plist.path.replace(' ', '\ '))))
            img.close()
    # Clear cache #
    logger.info('Refreshing cache...')
    refresh_cache()
    logger.info('Successfully activated \'{}\'.'.format(theme.name))
    
def deactivate_theme(path: str):
    '''Deactivate a theme.'''
    # Get theme package #
    theme_pack = unpack(path)
    # Parse to object #
    theme: Theme = theme_pack.get('theme')
    # Print theme name #
    logger.info('Deactivating \'{}\'.'.format(theme.name))
    # Loop through icons #
    for icon in theme.icons:
        if icon.plist.icon_asset is None:
            continue
        # Remove icon file #
        unlink(str(icon.plist.resource_path + '/' + icon.plist.icon_asset + '.icns'))
        # Enact icon backup #
        enact_backup(icon.plist)
        # Clear cache #
        system('touch {}'.format(str(icon.plist.path.replace(' ', '\ '))))
    # Clear cache #
    logger.info('Refreshing cache...')
    refresh_cache()
    logger.info('Successfully deactivated \'{}\'.'.format(theme.name))