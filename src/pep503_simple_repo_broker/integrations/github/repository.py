"""Github release API."""

from http import HTTPStatus

from aiohttp import ClientSession

from ..abstracts import IntegrationPackageIndex, PackageName, PackageVersion
from .objects import GithubReleaseObject
from .types import GithubRepositoryReference, GithubToken


class GithubRepositoryApi:
    """Github repository API."""

    GITHUB_API_BASE_URL: str = "https://api.github.com"

    def __init__(self, github_token: GithubToken, repository: GithubRepositoryReference) -> None:
        """Initialize Github release API."""
        self._github_token: GithubToken = github_token
        self._repository: GithubRepositoryReference = repository

    def acquire_session(self) -> ClientSession:
        """Acquire session."""
        return ClientSession(
            headers={"Authorization": f"Bearer {self._github_token}"},
            base_url=self.GITHUB_API_BASE_URL,
        )

    async def retrieve_releases(self) -> list[GithubReleaseObject]:
        """Retrieve releases."""
        url: str = f"/repos/{self._repository['namespace']}/{self._repository['name']}/releases"
        async with self.acquire_session() as session:
            async with session.get(url) as response:
                if response.status != HTTPStatus.OK:
                    raise Exception(f"Failed to retrieve releases: {response.status}")
                return [GithubReleaseObject.model_validate(release) for release in await response.json()]


def transform_release_to_package_version(release: GithubReleaseObject) -> list[PackageVersion]:
    """Transform release to package version."""
    package_version_list: list[PackageVersion] = []

    for asset in release.assets:
        if asset.name.endswith(".tar.gz") or asset.name.endswith(".whl"):
            package_version_list.append(PackageVersion(asset.name))

    return package_version_list


class GithubRepository:
    """Github repository."""

    def __init__(self, github_token: GithubToken, repository: GithubRepositoryReference) -> None:
        """Initialize Github release API."""
        self._github_token: GithubToken = github_token
        self._repository: GithubRepositoryReference = repository
        self._api: GithubRepositoryApi = GithubRepositoryApi(github_token, repository)

    async def get_index(self) -> IntegrationPackageIndex:
        """Get index."""
        releases: list[GithubReleaseObject] = await self._api.retrieve_releases()
        package_version_list: list[PackageVersion] = []
        for release in releases:
            package_version_list.extend(transform_release_to_package_version(release))
        package_name: PackageName = self._repository["package_name"] or PackageName(self._repository["name"])
        return {
            "package_name": package_name,
            "package_version_list": package_version_list,
        }
