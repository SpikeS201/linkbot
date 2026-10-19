import unittest
from crawl import (normalize_url, get_heading_from_html, get_first_paragraph_from_html, 
get_urls_from_html, get_images_from_html, extract_page_data)


class TestCrawl(unittest.TestCase):
        def test_normalize_url_https_slash(self):
                input_url = "https://www.boot.dev/blog/path/"
                actual = normalize_url(input_url)
                expected = "www.boot.dev/blog/path"
                self.assertEqual(actual, expected)
        
        def test_normalize_url_https_noslash(self):
                input_url = "https://www.boot.dev/blog/path"
                actual = normalize_url(input_url)
                expected = "www.boot.dev/blog/path"
                self.assertEqual(actual, expected)
            
        def test_normalize_url_http_slash(self):
                input_url = "http://www.boot.dev/blog/path/"
                actual = normalize_url(input_url)
                expected = "www.boot.dev/blog/path"
                self.assertEqual(actual, expected) 
    
        def test_normalize_url_http_noslash(self):
                input_url = "http://www.boot.dev/blog/path"
                actual = normalize_url(input_url)
                expected = "www.boot.dev/blog/path"
                self.assertEqual(actual, expected)
    
        def test_normalize_url_https_upper(self):
                input_url = "https://www.BOOT.DEV/blog/path/"
                actual = normalize_url(input_url)
                expected = "www.boot.dev/blog/path"
                self.assertEqual(actual, expected)
    
        def test_get_heading_from_html_first_head(self):
                input_body = """<html><body>
                <h1>Test Title 1</h1>
                </body></html>"""
                actual = get_heading_from_html(input_body)
                expected = "Test Title 1"
                self.assertEqual(actual, expected)
        
        def test_get_heading_from_html_second_head(self):
                input_body = """<html><body>
                <h2>Test Title 2</h2>
                </body></html>"""
                actual = get_heading_from_html(input_body)
                expected = "Test Title 2"
                self.assertEqual(actual, expected)
        
        def test_get_heading_from_html_two_heads(self):
                input_body = """<html><body>
                <h1>Test Title 1</h1>
                <h2>Test Title 2</h2>
                </body></html>"""
                actual = get_heading_from_html(input_body)
                expected = "Test Title 1"
                self.assertEqual(actual, expected)
    
        def test_get_heading_from_html_empty_head(self):
                input_body = "<html><body><h1></h1></body></html>"
                actual = get_heading_from_html(input_body)
                expected = ""
                self.assertEqual(actual, expected)
        
        def test_get_heading_from_html_notag(self):
                input_body = "<html><body></body></html>"
                actual = get_heading_from_html(input_body)
                expected = ""
                self.assertEqual(actual, expected)
        
        def test_get_heading_from_html_nested(self):
                input_body = """<html><body>
                <article><header>
                <h1>Test Title 1</h1>
                </body></html>"""
                actual = get_heading_from_html(input_body)
                expected = "Test Title 1"""
                self.assertEqual(actual, expected)
        
        def test_get_first_paragraph_from_html_main_priority(self):
                input_body = """<html><body>
                <p>Outside paragraph.</p>
                <main>
                <p>Main paragraph.</p>
                </main>
                </body></html>"""
                actual = get_first_paragraph_from_html(input_body)
                expected = "Main paragraph."
                self.assertEqual(actual, expected)
        
        def test_get_first_paragraph_from_html_empty(self):
                input_body = """<html><body>
                <main>
                <p></p>
                </main>
                </body></html>"""
                actual = get_first_paragraph_from_html(input_body)
                expected = ""
                self.assertEqual(actual, expected)
        
        def test_get_first_paragraph_from_html_no_tag(self):
                input_body = """<html><body>
                <main>
                </main>
                </body></html>"""
                actual = get_first_paragraph_from_html(input_body)
                expected = ""
                self.assertEqual(actual, expected)
        
        def test_get_urls_from_html_absolute(self):
                input_body = """<html><body>
                <a href="https://crawler-test.com">
                <span>Boot.dev</span></a>
                </body></html>"""
                input_url = "https://crawler-test.com"
                actual = get_urls_from_html(input_body, input_url)
                expected = ["https://crawler-test.com"]
                self.assertEqual(actual, expected)
                
        def test_get_urls_from_html_relative(self):
                input_body = """<html><body>
                <a href="/xyz.html">
                <span>Boot.dev</span></a>
                </body></html>"""
                input_url = "https://crawler-test.com"
                actual = get_urls_from_html(input_body, input_url)
                expected = ["https://crawler-test.com/xyz.html"]
                self.assertEqual(actual, expected)

        def test_get_urls_from_html_none(self):
                input_body = """<html><body>
                <span>Boot.dev</span>
                </body></html>"""
                input_url = "https://crawler-test.com"
                actual = get_urls_from_html(input_body, input_url)
                expected = []
                self.assertEqual(actual, expected)
                
        def test_get_urls_from_html_difplace(self):
                input_body = """<html><body>
                <a href="https://www.boot.dev">Learn Backend Development</a>
                <main>
                <a href="https://crawler-test.com">
                <span>Boot.dev</span></a>
                </main></body></html>"""
                input_url = "https://crawler-test.com"
                actual = get_urls_from_html(input_body, input_url)
                expected = [
                        "https://www.boot.dev",
                        "https://crawler-test.com"
                        ]
                self.assertEqual(actual, expected)
        
        def test_get_images_from_html_absolute(self):
                input_body = """<html><body>
                <img src="https://crawler-test.com/logo.png" alt="Logo">
                </body></html>"""
                input_url = "https://crawler-test.com/gallery.html"
                actual = get_images_from_html(input_body, input_url)
                expected = ["https://crawler-test.com/logo.png"]
                self.assertEqual(actual, expected)
        
        def test_get_images_from_html_relative(self):
                input_body = """<html><body>
                <img src="/logo.png" alt="Logo">
                </body></html>"""
                input_url = "https://crawler-test.com/gallery.html"
                actual = get_images_from_html(input_body, input_url)
                expected = ["https://crawler-test.com/logo.png"]
                self.assertEqual(actual, expected)
        def test_get_images_from_html_relative2(self):
                input_body = """<html><body>
                <img src="logo.png" alt="Logo">
                </body></html>"""
                input_url = "https://crawler-test.com/gallery.html"
                actual = get_images_from_html(input_body, input_url)
                expected = ["https://crawler-test.com/logo.png"]
                self.assertEqual(actual, expected)
        
        def test_get_images_from_html_none(self):
                input_body = """<html><body></body></html>"""
                input_url = "https://crawler-test.com/gallery.html"
                actual = get_images_from_html(input_body, input_url)
                expected = []
                self.assertEqual(actual, expected)

        def test_get_images_from_html_difplace(self):
                input_body = """<html><body>
                <img src="https://crawler2-test.com/logo.png" alt="Logo">
                <main>
                <img src="https://crawler-test.com/logo.png" alt="Logo">
                </main></body></html>"""
                input_url = "https://crawler-test.com/gallery.html"
                actual = get_images_from_html(input_body, input_url)
                expected = [
                        "https://crawler2-test.com/logo.png", 
                        "https://crawler-test.com/logo.png"
                        ]
                self.assertEqual(actual, expected)   

        def test_extract_page_data_basic(self):
                input_url = "https://crawler-test.com"
                input_body = """<html><body>
                <h1>Test Title</h1>
                <p>This is the first paragraph.</p>
                <a href="/link1">Link 1</a>
                <img src="/image1.jpg" alt="Image 1">
                </body></html>"""
                actual = extract_page_data(input_body, input_url)
                expected = {
                "url": "https://crawler-test.com",
                "heading": "Test Title",
                "first_paragraph": "This is the first paragraph.",
                "outgoing_links": ["https://crawler-test.com/link1"],
                "image_urls": ["https://crawler-test.com/image1.jpg"],
                }
                self.assertEqual(actual, expected)
        def test_extract_page_data_main_section(self) -> None:
                input_url = "https://crawler-test.com"
                input_body = """<html><body>
                <nav><p>Navigation paragraph</p></nav>
                 <main>
                <h1>Main Title</h1>
                <p>Main paragraph content.</p>
                </main>
                </body></html>"""
                actual = extract_page_data(input_body, input_url)
                self.assertEqual(actual["heading"], "Main Title")
                self.assertEqual(actual["first_paragraph"], "Main paragraph content.")

        def test_extract_page_data_missing_elements(self) -> None:
                input_url = "https://crawler-test.com"
                input_body = "<html><body><div>No h1, p, links, or images</div></body></html>"
                actual = extract_page_data(input_body, input_url)
                expected = {
                "url": "https://crawler-test.com",
                "heading": "",
                "first_paragraph": "",
                "outgoing_links": [],
                "image_urls": [],
                }
                self.assertEqual(actual, expected)

if __name__ == "__main__":
    unittest.main()