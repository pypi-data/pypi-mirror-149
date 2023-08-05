#!/usr/bin/env python3

"""
    SPDX-FileCopyrightText: 2022 Senne Van Baelen
    SPDX-License-Identifier: Apache-2.0
"""

import os
import logging
import pathlib

GENERAL_FORMATTER = logging.Formatter(fmt="[%(levelname)s \
- %(module)s (%(asctime)s)] %(message)s")

INFO_FORMATTER = logging.Formatter(fmt="[%(levelname)s \
- %(module)s] %(message)s")


def get_logger(name, log_level="INFO", logfile=None):

    """ initialise or re-configure logger """

    # remove old handlers
    logger = logging.getLogger(name)    # e.g. root logger
    for hdlr in logger.handlers[:]:     # remove all old handlers
        logger.removeHandler(hdlr)

    handler = None
    if not logfile:
        handler = logging.StreamHandler()
    else:
        cwd = os.getcwd()
        logpath = pathlib.Path(cwd, logfile)
        print(f"Redirecting all logs to {logpath}")
        handler = logging.FileHandler(logpath, 'a')

    logger.addHandler(handler)

    if log_level == "DEBUG":
        logger.setLevel(logging.DEBUG)
        handler.setFormatter(GENERAL_FORMATTER)
    elif log_level == "INFO":
        logger.setLevel(logging.INFO)
        handler.setFormatter(INFO_FORMATTER)
    elif log_level == "WARNING":
        logger.setLevel(logging.WARNING)
        handler.setFormatter(GENERAL_FORMATTER)
    elif log_level == "ERROR":
        logger.setLevel(logging.ERROR)
        handler.setFormatter(GENERAL_FORMATTER)

    return logger
