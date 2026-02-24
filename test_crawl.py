import unittest
from crawl import (
    normalize_url,
    get_h1_from_html,
    get_first_paragraph_from_html,
    get_urls_from_html,
    get_images_from_html,
    extract_page_data
)


class TestCrawl(unittest.TestCase):

    # ---------- normalize_url ----------

    def test_normalize_url_basic(self):
        self.assertEqual(normalize_url("https://blog.boot.dev/path"), "blog.boot.dev/path")

    def test_normalize_url_trailing_slash(self):
        self.assertEqual(normalize_url("https://blog.boot.dev/path/"), "blog.boot.dev/path")

    def test_normalize_url_no_scheme(self):
        self.assertEqual(normalize_url("blog.boot.dev/path"), "blog.boot.dev/path")

    # ---------- get_h1_from_html ----------

    def test_get_h1_basic(self):
        html = "<html><body><h1>Title</h1></body></html>"
        self.assertEqual(get_h1_from_html(html), "Title")

    def test_get_h1_missing(self):
        html = "<html><body></body></html>"
        self.assertEqual(get_h1_from_html(html), "")

    def test_get_h1_nested(self):
        html = "<html><body><div><h1>Nested</h1></div></body></html>"
        self.assertEqual(get_h1_from_html(html), "Nested")

    # ---------- get_first_paragraph_from_html ----------

    def test_get_first_paragraph_basic(self):
        html = "<html><body><p>First paragraph</p></body></html>"
        self.assertEqual(get_first_paragraph_from_html(html), "First paragraph")

    def test_get_first_paragraph_main_priority(self):
        html = "<html><body><p>Outside</p><main><p>Main</p></main></body></html>"
        self.assertEqual(get_first_paragraph_from_html(html), "Main")

    def test_get_first_paragraph_multiple_p_no_main(self):
        html = "<html><body><p>First</p><p>Second</p></body></html>"
        self.assertEqual(get_first_paragraph_from_html(html), "First")

    # ---------- get_urls_from_html ----------

    def test_get_urls_absolute(self):
        html = '<html><body><a href="https://blog.boot.dev"></a></body></html>'
        result = get_urls_from_html(html, "https://blog.boot.dev")
        self.assertEqual(result, ["https://blog.boot.dev"])

    def test_get_urls_relative(self):
        html = '<html><body><a href="/about"></a></body></html>'
        result = get_urls_from_html(html, "https://blog.boot.dev")
        self.assertEqual(result, ["https://blog.boot.dev/about"])

    def test_get_urls_missing_href(self):
        html = "<html><body><a>Missing href</a></body></html>"
        result = get_urls_from_html(html, "https://blog.boot.dev")
        self.assertEqual(result, [])

    # ---------- get_images_from_html ----------

    def test_get_images_relative(self):
        html = '<html><body><img src="/logo.png"></body></html>'
        result = get_images_from_html(html, "https://blog.boot.dev")
        self.assertEqual(result, ["https://blog.boot.dev/logo.png"])

    def test_get_images_absolute(self):
        html = '<html><body><img src="https://cdn.site/img.png"></body></html>'
        result = get_images_from_html(html, "https://blog.boot.dev")
        self.assertEqual(result, ["https://cdn.site/img.png"])

    def test_get_images_missing_src_alt(self):
        html = "<html><body><img></body></html>"
        result = get_images_from_html(html, "https://blog.boot.dev")
        self.assertEqual(result, [])

    # ---------- extract_page_data ----------

    def test_extract_page_data_basic(self):
        html = """
        <html><body>
            <h1>Test Title</h1>
            <p>This is the first paragraph.</p>
            <a href="/link1">Link 1</a>
            <img src="/image1.jpg" alt="Image 1">
        </body></html>
        """
        url = "https://blog.boot.dev"
        expected = {
            "url": url,
            "h1": "Test Title",
            "first_paragraph": "This is the first paragraph.",
            "outgoing_links": ["https://blog.boot.dev/link1"],
            "image_urls": ["https://blog.boot.dev/image1.jpg"]
        }
        self.assertEqual(extract_page_data(html, url), expected)

    def test_extract_page_data_missing(self):
        html = "<html><body></body></html>"
        url = "https://example.com"
        expected = {
            "url": url,
            "h1": "",
            "first_paragraph": "",
            "outgoing_links": [],
            "image_urls": []
        }
        self.assertEqual(extract_page_data(html, url), expected)

    def test_extract_page_data_relative_links_images(self):
        html = "<html><body><a href='/link2'></a><img src='/img2.png'></body></html>"
        url = "https://example.com"
        expected = {
            "url": url,
            "h1": "",
            "first_paragraph": "",
            "outgoing_links": ["https://example.com/link2"],
            "image_urls": ["https://example.com/img2.png"]
        }
        self.assertEqual(extract_page_data(html, url), expected)


if __name__ == "__main__":
    unittest.main()