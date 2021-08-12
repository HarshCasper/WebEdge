from bs4 import BeautifulSoup as Soup
import requests
from six.moves.urllib import parse
from webedge.warnings import BADGES
from webedge.warnings import WARNINGS
from webedge import webpage_analysis


class Spider:
    report = {"pages": []}

    def __init__(self, site, sitemap=None, page=None):
        parsed_url = parse.urlparse(site)

        self.domain = "{0}://{1}".format(parsed_url.scheme, parsed_url.netloc)
        self.pages_crawled = []
        self.pages_to_crawl = []
        self.titles = {}
        self.descriptions = {}
        self.issues = []
        self.achieved = []

        if sitemap is not None:
            locations = []
            resp = requests.get(self.domain + sitemap)
            if resp.status_code == requests.codes.ok:
                locations = self._parse_sitemap(resp.content)

            self.pages_to_crawl.append(site)
            self.pages_to_crawl.extend(locations)
        elif page is not None:
            self.pages_to_crawl.append(site + page)
        else:
            self.pages_to_crawl.append(site)

    def _parse_sitemap(self, sitemap):
        """
        Parse the Sitemap for Locations.
        Args:
            sitemap: XML Sitempa
        Returns:
            locations
        """
        locations = []

        soup = Soup(sitemap, "html.parser")
        urls = soup.findAll("url")

        if len(urls) > 0:
            for u in urls:
                loc = u.find("loc").string
                locations.append(loc)

        return locations

    def _analyze_crawlers(self):
        """
        Analyzes Crawlers in form of robots.txt file.
        Returns:
            Badges/Warnings: Depending on whether a Robots.txt exists.
        """
        resp = requests.get(self.domain + "/robots.txt")
        if resp.status_code == requests.codes.ok:
            self.earned(BADGES["ROBOTS.TXT"])
        else:
            self.warn(WARNINGS["ROBOTS.TXT"])

    def _analyze_blog(self):
        """
        Analyzes Blogs in form of a Blogging Subdomain
        Returns:
            Badges/Warnings: Depending on whether a Blog exists or not.
        """
        resp = requests.get(self.domain + "/blog")
        if resp.status_code == requests.codes.ok:
            self.earned(BADGES["BLOG_DETECTED"], self.domain + u"/blog")
        else:
            self.warn(WARNINGS["BLOG_MISSING"])

    def warn(self, message, value=None):
        """
        Value lost through improper SEO Optimization on the Website.
        """
        self.issues.append({"warning": message, "value": value})

    def earned(self, message, value=None):
        """
        Value earned through proper SEO Optimization on the Website.
        """
        self.achieved.append({"achievement": message, "value": value})

    def crawl(self):
        """
        Crawl the Website and analyze different things.
        """
        self._analyze_crawlers()
        self._analyze_blog()
        for page_url in self.pages_to_crawl:
            resp = requests.get(page_url)
            if resp.status_code == requests.codes.ok:
                html = webpage_analysis.Webpage(
                    page_url, resp.content, self.titles, self.descriptions
                )
                page_report = html.report()
                self.report["pages"].append(page_report)
                self.pages_crawled.append(page_url.strip().lower())
                # print("Crawled {0} Pages of {1}: {2}".format(
                #     len(self.pages_crawled), len(self.pages_to_crawl), page_url))
            elif resp.status_code == requests.codes.not_found:
                self.warn(WARNINGS["BROKEN_LINK"], page_url)
            else:
                self.warn(
                    WARNINGS["SERVER_ERROR"],
                    "HTTP{0} received for {1}".format(resp.status_code, page_url),
                )
        self.report["site"] = {}
        self.report["site"]["issues"] = self.issues
        self.report["site"]["achieved"] = self.achieved
        return self.report
