"""Github objects."""

from pydantic import BaseModel


class GithubReleaseAssetObject(BaseModel):
    """Github release asset object."""

    url: str
    name: str
    digest: str
    browser_download_url: str
    content_type: str


class GithubReleaseObject(BaseModel):
    """Github release object."""

    tag_name: str
    name: str
    assets: list[GithubReleaseAssetObject]
