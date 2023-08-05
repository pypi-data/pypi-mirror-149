# -*- coding: utf-8 -*-
"""libjson module

"""
import json
import logging
from typing import Any, Union

from libumccr.utils import load_package_if_found

logger = logging.getLogger(__name__)


def dumps(data: Any, encoder=None) -> str:
    if encoder:
        return json.dumps(data, cls=encoder)

    elif load_package_if_found("django"):
        import django.core.serializers.json as django_ser
        return json.dumps(data, cls=django_ser.DjangoJSONEncoder)

    try:
        return json.dumps(data)
    except TypeError as e:
        logger.warning(f"Forcing string serializer. Exception: {e}")
        return json.dumps(data, default=str)


def loads(data: Union[str, bytes], decoder=None) -> Any:
    if decoder:
        return json.loads(data, cls=decoder)

    return json.loads(data)
