from flask.wrappers import Request, Response
from abc import ABC, abstractmethod
from flask import Flask
from typing import Any

__author__ = "Noé Cruz | contactozurckz@gmail.com"
__copyright__ = "Copyright 2021, Small APi Project"
__credits__ = ["Noé Cruz", "Zurck'z"]
__license__ = "upax"
__version__ = "0.0.1"
__maintainer__ = "Noé Cruz"
__email__ = "contactozurckz@gmail.com"
__status__ = "Dev"


# Middlewares | Zurck'Z Middlware
# Base middleware for flask
class ZMiddleware(ABC):
    def __init__(self, app: Flask, **kwargs) -> None:
        super().__init__()
        self.app = app
        self.kwargs = kwargs

    @abstractmethod
    def __call__(self, environ: Any, start_response: Any) -> Any:
        return self.app(environ, start_response)


class ParserMiddleWare(ZMiddleware):
    """
    Default middleware for custom access response
    """

    def __init__(self, app: Flask, **kwargs):
        super().__init__(app, **kwargs)
        self.app = app

    def __call__(self, environ, start_response):
        request = Request(environ)
        return self.app(environ, start_response)
