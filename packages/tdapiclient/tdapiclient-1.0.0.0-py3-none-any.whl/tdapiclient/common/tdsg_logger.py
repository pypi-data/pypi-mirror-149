"""
Unpublished work.
Copyright (c) 2022 by Teradata Corporation. All rights reserved.
TERADATA CORPORATION CONFIDENTIAL AND TRADE SECRET

Primary Owner: pt186002d@teradata.com
Secondary Owner:

This is internal logging file for tdsagemaker.
"""

import logging
import sys

# Create a formatter for the logger
formatter = logging.Formatter(
    '%(asctime)s %(levelname)s %(filename)s:%(lineno)s %(message)s')

# Use standard out for the stream handler
streamhandler = logging.StreamHandler(sys.stdout)
streamhandler.setFormatter(formatter)

logger = logging.getLogger(__name__)
logger.addHandler(streamhandler)

# Default level is INFO
logger.setLevel(logging.INFO)


def get_logger():
    """
        Private logging method for internal methods.

    PARAMETERS:
        None

    RETURNS:
        A tdsagemaker logger for logging messages.

    RAISES:
        None

    EXAMPLES:
        from tdsagemaker.common import logger
        logger = logger.get_logger()
        logger.error("Some error happened")
    """
    return logging.getLogger(__name__)
