import unittest
import learnunittests
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from web_scraper_2 import WebScraper
import lxml
import requests


class WebScraperTest(unittest.TestCase):

    def test_parse_html_doc(self):
        print("test parse html doc")
        pass


if __name__ == "__main__":
    unittest.main()