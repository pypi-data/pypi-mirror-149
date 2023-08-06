# -*- coding: utf-8 -*-

from pathlib import Path

import json

from pydantic import BaseSettings
from typing import Dict, Any


def json_config_settings_source(settings: BaseSettings) -> Dict[str, Any]:
    """
    pydantic settings provider for JSON files
    :param settings:
    :return:
    """
    if settings.__config__.json_file is None:
        return {}
    path = Path(settings.__config__.json_file)
    if not path.exists():
        return {}
    return json.loads(path.read_text('utf-8'))
