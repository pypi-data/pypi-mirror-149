# THEMER #
# logger.py #
# COPYRIGHT (c) Jaidan 2022- #

# Imports #
import logging
import radium as r

class Logger:
    def __init__(self):
        self.logger = logging.Logger(__name__)
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(r.Radium)

logger = Logger().logger