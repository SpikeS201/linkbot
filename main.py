import sys
from crawl import *

def main():
    print("Hello from linkbot!")
    if len(sys.argv) < 2:
        print("no website provided")
        sys.exit(1)
    if len(sys.argv) > 2:
        print("too many arguments provided")
        sys.exit(1)
    
    print(f"starting crawl of: {sys.argv[1]}...")
    
    page_data = crawl_page(sys.argv[1])
    
    print(f"crawling finished, crawled pages{len(page_data)}")
    for page in page_data.values():
        print(f"- {page['url']}: {len(page['outgoing_links'])} outgoing links")
    
    
    sys.exit(0)


if __name__ == "__main__":
    main()
