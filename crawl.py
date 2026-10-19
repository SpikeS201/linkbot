from urllib.parse import urlsplit, urljoin
from bs4 import BeautifulSoup, Tag
from typing import TypedDict
import requests


class PageData(TypedDict):
    url: str
    heading: str
    first_paragraph: str
    outgoing_links: list[str]
    image_urls: list[str]

def normalize_url(input_url: str) -> str:
    split = urlsplit(input_url)
    netloc = split.netloc
    path = split.path.rstrip("/")
    return (netloc + path).lower()

def get_heading_from_html(html: str) -> str:
    soup = BeautifulSoup(html, features="html.parser")
    h_tag = soup.find("h1") or soup.find("h2")
    return h_tag.get_text(strip=True) if isinstance(h_tag, Tag) else ""

def get_first_paragraph_from_html(html: str) -> str:
    soup = BeautifulSoup(html, features="html.parser")
    main_tag = soup.find("main")
    if main_tag:
        p_tag = main_tag.find("p")
    else:
        p_tag = soup.find("p")
    return p_tag.get_text(strip=True) if isinstance(p_tag, Tag) else ""

def get_urls_from_html(html: str, base_url: str)-> list:
    soup = BeautifulSoup(html, features="html.parser")
    href_list = []
    for a in soup.find_all("a"):
        link = a.get("href")
        if not isinstance(link, str) or link == "":
            continue
        elif urlsplit(link).netloc == '':
            href_list.append(urljoin(base_url, link))
        else:
            href_list.append(link)
    return href_list

def get_images_from_html(html: str, base_url: str)-> list:
    soup = BeautifulSoup(html, features="html.parser")
    src_list: list = []
    for img in soup.find_all("img"):
        link = img.get("src")
        if not isinstance(link, str) or link == "":
            continue
        elif urlsplit(link).netloc == '':
            src_list.append(urljoin(base_url, link))
        else:
            src_list.append(link)
    return src_list

def extract_page_data(html: str, page_url: str)-> PageData:
    page_data: PageData = {
                    "url": page_url,
                    "heading": get_heading_from_html(html),
                    "first_paragraph": get_first_paragraph_from_html(html),
                    "outgoing_links": get_urls_from_html(html, page_url),
                    "image_urls": get_images_from_html(html, page_url), 
                    }
    return page_data

def get_html(url):
    try:
        r = requests.get(url, headers={"User-Agent": "BootCrawler/1.0"})
    except Exception as e:
        raise Exception(f"network error while fetching {url}: {e}")
    
    r.raise_for_status()
    
    if not r.headers['Content-Type'].startswith('text/html'):
        raise Exception(f"got non-HTML response: {r.headers['Content-Type']}")
    
    return r.text

def crawl_page(
    base_url: str,
    current_url: str | None = None,
    page_data: dict[str, PageData] | None = None
    )-> dict[str, PageData]:
    
    if current_url is None:
        current_url = base_url
    if page_data is None:
        page_data = {}
        
    if urlsplit(base_url).netloc != urlsplit(current_url).netloc:
        return page_data
    
    url = normalize_url(current_url)
    
    if url in page_data:
        return page_data
    
    print(f"crawling {url}")
    html = get_html(current_url)
    
    data = extract_page_data(html, current_url)
    page_data[url] = data
    
    for link in data["outgoing_links"]:
        page_data = crawl_page(base_url, link, page_data)
        print(f"crawling {link}")
    
    return page_data
    
    