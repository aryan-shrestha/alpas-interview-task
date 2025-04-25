from django.test import TestCase

from scraper.utils import extract_data_from_urls, get_html, parse_html

# Create your tests here.

class ScraperTestCase(TestCase):
    def setUp(self):
        self.urls = [
            'https://birgunjmun.gov.np/en',
            'https://mechinagarmun.gov.np/en',
            'https://melaulimun.gov/'
        ]

    def test_extract_data_from_urls(self):
        """
        Test the extract_data_from_urls function.
        """
        for url in self.urls:
            all_data = extract_data_from_urls(self.urls)
        
        for data in all_data:
            print(data)