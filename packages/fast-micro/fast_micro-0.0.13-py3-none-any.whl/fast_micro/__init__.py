import socket, time
import fast_micro.permission as permission
from typing import Callable, List, Optional
from fastapi import FastAPI, Request
from starlette.middleware import Middleware
from starlette_context import plugins
from starlette_context.middleware import RawContextMiddleware
from starlette_context.plugins.base import Plugin
from fast_micro.logger import setup_logging
from fast_micro.middleware import RequestEncrichMiddleware


def create_app(
        log_level: str = "INFO", 
        permission_handler: Callable[[Request, List[str]], bool] = None,
        skip_route_logging: List[str] = None, 
        health_url: str = "/health",
        middleware: List[Middleware] = None,
        context_plugins: List[Plugin] = None,
        logging_config: Optional[dict] = None
    ) -> FastAPI:

    setup_logging(log_level, logging_config)

    app_context_plugins = (
        plugins.RequestIdPlugin(),
        plugins.CorrelationIdPlugin(),
    )

    if permission_handler:
        permission.PERMISSION_FUNC = permission_handler

    if context_plugins:
        app_context_plugins = app_context_plugins + tuple(context_plugins)

    skip_route_logging = skip_route_logging if skip_route_logging else [health_url]
    app_middleware = [
        Middleware(RawContextMiddleware, plugins=app_context_plugins),
        Middleware(RequestEncrichMiddleware, skip_routes=skip_route_logging),
    ]
    
    if middleware:
        app_middleware.extend(middleware)
    
    app: FastAPI = FastAPI(middleware=app_middleware)

    @app.get(health_url)
    def _default_get_health():
        """Returns health information from the app
        """
        return {
            "hostname": socket.gethostname(),
            "status": "success",
            "timestamp": time.time()
        }

    return app