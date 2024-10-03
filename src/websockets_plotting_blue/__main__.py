"""Interface for ``python -m websockets_plotting_blue``."""

from argparse import ArgumentParser
from collections.abc import Sequence

import asyncpg
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from websockets_plotting_blue.plotting.router import router as PlottingRouter
from websockets_plotting_blue.routers.runs_router import router as runs_router
from websockets_plotting_blue.websockets.router import router as WebSocketRouter

from . import __version__

__all__ = ["main"]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5174", "ws://localhost:5174"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(runs_router, prefix="/runs")
app.include_router(WebSocketRouter, prefix="/sockets")
app.include_router(PlottingRouter, prefix="/plots")


async def get_db_connection():
    return await asyncpg.connect(dsn="postgres://user:password@localhost/dbname")


def main(args: Sequence[str] | None = None) -> None:
    """Argument parser for the CLI."""
    parser = ArgumentParser()
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=__version__,
    )
    parser.parse_args(args)
    import uvicorn

    uvicorn.run(app)


if __name__ == "__main__":
    main()
