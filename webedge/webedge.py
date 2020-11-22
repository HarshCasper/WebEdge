import sys
from webedge import website_analysis

def main():
    if len(sys.argv) == 2:
        site_domain = sys.argv[1]
        spider = website_analysis.Spider(site_domain)
        spider.crawl()
    elif len(sys.argv) == 3:
        site_domain = sys.argv[1]
        site_map = site_domain + sys.argv[2]
        spider = website_analysis.spider(site_domain, site_map)
        spider.crawl()
    else:
        print("Run the Command: webedge http://[YOUR_WEBSITE]]")
        exit

if __name__ == "__main__":
    sys.exit(main())
    