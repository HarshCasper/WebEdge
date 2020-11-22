from webedge import webpage_analysis
from bs4 import BeautifulSoup as Soup
import json
import requests


class Spider(object):
    pages_to_crawl = []
    pages_crawled = []

    titles = {}
    descriptions = {}

    report = {
        "pages": []
    }

    def __init__(self, site, sitemap=None):
        if sitemap is not None:
            locations = self._parse_sitemap(sitemap)
            self.pages_to_crawl.extend(locations)
        else:
            self.pages_to_crawl.append(site)

    def _parse_sitemap(self, url):
        '''
        Parse the Sitemap for Locations
        '''
        output = []

        resp = requests.get(url)
        if not resp.ok:
            return []

        soup = Soup(resp.content, "html.parser")
        urls = soup.findAll('url')

        if len(url) > 0:
            for u in urls:
                loc = u.find('loc').string
                output.append(loc)

        return output

    def crawl(self):
        for page in self.pages_to_crawl:
            html = webpage_analysis.Webpage(page, self.titles, self.descriptions)

            page_report = html.report()
            self.report['pages'].append(page_report)
            self.pages_crawled.append(page.strip().lower())

        print(json.dumps(self.report, indent=4, separators=(',', ': ')))
