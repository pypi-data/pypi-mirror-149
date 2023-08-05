from typing import Any, List, Optional, Dict
from flask_cors import CORS

from flask import Flask

from zpy.api.flask.zhooks import ZHook
from zpy.api.flask.zmiddlewares import ZMiddleware


def create_flask_app(
        config: dict,
        path_cors_allow: str = None,
        origins: List[str] = None
) -> Flask:
    """
    Flask app builder
    """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config)
    path_allow = "/*" if path_cors_allow is None or path_cors_allow == '' else path_cors_allow
    _origins = '*' if origins is None or len(origins) <= 0 else origins
    CORS(app, resources={path_allow: {"origins": _origins}})
    return app


def create_app(app: Optional[Flask] = None,
               mw: Optional[List[ZMiddleware]] = None,
               mw_args: Optional[List[Any]] = None,
               hk: Optional[List[ZHook]] = None,
               hk_args: Optional[List[Any]] = None,
               shared_data: Dict[Any, Any] = None,
               path_cors_allow: str = None,
               origins_cors: List[str] = None
               ) -> Flask:
    """
    API App Builder
    @param app: Flask application instance.
    @param mw:  Middlewares
    @param mw_args:  Middleware arguments
    @param hk: Hooks
    @param hk_args: hooks arguments
    @param shared_data: data for setup in flask context
    @param path_cors_allow: Path for configure cors origins. Default: '/*'
    @param origins_cors: Origins for configure cors. Default '*'
    @return:  flask instance
    """
    if hk_args is None:
        hk_args = []
    if mw_args is None:
        mw_args = []
    if shared_data is None:
        shared_data = {}
    if hk is None:
        hk = []
    if mw is None:
        mw = []
    if app is None:
        app = create_flask_app(shared_data, path_cors_allow, origins_cors)

    for i, m in enumerate(mw):
        args = mw_args[i] if i < len(mw_args) else {}
        args.update(shared_data)
        app.wsgi_app = m(app.wsgi_app, **args)
    for i, h in enumerate(hk):
        args = hk_args[i] if i < len(hk_args) else {}
        args.update(shared_data)
        h().execute(app, **args)

    return app
