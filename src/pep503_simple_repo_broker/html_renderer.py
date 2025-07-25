"""HTML Renderer Package."""

from abc import ABC
from typing import Self, TypedDict

from fastapi.responses import HTMLResponse


class AbstractHtmlRenderer(ABC):
    """Abstract HTML Renderer."""

    @classmethod
    def build_html(cls, body: str, head: str) -> str:
        """Build HTML."""
        return f"<!DOCTYPE html><html lang='en'><head>{head}</head><body>{body}</body></html>"


class HtmlListItem(TypedDict):
    """HTML List Item."""

    name: str
    url: str


class HtmlListRenderer(AbstractHtmlRenderer):
    """HTML List Renderer."""

    def __init__(self, title: str | None = None) -> None:
        """Initialize HTML List Renderer."""
        self.items: list[HtmlListItem] = []
        self.title: str | None = title

    def add_items(self, items: list[HtmlListItem]) -> Self:
        """Add items to HTML List Renderer."""
        self.items.extend(items)
        return self

    def add_item(self, item: HtmlListItem) -> Self:
        """Add item to HTML List Renderer."""
        self.items.append(item)
        return self

    def build_body(self) -> str:
        """Build HTML List Body."""
        return "".join([f"<a href='{item['url']}'>{item['name']}</a>" for item in self.items])  # pylint: disable=inconsistent-quotes

    def build_head(self) -> str:
        """Build HTML List Head."""
        return f"<title>{self.title}</title>" if self.title else ""

    def render(self) -> HTMLResponse:
        """Render HTML List Renderer."""
        return HTMLResponse(
            content=self.build_html(
                body=self.build_body(),
                head=self.build_head(),
            )
        )
