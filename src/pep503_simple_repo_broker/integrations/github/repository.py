"""Github release API."""

from http import HTTPStatus
from typing import AsyncGenerator

from aiohttp import ClientSession
from fastapi import HTTPException
from pydantic import HttpUrl

from ..abstracts import IntegrationId, IntegrationPackageIndex, PackageName, PackageVersion
from .objects import GithubReleaseObject
from .types import GithubRepositoryReference, GithubToken


class GithubRepositoryApi:
    """Github repository API."""

    GITHUB_API_BASE_URL: str = "https://api.github.com"

    def __init__(self, github_token: GithubToken, repository: GithubRepositoryReference) -> None:
        """Initialize Github release API."""
        self._github_token: GithubToken = github_token
        self._repository: GithubRepositoryReference = repository

    def acquire_session(self, base_url: str | None = None, headers: dict[str, str] | None = None) -> ClientSession:
        """Acquire session."""
        if base_url is None:
            base_url = self.GITHUB_API_BASE_URL
        if headers is None:
            headers = {}
        headers["Authorization"] = f"Bearer {self._github_token}"
        return ClientSession(
            headers=headers,
            base_url=base_url,
        )

    async def retrieve_releases(self) -> list[GithubReleaseObject]:
        """Retrieve releases."""
        url: str = f"/repos/{self._repository['namespace']}/{self._repository['name']}/releases"
        async with self.acquire_session() as session:
            async with session.get(url) as response:
                if response.status != HTTPStatus.OK:
                    raise Exception(f"Failed to retrieve releases: {response.status}")
                return [GithubReleaseObject.model_validate(release) for release in await response.json()]

    async def download_asset(self, url: str) -> AsyncGenerator[bytes, None]:
        """Download asset."""
        async with self.acquire_session(
            headers={"Accept": "application/octet-stream"},
        ) as session:
            async with session.get(url) as response:
                async for content in response.content:
                    yield content


def transform_release_to_package_version(release: GithubReleaseObject) -> list[PackageVersion]:
    """Transform release to package version."""
    package_version_list: list[PackageVersion] = []

    for asset in release.assets:
        if asset.name.endswith(".tar.gz") or asset.name.endswith(".whl"):
            package_version_list.append(PackageVersion(asset.name))

    return package_version_list


class GithubRepository:
    """Github repository."""

    def __init__(
        self, github_token: GithubToken, repository: GithubRepositoryReference, integration_id: IntegrationId
    ) -> None:
        """Initialize Github release API."""
        self._github_token: GithubToken = github_token
        self._repository: GithubRepositoryReference = repository
        self._integration_id: IntegrationId = integration_id
        self._api: GithubRepositoryApi = GithubRepositoryApi(github_token, repository)

    async def get_index(self) -> IntegrationPackageIndex:
        """Get index."""
        releases: list[GithubReleaseObject] = await self._api.retrieve_releases()
        package_version_list: list[PackageVersion] = []
        for release in releases:
            package_version_list.extend(transform_release_to_package_version(release))
        package_name: PackageName = self._repository["package_name"] or PackageName(self._repository["name"])
        return {
            "integration_id": self._integration_id,
            "package_name": package_name,
            "package_version_list": package_version_list,
        }

    async def get_download_package(
        self, package_name: PackageName, package_version: PackageVersion
    ) -> AsyncGenerator[bytes, None]:
        """Get download package."""
        releases: list[GithubReleaseObject] = await self._api.retrieve_releases()
        # we must retrieve the asset url from the release
        asset_url: str | None = None
        for release in releases:
            for asset in release.assets:
                if asset.name == package_version:
                    asset_url = asset.url
                    break
            if asset_url is not None:
                break
        if asset_url is None:
            raise HTTPException(status_code=404, detail="Package version not found")

        return self._api.download_asset(asset_url)
