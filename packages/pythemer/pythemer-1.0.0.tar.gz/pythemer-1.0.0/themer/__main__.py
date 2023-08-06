# THEMER #
# __main__.py #
# COPYRIGHT (c) Jaidan 2022- #

# Imports #
import click
from themer.theme import (activate_theme, deactivate_theme)

__author__ = "Jaidan"

@click.group()
def main():
    '''A WIP theme engine for macOS, written in Python.'''
    pass

@main.command()
@click.argument('path', type=click.Path(exists=True))
def activate(path):
    '''Activate a theme.'''
    activate_theme(path)

@main.command()
@click.argument('path', type=click.Path(exists=True))
def deactivate(path):
    '''Deactivate a theme.'''
    deactivate_theme(path)

if __name__ == "__main__":
    main()