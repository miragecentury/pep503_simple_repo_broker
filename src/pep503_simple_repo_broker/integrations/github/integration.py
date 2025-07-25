"""Github integration."""

import os
import uuid
from collections.abc import AsyncGenerator

from fastapi import HTTPException
from fastapi.responses import StreamingResponse

from ..abstracts import AbstractIntegration, IntegrationId, IntegrationPackageIndex, PackageName, PackageVersion
from .repository import GithubRepository
from .types import GithubRepositoryReference, GithubRepositorySlug, GithubToken, get_github_repository_slug


class GithubIntegration(AbstractIntegration):
    """Github integration."""

    def __init__(
        self,
        repositories: list[GithubRepositoryReference] | None = None,
    ) -> None:
        """Initialize Github integration."""
        self._integration_id: IntegrationId = IntegrationId(uuid.uuid4())
        # Github token
        github_token: str | None = os.getenv("GITHUB_TOKEN", None)
        if github_token is None:
            raise ValueError("GITHUB_TOKEN is not set")
        self._github_token: GithubToken = GithubToken(github_token)

        # Repositories
        self._repositories: dict[GithubRepositorySlug, GithubRepository] = {}
        self._indexes_by_slug: dict[GithubRepositorySlug, IntegrationPackageIndex] = {}
        if repositories is not None:
            for repository in repositories:
                slug: GithubRepositorySlug = get_github_repository_slug(repository["namespace"], repository["name"])
                if slug in self._repositories:
                    raise ValueError(f"Repository {slug} already exists")
                self._repositories[slug] = GithubRepository(self._github_token, repository, self._integration_id)

    @property
    def id(self) -> IntegrationId:
        """Get integration id."""
        return self._integration_id

    async def populate_indexes(self) -> None:
        """Populate indexes."""
        for slug, repository in self._repositories.items():
            self._indexes_by_slug[slug] = await repository.get_index()

    async def get_index(self) -> list[IntegrationPackageIndex]:
        """Get index."""
        await self.populate_indexes()
        return list(self._indexes_by_slug.values())

    async def get_download_package(
        self, package_name: PackageName, package_version: PackageVersion
    ) -> AsyncGenerator[bytes, None]:
        """Get download package."""
        # Identify the repository slug based on the package name
        repository_slug: GithubRepositorySlug | None = next(
            (slug for slug, index in self._indexes_by_slug.items() if index["package_name"] == package_name), None
        )
        if repository_slug is None:
            raise HTTPException(status_code=404, detail="Repository not found")

        # Identify the package version based on the package name and version
        package_version_list: list[PackageVersion] = self._indexes_by_slug[repository_slug]["package_version_list"]
        if package_version not in package_version_list:
            raise HTTPException(status_code=404, detail="Package version not found")

        return await self._repositories[repository_slug].get_download_package(package_name, package_version)
