import logging
import sys

from datetime import datetime
from os.path import join

import os

from typing import Optional, NoReturn


def configure_logger(log_dir: Optional[str] = os.getcwd()) -> NoReturn:
    """Runs basic configuration for the workflow.
    """
    logger = logging.getLogger("pipeline").getChild("configuration")
    format = "%(asctime)s:%(name)s:%(levelname)s:%(message)s"

    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    log_filename = "{}.log".format(timestamp)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    filename = join(log_dir, log_filename)

    log_formatter = logging.Formatter(format)
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(log_formatter)

    logging.basicConfig(filename=filename, format=format, level=logging.INFO)
    logging.getLogger().addHandler(stream_handler)

    logger.info("Logging configurations finished.")
