import re
import bs4
import requests
from six.moves.urllib import parse
from webedge.stop_words import ENGLISH_STOP_WORDS
from webedge.warnings import BADGES
from webedge.warnings import WARNINGS
from webedge.social_websites import SOCIAL_WEBSITES
from AnalyseSentiment.AnalyseSentiment import AnalyseSentiment

# REGEX to match the Words on the Markup Document
TOKEN_REGEX = re.compile(r"(?u)\b\w\w+\b")


class Webpage:
    url = None
    title = None
    description = None

    website_titles = {}
    website_descriptions = {}

    def __init__(self, page_url, html, website_titles, website_descriptions):
        self.url = page_url
        self.netloc = parse.urlparse(page_url).netloc
        self.html = html
        self.title = None
        self.description = None
        self.keywords = {}
        self.issues = []
        self.achieved = []

        self.website_titles = website_titles
        self.website_descriptions = website_descriptions

    def report(self):
        """
        Analyzes and verified the Optimizations on the Page.
        """
        soup = bs4.BeautifulSoup(self.html, "html.parser")

        # per page analysis
        self._analyze_title(soup)
        self._analyze_description(soup)
        self._analyze_url_structure(soup)
        self._analyze_anchors(soup)
        self._analyze_images(soup)
        self._analyze_headings(soup)
        self._analyze_keywords(soup)
        self._analyze_wordcount(soup)

        return self._render()

    def _analyze_title(self, doc):
        """
        Validate the title
        Args:
            doc: Beautful Soup Object
        Returns:
            earned/warn: Returns if the Document Title fall among the prerequisties set
        """
        self.title = t = u""
        if doc.title:
            self.title = t = doc.title.text

        length = len(t)
        if length == 0:
            self.warn(WARNINGS["TITLE_MISSING"], self.title)
            return
        if length < 10:
            self.warn(WARNINGS["TITLE_TOO_SHORT"], self.title)
        elif length > 70:
            self.warn(WARNINGS["TITLE_TOO_LONG"], self.title)
        else:
            self.earned(BADGES["TITLE_LENGTH"], self.title)

        if any(vague_words in t.lower() for vague_words in ["untitled", "page"]):
            self.warn(WARNINGS["TITLE_TOO_GENERIC"], self.title)
        else:
            self.earned(BADGES["TITLE_INFORMATIVE"], self.title)

        sentimentobj = AnalyseSentiment()
        sentimentdata = sentimentobj.Analyse(self.title)
        if sentimentdata.get("overall_sentiment") == "Negative":
            self.warn(WARNINGS["NEGATIVE_TITLE"], self.title)
        elif sentimentdata.get("overall_sentiment") == "Neutral":
            self.earned(BADGES["NEUTRAL_TITLE"], self.title)
        else:
            self.earned(BADGES["POSITIVE_TITLE"], self.title)

        title_words = self.grouped(self.tokenize(t))
        for word, count in title_words:
            if count > 3:
                self.warn(WARNINGS["TITLE_KEYWORD_STUFFED"], self.title)

        if t in self.website_titles:
            self.warn(
                WARNINGS["TITLE_DUPLICATED"],
                u'"{0}" previously used on pages: {1}'.format(
                    t, self.website_titles[t]
                ),
            )
        else:
            self.earned(BADGES["TITLE_UNIQUE"], self.title)
            self.website_titles[t] = self.url

    def _analyze_description(self, doc):
        """
        Analyzes and Validates the description present in the Markup Document.
        Args:
            doc: Beautful Soup Object
        Returns:
            earned/warn: Returns if Description fall among the prerequisties set
        """
        desc = doc.findAll("meta", attrs={"name": "description"})

        self.description = d = u""
        if len(desc) > 0:
            self.description = d = desc[0].get("content", "")

        length = len(d)
        if length == 0:
            self.warn(WARNINGS["DESCRIPTION_MISSING"])
            return
        if length < 140:
            self.warn(WARNINGS["DESCRIPTION_TOO_SHORT"], self.description)
        elif length > 255:
            self.warn(WARNINGS["DESCRIPTION_TOO_LONG"], self.description)
        else:
            self.earned(BADGES["DESCRIPTION_LENGTH"], self.description)

        if any(vague_words in d.lower() for vague_words in ["web page", "page about"]):
            self.warn(WARNINGS["DESCRIPTION_TOO_GENERIC"], self.description)
        else:
            self.earned(BADGES["DESCRIPTION_INFORMATIVE"], self.description)

        sentimentobj = AnalyseSentiment()
        sentimentdata = sentimentobj.Analyse(self.title)
        if sentimentdata.get("overall_sentiment") == "Negative":
            self.warn(WARNINGS["NEGATIVE_DESCRIPTION"], self.description)
        elif sentimentdata.get("overall_sentiment") == "Neutral":
            self.earned(BADGES["NEUTRAL_DESCRIPTION"], self.description)
        else:
            self.earned(BADGES["POSITIVE_DESCRIPTION"], self.description)

        desc_words = self.grouped(self.tokenize(d))
        for word, count in desc_words:
            if count > 3:
                self.warn(WARNINGS["DESCRIPTION_KEYWORD_STUFFED"], self.description)

        if d in self.website_descriptions:
            self.warn(
                WARNINGS["DESCRIPTION_DUPLICATED"],
                u'"{0}" previously used on pages: {1}'.format(
                    d, self.website_descriptions[d]
                ),
            )
        else:
            self.website_descriptions[d] = self.url

    def _analyze_url_structure(self, doc):
        """
        Analyze and verified the URL Structure of the Website.
        Args:
            doc: Beautful Soup Object
        Returns:
            earned/warn: Returns if URL Structure falls in the prerequisties set
        """

        parsed_url = parse.urlparse(self.url)
        path = parsed_url.path.split("/")

        if len(self.url) > 100:
            self.warn(WARNINGS["URL_TOO_LONG"], self.url)

        if any(vague_words in self.url.lower() for vague_words in ["page"]):
            self.warn(WARNINGS["URL_TOO_GENERIC"], self.url)

        url_words = self.grouped(self.tokenize(path[-1]))
        for word, count in url_words:
            if count >= 2:
                self.warn(WARNINGS["URL_KEYWORD_STUFFED"], self.url)

        if len(path) > 3:
            self.warn(WARNINGS["URL_TOO_DEEP"], self.url)

        canonical = doc.find("link", rel="canonical")
        if canonical:
            canonical_url = canonical["href"]

            if canonical_url != self.url:
                self.warn(WARNINGS["URL_NOT_CANONICAL"], canonical_url)
            else:
                self.earned(BADGES["URL_CANONICAL"], self.url)

        if any(x.isupper() for x in self.url):
            self.warn(WARNINGS["URL_CAPITALIZED"], self.url)
        else:
            self.earned(BADGES["URL_CORRECTLY_CASED"], self.url)

    def _analyze_anchors(self, doc):
        """
        Analyzes and verified the Anchor Tags on the Markup.
        Args:
            doc: Beautful Soup Object
        Returns:
            earned/warn: Returns if Anchors are defined and the prerequisties are set.
        """
        anchors = doc.find_all("a", href=True)
        verified_pages = []

        for tag in anchors:
            tag_href = tag["href"]
            tag_text = tag.text.lower().strip()

            image_link = tag.find("img")

            if image_link is None:
                if len(tag.get("title", "")) == 0 and len(tag_text) == 0:
                    self.warn(WARNINGS["ANCHOR_TEXT_MISSING"], tag_href)
                elif len(tag_text) < 3:
                    self.warn(WARNINGS["ANCHOR_TEXT_TOO_SHORT"], tag_text)
                elif len(tag_text) > 100:
                    self.warn(WARNINGS["ANCHOR_TEXT_TOO_LONG"], tag_text)

                if any(
                    vague_words in tag_text.lower()
                    for vague_words in ["click here", "page", "article"]
                ):
                    self.warn(WARNINGS["ANCHOR_TEXT_TOO_GENERIC"], tag_text)

            elif len(image_link.get("alt", "")) == 0:
                self.warn(WARNINGS["IMAGE_LINK_ALT_MISSING"], tag_href)
            else:
                self.earned(BADGES["IMAGE_LINK_ALT"], image_link.get("alt", ""))

            if len(tag_href) > 100:
                self.warn(WARNINGS["ANCHOR_HREF_TOO_LONG"], tag_href)

            if tag_text == tag_href:
                self.warn(WARNINGS["ANCHOR_HREF_EQUALS_TEXT"], tag_text)

            if (
                len(parse.urlparse(tag_href).netloc) > 0
                and self.netloc not in tag_href
                and all(
                    social_site not in tag_href for social_site in SOCIAL_WEBSITES
                )
            ):
                if tag.get("rel") is None or "nofollow" not in tag.get("rel"):
                    self.warn(WARNINGS["ANCHOR_NO_FOLLOW"], tag_href)
                else:
                    self.earned(BADGES["ANCHOR_NO_FOLLOW"], tag_href)

            if not tag_href.startswith("mailto:"):
                referenced_href = tag_href
                if len(parse.urlparse(tag_href).netloc) == 0:
                    referenced_href = parse.urljoin(self.url, tag_href)

                if referenced_href not in verified_pages:
                    resp = requests.head(referenced_href)
                    if resp.status_code == requests.codes.not_found:
                        self.warn(WARNINGS["BROKEN_LINK"], referenced_href)

                verified_pages.append(referenced_href)

    def _analyze_images(self, doc):
        """
        Analyzes and verifies that each image has an alt and title.
        Args:
            doc: Beautful Soup Object
        Returns:
            earned/warn: Returns if Images Alt and Title tag fall in the prerequisties set
        """
        images = doc.find_all("img")

        for image in images:
            src = image.get("src", image.get("data-src", ""))

            if len(src) == 0:
                self.warn(WARNINGS["IMAGE_SRC_MISSING"], str(image))
            else:
                if len(image.get("alt", "")) == 0:
                    self.warn(WARNINGS["IMAGE_ALT_MISSING"], str(image))

                if (
                    len(parse.urlparse(src).netloc) == 0 or self.netloc in src
                ) and len(src) > 15:
                    self.warn(WARNINGS["IMAGE_SRC_TOO_LONG"], src)
                if len(image.get("alt", "")) > 40:
                    self.warn(WARNINGS["IMAGE_ALT_TOO_LONG"], image.get("alt", ""))

    def _analyze_headings(self, doc):
        """
        Analyzes Headings on the Website and makes sure of atleast one heading tag.
        Args:
            doc: Beautful Soup Object
        Returns:
            earned/warn: Returns if Headings fall in the prerequisties set
        """
        h1tags = doc.find_all("h1")

        self.headers = []
        for h in h1tags:
            self.headers.append(h.text)

            if len(h.text) < 3:
                self.warn(WARNINGS["H1_TOO_SHORT"], h.text)
            else:
                self.earned(BADGES["H1_LENGTH"], h.text)

        if len(h1tags) != 1:
            self.warn(WARNINGS["H1_ONE_PER_PAGE"], self.headers)
        else:
            self.earned(BADGES["H1_ONE_PER_PAGE"], self.headers)

    def _analyze_keywords(self, doc):
        """
        Analyzes the Keywords on the Website.
        Args:
            doc: Beautful Soup Object
        Returns:
            earned/warn: Returns if Keyword Count fall in the prerequisties set
        """
        kw_meta = doc.findAll("meta", attrs={"name": "keywords"})

        if len(kw_meta) > 0:
            self.warn(WARNINGS["KEYWORDS_META"], kw_meta)

        self.keywords = self._get_keywords(doc)

        del self.keywords[5:]

    def _analyze_wordcount(self, doc):
        """
        Analyzes the Wordcount on the Website.
        Args:
            doc: Beautful Soup Object
        Returns:
            earned/warn: Returns if Wordcount fall in the prerequistie limit
        """
        page_content = self._get_keywords(doc)
        count = sum(freq for word, freq in page_content)
        if count < 2416:
            self.warn(
                WARNINGS["WORDCOUNT_TOO_SHORT"], u"You have {0} words.".format(count)
            )
        else:
            self.earned(BADGES["WORDCOUNT"], u"You have {0} words.".format(count))

    def _render(self):
        """
        Renders the Result of SEO Analysis
        """
        keywords_result = []

        for word, count in self.keywords:
            kw = {
                "keyword": word,
                "frequency": count,
                "in_title": word in self.title.lower(),
                "in_description": word in self.description.lower(),
                "in_header": word in self.headers,
            }
            keywords_result.append(kw)

        return {
            "url": self.url,
            "keywords": keywords_result,
            "issues": self.issues,
            "achieved": self.achieved,
            "title": self.title,
            "description": self.description,
        }

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

    def visible_tags(self, element):
        """
        Finds element tags in the Markup Document.
        Args:
            element: Elements from the Markup Document
        Returns:
            boolean: True/False depending on the availability of the Elements
        """
        non_visible_elements = [
            "style",
            "script",
            "[document]",
            "head",
            "title",
            "meta",
        ]

        if element.parent.name in non_visible_elements:
            return False
        if isinstance(element, bs4.element.Comment):
            return False

        return True

    def tokenize(self, rawtext):
        """
        Tokenizes the Raw Text passed to it by passing through Regex and removing Stop Words.
        Args:
            rawtext: Markup Text
        Returns:
            word: Tokenized Text after removing Stop Words and passing through Regex
        """
        return [
            word
            for word in TOKEN_REGEX.findall(rawtext.lower())
            if word not in ENGLISH_STOP_WORDS
        ]

    def grouped(self, token_list):
        """
        Groups the List with the Token List passed to it.
        Args:
            token_list: List Data Structure
        Returns:
            grouped_list: Dictionary consisting of all the Grouped Lists together
        """
        grouped_list = {}
        for word in token_list:
            if word in grouped_list:
                grouped_list[word] += 1
            else:
                grouped_list[word] = 1

        grouped_list = sorted(grouped_list.items(), key=lambda x: x[1], reverse=True)
        return grouped_list

    def _get_keywords(self, doc):
        """
        Fetches the Keywords present in the given Webpage.
        Args:
            doc: Beautful Soup Object

        Returns:
            keywords: Dictionary of Keywords and their Frequencies
        """
        keywords = {}
        text_elements = filter(self.visible_tags, doc.findAll(text=True))
        page_text = "".join(element.lower() + " " for element in text_elements)
        tokens = self.tokenize(page_text)
        keywords = self.grouped(tokens)

        return keywords
