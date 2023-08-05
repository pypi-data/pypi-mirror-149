# -*- coding: utf-8 -*-
import logging
import sys
from importlib import util as importlib_util

logger = logging.getLogger(__name__)


def load_package_if_found(name):
    spec = importlib_util.find_spec(name)
    if name in sys.modules:
        logger.debug(f"{name!r} already in sys.modules")
        return True
    elif spec is not None:
        module = importlib_util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
        logger.debug(f"{name!r} has been imported")
        return True
    else:
        logger.debug(f"can't find the {name!r} module")
        return False
