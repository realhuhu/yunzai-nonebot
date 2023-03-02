from pathlib import Path

import nonebot

from .hijack import hijack_driver, hijack_logger, hijack_adapter
from .server import create_servicer


def init(config_path: Path):
    hijack_logger()
    driver = hijack_driver(config_path)
    adapter_v11, adapter_v12 = hijack_adapter()
    driver.register_adapter(adapter_v11)
    # driver.register_adapter(adapter_v12)


def run(*args, **kwargs):
    nonebot.run(*args, **kwargs)
