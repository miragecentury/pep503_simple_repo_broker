"""Application."""

import os
from typing import Any

import uvicorn
from fastapi import FastAPI

from .integrations.abstracts import AbstractIntegration, PackageName
from .integrations.github import GithubIntegration, GithubNamespace, GithubRepositoryName


class Application:
    """Application."""

    def setup_integrations(self) -> list[AbstractIntegration]:
        """Setup integrations.

        TODO: Load integrations from configuration file or environment variables.
        """
        return [
            GithubIntegration(
                [
                    {
                        "namespace": GithubNamespace(os.getenv("GITHUB_NAMESPACE", "")),
                        "name": GithubRepositoryName(os.getenv("GITHUB_REPOSITORY_NAME", "")),
                        "package_name": PackageName(os.getenv("GITHUB_PACKAGE_NAME", "")),
                    }
                ]
            )
        ]

    def __init__(self, host: str | None = None, port: int | None = None) -> None:
        """Initialize Application."""
        # Configurations
        self._host = host or "0.0.0.0"
        self._port = port or 8000
        # Integrations
        self._integrations: list[AbstractIntegration] = self.setup_integrations()
        # Attributes
        self._fastapi_app = FastAPI()

        setattr(self._fastapi_app.state, "integrations", self._integrations)

        from .api import api_router  # pylint: disable=import-outside-toplevel # noqa: PLC0415

        self._fastapi_app.include_router(api_router)

    async def __call__(self, scope: Any, receive: Any, send: Any) -> None:
        """Forward the call to the FastAPI app."""
        return await self._fastapi_app.__call__(scope=scope, receive=receive, send=send)

    def run(self) -> None:
        """Run Application."""
        uvicorn.run(self, host=self._host, port=self._port)
