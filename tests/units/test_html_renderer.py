"""Test HTML Renderer."""

from unittest.mock import Mock, patch

from pep503_simple_repo_broker.html_renderer import (
    HtmlListItem,
    HtmlListRenderer,
)


class TestHtmlListIten:
    """Test HTML List Item TypedDict."""

    def test_html_list_item_creation(self) -> None:
        """Test creating HtmlListIten with required fields."""
        item: HtmlListItem = {"name": "Test Item", "url": "https://test.com"}
        assert item["name"] == "Test Item"
        assert item["url"] == "https://test.com"

    def test_html_list_item_type_hints(self) -> None:
        """Test that HtmlListIten has correct type hints."""
        # This test ensures the TypedDict is properly defined
        item: HtmlListItem = {"name": "Test", "url": "https://test.com"}
        assert isinstance(item["name"], str)
        assert isinstance(item["url"], str)


class TestHtmlListRenderer:
    """Test HTML List Renderer."""

    def test_init_with_title(self) -> None:
        """Test HtmlListRenderer initialization with title."""
        renderer = HtmlListRenderer(title="Test Title")
        assert renderer.title == "Test Title"
        assert renderer.items == []

    def test_init_without_title(self) -> None:
        """Test HtmlListRenderer initialization without title."""
        renderer = HtmlListRenderer()
        assert renderer.title is None
        assert renderer.items == []

    def test_add_item(self) -> None:
        """Test adding single item to renderer."""
        renderer = HtmlListRenderer()
        item: HtmlListItem = {"name": "Test Item", "url": "https://test.com"}

        result = renderer.add_item(item)

        assert result is renderer  # Test method chaining
        assert len(renderer.items) == 1
        assert renderer.items[0] == item

    def test_add_items(self) -> None:
        """Test adding multiple items to renderer."""
        renderer = HtmlListRenderer()
        items: list[HtmlListItem] = [
            {"name": "Item 1", "url": "https://item1.com"},
            {"name": "Item 2", "url": "https://item2.com"},
        ]

        result = renderer.add_items(items)

        assert result is renderer  # Test method chaining
        assert len(renderer.items) == 2
        assert renderer.items == items

    def test_add_items_empty_list(self) -> None:
        """Test adding empty list of items."""
        renderer = HtmlListRenderer()
        initial_items = renderer.items.copy()

        result = renderer.add_items([])

        assert result is renderer
        assert renderer.items == initial_items

    def test_build_body_empty_items(self) -> None:
        """Test building body with no items."""
        renderer = HtmlListRenderer()
        body = renderer.build_body()
        assert body == ""

    def test_build_body_single_item(self) -> None:
        """Test building body with single item."""
        renderer = HtmlListRenderer()
        item: HtmlListItem = {"name": "Test Item", "url": "https://test.com"}
        renderer.add_item(item)

        body = renderer.build_body()
        expected = "<a href='https://test.com'>Test Item</a>"
        assert body == expected

    def test_build_body_multiple_items(self) -> None:
        """Test building body with multiple items."""
        renderer = HtmlListRenderer()
        items: list[HtmlListItem] = [
            {"name": "Item 1", "url": "https://item1.com"},
            {"name": "Item 2", "url": "https://item2.com"},
        ]
        renderer.add_items(items)

        body = renderer.build_body()
        expected = "<a href='https://item1.com'>Item 1</a><a href='https://item2.com'>Item 2</a>"
        assert body == expected

    def test_build_head_with_title(self) -> None:
        """Test building head with title."""
        renderer = HtmlListRenderer(title="Test Title")
        head = renderer.build_head()
        assert head == "<title>Test Title</title>"

    def test_build_head_without_title(self) -> None:
        """Test building head without title."""
        renderer = HtmlListRenderer()
        head = renderer.build_head()
        assert head == ""

    def test_build_head_with_none_title(self) -> None:
        """Test building head with None title."""
        renderer = HtmlListRenderer(title=None)
        head = renderer.build_head()
        assert head == ""

    @patch("pep503_simple_repo_broker.html_renderer.HTMLResponse")
    def test_render_with_title_and_items(self, mock_html_response: Mock) -> None:
        """Test render method with title and items."""
        renderer = HtmlListRenderer(title="Test Title")
        item: HtmlListItem = {"name": "Test Item", "url": "https://test.com"}
        renderer.add_item(item)

        mock_response = Mock()
        mock_html_response.return_value = mock_response

        result = renderer.render()

        # Verify HTMLResponse was called with correct content
        mock_html_response.assert_called_once()
        call_args = mock_html_response.call_args
        assert call_args[1]["content"] == (
            "<!DOCTYPE html><html lang='en'><head><title>Test Title</title></head>"
            "<body><a href='https://test.com'>Test Item</a></body></html>"
        )
        assert result == mock_response

    @patch("pep503_simple_repo_broker.html_renderer.HTMLResponse")
    def test_render_without_title(self, mock_html_response: Mock) -> None:
        """Test render method without title."""
        renderer = HtmlListRenderer()
        item: HtmlListItem = {"name": "Test Item", "url": "https://test.com"}
        renderer.add_item(item)

        mock_response = Mock()
        mock_html_response.return_value = mock_response

        result = renderer.render()

        # Verify HTMLResponse was called with correct content
        mock_html_response.assert_called_once()
        call_args = mock_html_response.call_args
        assert call_args[1]["content"] == (
            "<!DOCTYPE html><html lang='en'><head></head><body><a href='https://test.com'>Test Item</a></body></html>"
        )
        assert result == mock_response

    @patch("pep503_simple_repo_broker.html_renderer.HTMLResponse")
    def test_render_empty_items(self, mock_html_response: Mock) -> None:
        """Test render method with empty items."""
        renderer = HtmlListRenderer(title="Test Title")

        mock_response = Mock()
        mock_html_response.return_value = mock_response

        result = renderer.render()

        # Verify HTMLResponse was called with correct content
        mock_html_response.assert_called_once()
        call_args = mock_html_response.call_args
        assert call_args[1]["content"] == (
            "<!DOCTYPE html><html lang='en'><head><title>Test Title</title></head><body></body></html>"
        )
        assert result == mock_response

    def test_method_chaining(self) -> None:
        """Test method chaining for add_item and add_items."""
        renderer = HtmlListRenderer(title="Test")

        # Test chaining add_item
        result1 = renderer.add_item({"name": "Item 1", "url": "https://item1.com"})
        assert result1 is renderer

        # Test chaining add_items
        result2 = renderer.add_items(
            [
                {"name": "Item 2", "url": "https://item2.com"},
                {"name": "Item 3", "url": "https://item3.com"},
            ]
        )
        assert result2 is renderer

        # Verify all items were added
        assert len(renderer.items) == 3
        assert renderer.items[0]["name"] == "Item 1"
        assert renderer.items[1]["name"] == "Item 2"
        assert renderer.items[2]["name"] == "Item 3"
