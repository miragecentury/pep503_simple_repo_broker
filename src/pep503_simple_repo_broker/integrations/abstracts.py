"""Abstracts for integrations."""

from abc import ABC, abstractmethod
from typing import NewType, TypedDict

from fastapi.responses import StreamingResponse

PackageName = NewType("PackageName", str)
PackageVersion = NewType("PackageVersion", str)


class IntegrationPackageIndex(TypedDict):
    """Integration index."""

    package_name: PackageName
    package_version_list: list[PackageVersion]


class AbstractIntegration(ABC):
    """Abstract integration."""

    @abstractmethod
    async def get_index(self) -> list[IntegrationPackageIndex]:
        """Get index."""
        raise NotImplementedError("get_index not implemented")

    @abstractmethod
    async def get_download_package(
        self, package_name: PackageName, package_version: PackageVersion
    ) -> StreamingResponse:
        """Get download package."""
        raise NotImplementedError("get_download_package not implemented")
