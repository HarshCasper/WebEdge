import testtools
from webedge import stop_words


class StopWordsTests(testtools.TestCase):

    def setUp(self):
        super(StopWordsTests, self).setUp()
        pass

    def test_stopwords(self):
        words = stop_words.ENGLISH_STOP_WORDS
        self.assertTrue("able" in words)
        self.assertTrue("about" in words)
        self.assertTrue("looks" in words)
        self.assertTrue("zero" in words)
        self.assertEqual(len(words), 635)
