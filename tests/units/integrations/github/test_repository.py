"""Test Github repository API."""

import pytest

from pep503_simple_repo_broker.integrations.github.repository import GithubRepository, GithubRepositoryApi
from pep503_simple_repo_broker.integrations.github.types import (
    GithubRepositoryReference,
    GithubToken,
)


class TestGithubRepositoryApi:
    """Test Github repository API."""

    @pytest.mark.asyncio
    async def test_retrieve_releases(self, github_token: GithubToken, repository: GithubRepositoryReference) -> None:
        """Test retrieve releases."""
        github_repository_api = GithubRepositoryApi(github_token, repository)
        releases = await github_repository_api.retrieve_releases()
        assert releases is not None
        assert len(releases) > 0


class TestGithubRepository:
    """Test Github repository."""

    @pytest.mark.asyncio
    async def test_get_index(self, github_token: GithubToken, repository: GithubRepositoryReference) -> None:
        """Test get index."""
        github_repository = GithubRepository(github_token, repository)
        index = await github_repository.get_index()
        assert index is not None
        assert len(index) > 0
