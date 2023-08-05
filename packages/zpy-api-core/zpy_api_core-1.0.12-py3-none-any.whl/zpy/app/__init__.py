# Created by Noé Cruz | Zurckz 22 at 05/03/2022
# See https://www.linkedin.com/in/zurckz
import logging
from typing import Optional
from zpy.utils import get_env

from zpy.logger import zL, ZLFormat, ZLogger


class ZContext(object):

    def __init__(self, logger: Optional[ZLogger] = None):
        self.logger = logger
        self.app_name = get_env("APP_NAME", "Z-API")
        if not logger:
            self.logger = zL(self.app_name, logging.INFO, ZLFormat.LM)

    def release_logger(self, name: str = "Z-API"):
        self.logger.release(name)


context: Optional[ZContext] = None


def setup_context(ctx: Optional[ZContext] = None) -> ZContext:
    global context
    if ctx:
        context = ctx
    if not ctx:
        context = ZContext()
    return context


def zapp_context() -> ZContext:
    global context
    if not context:
        return setup_context()
    return context
