"""Github integration."""

import os
from typing import Generator

from fastapi.responses import StreamingResponse

from ..abstracts import AbstractIntegration, IntegrationPackageIndex, PackageName, PackageVersion
from .repository import GithubRepository
from .types import GithubRepositoryReference, GithubRepositorySlug, GithubToken, get_github_repository_slug


class GithubIntegration(AbstractIntegration):
    """Github integration."""

    def __init__(
        self,
        repositories: list[GithubRepositoryReference] | None = None,
    ) -> None:
        """Initialize Github integration."""
        # Github token
        github_token: str | None = os.getenv("GITHUB_TOKEN", None)
        if github_token is None:
            raise ValueError("GITHUB_TOKEN is not set")
        self._github_token: GithubToken = GithubToken(github_token)

        # Repositories
        self._repositories: dict[GithubRepositorySlug, GithubRepository] = {}
        if repositories is not None:
            for repository in repositories:
                slug: GithubRepositorySlug = get_github_repository_slug(repository["namespace"], repository["name"])
                if slug in self._repositories:
                    raise ValueError(f"Repository {slug} already exists")
                self._repositories[slug] = GithubRepository(self._github_token, repository)

    async def get_index(self) -> list[IntegrationPackageIndex]:
        """Get index."""
        index: list[IntegrationPackageIndex] = []
        for repository in self._repositories.values():
            index.append(await repository.get_index())
        return index

    async def get_download_package(
        self, package_name: PackageName, package_version: PackageVersion
    ) -> StreamingResponse:
        """Get download package."""

        def dummy() -> Generator[bytes, None, None]:
            """Dummy generator."""
            yield b"Hello, world!"

        return StreamingResponse(content=dummy())
