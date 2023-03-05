from pathlib import Path

import nonebot

from .hijack import hijack_driver, hijack_logger, hijack_adapter, hijack_params


def init(config_path: Path):
    hijack_logger()
    hijack_params()
    driver = hijack_driver(config_path)
    adapter = hijack_adapter()
    driver.register_adapter(adapter)


def run(*args, **kwargs):
    nonebot.run(*args, **kwargs)
