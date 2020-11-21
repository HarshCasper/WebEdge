import sys
import website_analysis

if __name__ == '__main__':
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
        print("Run the Command: python3 main.py http://[YOUR_WEBSITE]]")
        exit
