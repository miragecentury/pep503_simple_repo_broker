"""PEP503 Simple Repo Broker API."""

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, StreamingResponse

from .html_renderer import HtmlListItem, HtmlListRenderer
from .integrations.abstracts import AbstractIntegration, IntegrationPackageIndex, PackageName, PackageVersion

api_router: APIRouter = APIRouter(prefix="/simple")


def dependency_integrations(request: Request) -> list[AbstractIntegration]:
    """Dependency integrations."""
    return getattr(request.app.state, "integrations", [])


@api_router.get("/")
async def get_index(integrations: list[AbstractIntegration] = Depends(dependency_integrations)) -> HTMLResponse:
    """Get simple repo index."""
    index: list[IntegrationPackageIndex] = []
    for integration in integrations:
        index.extend(await integration.get_index())
    packages: list[PackageName] = [package_index["package_name"] for package_index in index]
    items: list[HtmlListItem] = [HtmlListItem(name=package, url=f"/simple/{package}") for package in packages]
    return HtmlListRenderer(title="Index").add_items(items).render()


@api_router.get("/{package_name}")
async def get_index_package(
    package_name: PackageName,
    integrations: list[AbstractIntegration] = Depends(dependency_integrations),
) -> HTMLResponse:
    """Get simple repo index package."""
    index: list[IntegrationPackageIndex] = []
    for integration in integrations:
        index.extend(await integration.get_index())
    package_index: IntegrationPackageIndex | None = next(
        (package_index for package_index in index if package_index["package_name"] == package_name), None
    )
    if package_index is None:
        raise HTTPException(status_code=404, detail="Package not found")

    items: list[HtmlListItem] = [
        HtmlListItem(name=package_version, url=f"/simple/{package_name}/{package_version}")
        for package_version in package_index["package_version_list"]
    ]

    return HtmlListRenderer(title=package_name).add_items(items).render()


async def get_download_package(
    package_name: PackageName,
    package_version: PackageVersion,
    integrations: list[AbstractIntegration] = Depends(dependency_integrations),
) -> StreamingResponse:
    """Get download package."""
    index: list[IntegrationPackageIndex] = []
    for integration in integrations:
        index.extend(await integration.get_index())
