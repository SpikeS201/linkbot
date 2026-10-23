import sys
from crawl import *
from json_report import write_json_report

async def main():
    print("Hello from linkbot!")
    if len(sys.argv) < 4:
        print("no website provided")
        sys.exit(1)
    if len(sys.argv) > 4:
        print("too many arguments provided")
        sys.exit(1)
    
    print(f"starting crawl of: {sys.argv[1]}...")
    
    page_data = await crawl_site_async(sys.argv[1])
    
    print(f"crawling finished, crawled pages{len(page_data)}")
    
    write_json_report(page_data)
    
    sys.exit(0)


if __name__ == "__main__":
    asyncio.run(main())
