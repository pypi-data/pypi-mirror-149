from fastapi import FastAPI

from .metrics_router import metrics_router
from .prometheus_middleware import PrometheusMiddleware


def fast_api():
    app = FastAPI()
    app.add_middleware(PrometheusMiddleware)
    app.add_route("/metrics", metrics_router)

    return app
