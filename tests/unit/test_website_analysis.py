import uuid
import mock
import requests
from bs4 import BeautifulSoup as Soup
from webedge import website_analysis
from webedge.warnings import BADGES
from webedge.warnings import WARNINGS
import ddt
import testtools


@ddt.ddt
class WebsiteTests(testtools.TestCase):

    def setUp(self):
        super(WebsiteTests, self).setUp()
        self.site_url = "http://www.mock{0}.com".format(uuid.uuid4())

    def test_init_url(self):
        web_page = website_analysis.Spider(self.site_url, None)
        self.assertEqual(len(web_page.pages_to_crawl), 1)
        self.assertEqual(web_page.pages_to_crawl[0], self.site_url)

    @ddt.file_data("data_sitemap_positive.json")
    @mock.patch('webedge.website_analysis.requests.get')
    def test_init_sitemap_positive(self, sitemap_content, mock_requests):
        sitemap_url = "/sitemap.xml"
        mock_requests.return_value.status_code = requests.codes.ok
        mock_requests.return_value.content = sitemap_content
        web_page = website_analysis.Spider(self.site_url, self.site_url + sitemap_url)
        self.assertTrue(self.site_url in web_page.pages_to_crawl)

    @ddt.file_data("data_sitemap_negative.json")
    @mock.patch('webedge.website_analysis.requests.get')
    def test_init_sitemap_negative(self, sitemap_content, mock_requests):
        sitemap_url = "/sitemap.xml"
        mock_requests.return_value.status_code = requests.codes.not_found
        mock_requests.return_value.content = sitemap_content
        web_page = website_analysis.Spider(self.site_url, self.site_url + sitemap_url)
        self.assertTrue(self.site_url in web_page.pages_to_crawl)

    @ddt.file_data("data_sitemap_positive.json")
    def test_parse_sitemap(self, sitemap_content):
        web_page = website_analysis.Spider(self.site_url, None)
        locations = web_page._parse_sitemap(sitemap_content)
        soup = Soup(sitemap_content, "html.parser")
        urls = soup.findAll('url')
        self.assertEqual(len(locations), len(urls))

    @ddt.file_data("data_webpage.json")
    @mock.patch('webedge.website_analysis.requests.get')
    def test_crawl(self, data, mock_requests):
        web_page = website_analysis.Spider(self.site_url, None)
        web_page._analyze_crawlers = mock.MagicMock(name="_analyze_crawlers")
        resp_code, content = data.split("|")
        mock_requests.return_value.status_code = int(resp_code)
        mock_requests.return_value.content = content
        web_page.crawl()
        if int(resp_code) == requests.codes.ok:
            self.assertEqual(len(web_page.issues), 0)
        elif int(resp_code) == requests.codes.not_found:
            self.assertTrue(any(issue["warning"] == WARNINGS["BROKEN_LINK"]
                                for issue in web_page.issues),
                            "{0} not raised.".format(WARNINGS["BROKEN_LINK"]))
        else:
            self.assertTrue(any(issue["warning"] == WARNINGS["SERVER_ERROR"]
                                for issue in web_page.issues),
                            "{0} not raised.".format(WARNINGS["SERVER_ERROR"]))

    @ddt.data("200", "404", "500")
    @mock.patch('webedge.website_analysis.requests.get')
    def test_analyze_crawlers(self, resp_code, mock_requests):
        mock_requests.return_value.status_code = int(resp_code)
        web_page = website_analysis.Spider(self.site_url, None)
        web_page._analyze_crawlers()
        if int(resp_code) == requests.codes.ok:
            self.assertTrue(any(earned["achievement"] == BADGES["ROBOTS.TXT"]
                                for earned in web_page.achieved),
                            "{0} not earned".format(BADGES["ROBOTS.TXT"]))
        else:
            self.assertTrue(any(issue["warning"] == WARNINGS["ROBOTS.TXT"]
                                for issue in web_page.issues),
                            "{0} not raised.".format(WARNINGS["ROBOTS.TXT"]))

    @ddt.data("200", "404", "500")
    @mock.patch('webedge.website_analysis.requests.get')
    def test_analyze_blog(self, resp_code, mock_requests):
        mock_requests.return_value.status_code = int(resp_code)
        web_page = website_analysis.Spider(self.site_url, None)
        web_page._analyze_blog()
        if int(resp_code) == requests.codes.ok:
            self.assertTrue(
                any(earned["achievement"] == BADGES["BLOG_DETECTED"]
                    for earned in web_page.achieved),
                "{0} not earned".format(BADGES["BLOG_DETECTED"]))
        else:
            self.assertTrue(
                any(issue["warning"] == WARNINGS["BLOG_MISSING"]
                    for issue in web_page.issues),
                "{0} not raised.".format(WARNINGS["BLOG_MISSING"]))
