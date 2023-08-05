from abc import ABC, abstractmethod

from flask import Flask


class ZHook(ABC):
    @abstractmethod
    def execute(self, app: Flask, **kwargs):
        pass


class NotFoundHook(ZHook):
    def execute(self, app: Flask, **kwargs):
        @app.errorhandler(404)
        def not_found(e):
            return "Resource requested not found", 404

        return super().execute(app)
