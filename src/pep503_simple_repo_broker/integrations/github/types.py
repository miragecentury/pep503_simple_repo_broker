"""Github types."""

from typing import NewType, TypedDict

from ..abstracts import PackageName

GithubToken = NewType("GithubToken", str)
GithubNamespace = NewType("GithubNamespace", str)
GithubRepositoryName = NewType("GithubRepositoryName", str)
GithubRepositorySlug = NewType("GithubRepositorySlug", str)


def get_github_repository_slug(
    namespace: GithubNamespace, name: GithubRepositoryName
) -> GithubRepositorySlug:
    """Get github repository slug."""
    if namespace == "" or name == "":
        raise ValueError("Namespace and name must be set")
    return GithubRepositorySlug(f"{namespace}/{name}")


class GithubRepositoryReference(TypedDict):
    """Github repository."""

    namespace: GithubNamespace
    name: GithubRepositoryName
    package_name: PackageName | None
