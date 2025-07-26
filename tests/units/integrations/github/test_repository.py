"""Test Github repository API."""

import os
import uuid

import pytest

from pep503_simple_repo_broker.integrations.abstracts import IntegrationId
from pep503_simple_repo_broker.integrations.github.repository import (
    GithubRepository,
    GithubRepositoryApi,
)
from pep503_simple_repo_broker.integrations.github.types import (
    GithubRepositoryReference,
    GithubToken,
)


class TestGithubRepositoryApi:
    """Test Github repository API."""

    @pytest.mark.skipif(os.getenv("GITHUB_TOKEN", "") == "", reason="GITHUB_TOKEN is not set")
    @pytest.mark.asyncio
    async def test_retrieve_releases(self, github_token: GithubToken, repository: GithubRepositoryReference) -> None:
        """Test retrieve releases."""
        github_repository_api = GithubRepositoryApi(github_token, repository)
        releases = await github_repository_api.retrieve_releases()
        assert releases is not None
        assert len(releases) > 0


class TestGithubRepository:
    """Test Github repository."""

    @pytest.mark.skipif(os.getenv("GITHUB_TOKEN", "") == "", reason="GITHUB_TOKEN is not set")
    @pytest.mark.asyncio
    async def test_get_index(self, github_token: GithubToken, repository: GithubRepositoryReference) -> None:
        """Test get index."""
        github_repository = GithubRepository(
            integration_id=IntegrationId(uuid.uuid4()),
            github_token=github_token,
            repository=repository,
        )
        index = await github_repository.get_index()
        assert index is not None
        assert len(index) > 0
