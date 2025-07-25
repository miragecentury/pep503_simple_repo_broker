"""Abstracts for integrations."""

import uuid
from abc import ABC, abstractmethod
from collections.abc import AsyncGenerator
from typing import NewType, TypedDict

PackageName = NewType("PackageName", str)
PackageVersion = NewType("PackageVersion", str)
IntegrationId = NewType("IntegrationId", uuid.UUID)


class IntegrationPackageIndex(TypedDict):
    """Integration index."""

    integration_id: IntegrationId
    package_name: PackageName
    package_version_list: list[PackageVersion]


class AbstractIntegration(ABC):
    """Abstract integration."""

    @property
    @abstractmethod
    def id(self) -> IntegrationId:
        """Get integration id."""
        raise NotImplementedError("id not implemented")

    @abstractmethod
    async def get_index(self) -> list[IntegrationPackageIndex]:
        """Get index."""
        raise NotImplementedError("get_index not implemented")

    @abstractmethod
    async def get_download_package(
        self, package_name: PackageName, package_version: PackageVersion
    ) -> AsyncGenerator[bytes, None]:
        """Get download package."""
        raise NotImplementedError("get_download_package not implemented")
