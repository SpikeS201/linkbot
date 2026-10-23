from urllib.parse import urlsplit, urljoin
from bs4 import BeautifulSoup, Tag
from typing import TypedDict
import aiohttp
import asyncio
import sys

class PageData(TypedDict):
    url: str
    heading: str
    first_paragraph: str
    outgoing_links: list[str]
    image_urls: list[str]

class AsyncCrawler:
    def __init__(self, base_url: str):
        self.base_url: str = base_url
        self.base_domain: str = urlsplit(base_url).netloc
        self.page_data: dict = {}
        self.visited = set()
        self.lock =  asyncio.Lock()
        self.max_concurrency: int = int(sys.argv[2])
        self.semaphore = asyncio.Semaphore(self.max_concurrency)
        self.session = None
        self.max_pages: int = int(sys.argv[3])
        self.should_stop: bool = False
        self.all_tasks = set()
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()
    
    async def add_page_visit(self, normalized_url):
        async with self.lock:
            if self.should_stop is True or normalized_url in self.visited:
                return False
            elif len(self.visited) >= self.max_pages:
                self.should_stop = True
                print("Reached maximum number of pages to crawl.")
                return False
            else:
                self.visited.add(normalized_url)
                return True
    
    async def get_html(self, url):
        try:
            async with self.session.get(url, headers={"User-Agent": "BootCrawler/1.0"}) as resp:
                resp.raise_for_status()
                if not resp.headers['Content-Type'].startswith('text/html'):
                    raise Exception(f"got non-HTML response: {resp.headers['Content-Type']}")
                return await resp.text()
        except Exception as e:
            raise Exception(f"network error while fetching {url}: {e}")
    
        
    async def crawl_page(self,
        current_url: str | None = None,
        )-> dict[str, PageData]:
        
        if self.should_stop is True:
            return self.page_data
        if current_url is None:
            current_url = self.base_url
        if self.page_data is None:
            self.page_data = {}
            
        if self.base_domain != urlsplit(current_url).netloc:
            return self.page_data
        
        url = normalize_url(current_url)
        
        if not await self.add_page_visit(url):
            return self.page_data
        
        print(f"crawling {url}")
        async with self.semaphore:
            
            html = await self.get_html(current_url)
        
            async with self.lock:
                data = extract_page_data(html, current_url)
                self.page_data[url] = data
                
                tasks = set()
                for link in data["outgoing_links"]:
                    task = asyncio.create_task(self.crawl_page(link))
                    tasks.add(task)
                    self.all_tasks.add(task)
                    print(f"crawling {link}")
                    task.add_done_callback(self.all_tasks.discard)
        
        await asyncio.gather(*tasks)
        
        return self.page_data

    async def crawl(self):
        await self.crawl_page(self.base_url)
        return self.page_data
    
async def crawl_site_async(base_url):
    async with AsyncCrawler(base_url) as crawler:
        return await crawler.crawl()
            

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




    