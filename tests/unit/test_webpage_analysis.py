import bs4
import ddt
import testtools
from webedge import webpage_analysis
from webedge.warnings import BADGES
from webedge.warnings import WARNINGS


@ddt.ddt
class WebpageTests(testtools.TestCase):

    def setUp(self):
        super(WebpageTests, self).setUp()
        self.titles = {}
        self.descriptions = {}

    def soup_file(self, html):
        soup = bs4.BeautifulSoup(html, "html.parser")
        return soup

    @ddt.file_data('data_html_positive.json')
    def test_analyze_positive(self, data):
        html = data[0]
        badge = data[1]
        self.wp = webpage_analysis.Webpage(
            "https://harshcasper.github.io",
            html,
            self.titles,
            self.descriptions)
        self.wp.report()

    @ddt.file_data('data_html_negative.json')
    def test_analyze_negative(self, data):
        html = data[0]
        expected_error = data[1]
        self.wp = webpage_analysis.Webpage(
            "https://harshcasper.github.io",
            html,
            self.titles,
            self.descriptions)
        self.wp.report()
        self.assertTrue(any(issue["warning"] == WARNINGS[expected_error]
                            for issue in self.wp.issues),
                        "{0} not raised.".format(WARNINGS[expected_error]))

    @ddt.file_data('data_url_negative.json')
    def test_analyze_negative_url(self, data):
        url = data[0]
        expected_error = data[1]
        html = ""
        self.wp = webpage_analysis.Webpage(
            url, html, self.titles, self.descriptions)
        self.wp.report()
        self.assertTrue(any(issue["warning"] == WARNINGS[expected_error]
                            for issue in self.wp.issues),
                        "{0} not raised.".format(WARNINGS[expected_error]))

    @ddt.file_data('data_url_positive.json')
    def test_analyze_positive_url(self, data):
        url = data[0]
        badge = data[1]
        html = ""
        self.wp = webpage_analysis.Webpage(
            url, html, self.titles, self.descriptions)
        self.wp.report()
        if badge != "":
            self.assertTrue(any(earned["achievement"] == BADGES[badge]
                                for earned in self.wp.achieved),
                            "{0} not earned".format(BADGES[badge]))

    @ddt.file_data('data_visible_tags.json')
    def test_visible_tags(self, data):
        html = ""
        self.wp = webpage_analysis.Webpage(
            "https://harshcasper.github.io",
            html,
            self.titles,
            self.descriptions)
        soup = self.soup_file(data[0])
        elements = soup.findAll(text=True)
        for tag in elements:
            result = self.wp.visible_tags(tag)
            self.assertEqual(result, data[1])

    @ddt.file_data('data_duplicates_negative.json')
    def test_analyze_duplicates_negative(self, page):
        html = page[0]
        expected_error = page[1]
        report = {"pages": []}
        for i in range(0, 2):
            self.wp = webpage_analysis.Webpage(
                "https://harshcasper.github.io/page{0}.html".format(i),
                html,
                self.titles,
                self.descriptions)

            page_report = self.wp.report()
            report['pages'].append(page_report)
        self.assertTrue(any(issue["warning"] == WARNINGS[expected_error]
                            for p in report['pages'] for issue in p['issues']),
                        "{0} not raised. {1} {2}".format(
                            WARNINGS[expected_error],
                            self.titles,
                            self.descriptions))
