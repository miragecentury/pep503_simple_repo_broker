"""Fixtures."""

import os

import pytest

from pep503_simple_repo_broker.integrations.abstracts import PackageName
from pep503_simple_repo_broker.integrations.github.types import (
    GithubNamespace,
    GithubRepositoryName,
    GithubRepositoryReference,
    GithubToken,
)


@pytest.fixture
def github_token() -> GithubToken:
    """Github token."""
    return GithubToken(os.getenv("GITHUB_TOKEN", ""))


@pytest.fixture
def repository() -> GithubRepositoryReference:
    """Github repository."""
    package_name: PackageName | None = PackageName(os.getenv("GITHUB_PACKAGE_NAME", ""))
    if package_name == "":
        package_name = None

    return GithubRepositoryReference(
        namespace=GithubNamespace(os.getenv("GITHUB_NAMESPACE", "")),
        name=GithubRepositoryName(os.getenv("GITHUB_REPOSITORY_NAME", "")),
        package_name=package_name,
    )
