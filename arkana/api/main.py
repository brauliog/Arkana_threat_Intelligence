from importlib.metadata import version

from fastapi import FastAPI

from arkana.api.routes import health

app = FastAPI(
    title="Arkana Threat Intelligence",
    version=version("arkana"),
)

app.include_router(health.router)
