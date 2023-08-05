

import logging

from . import log
from . import config

from .domains import pip
pip.install(config)


def updater():
    logging.info("Executing EBS Updater")
    for domain_name in config.domains:
        domain = getattr(config, domain_name)
        domain.update()
    logging.info("Update Check Complete")


if __name__ == '__main__':
    updater()
