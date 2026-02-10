import unittest
from spam_detector_ai.loading_and_processing.url_extractor import URLExtractor


class TestURLExtractor(unittest.TestCase):
    
    def setUp(self):
        self.extractor = URLExtractor()
    
    def test_extract_basic_url(self):
        text = "Check out https://example.com for more info"
        urls = self.extractor.extract_urls(text)
        self.assertGreater(len(urls), 0)
        self.assertTrue(any('example.com' in url for url in urls))
    
    def test_extract_multiple_urls(self):
        text = "Visit http://site1.com and http://site2.com"
        urls = self.extractor.extract_urls(text)
        self.assertGreaterEqual(len(urls), 2)
    
    def test_extract_url_without_protocol(self):
        text = "Visit www.example.com today"
        urls = self.extractor.extract_urls(text)
        self.assertGreater(len(urls), 0)
    
    def test_no_urls(self):
        text = "This is just plain text without any links"
        urls = self.extractor.extract_urls(text)
        self.assertEqual(len(urls), 0)
    
    def test_detect_ip_address_url(self):
        url = "http://192.168.1.1/page"
        analysis = self.extractor.analyze_url(url)
        self.assertTrue(analysis['is_ip_address'])
        self.assertGreater(analysis['suspicious_score'], 0)
    
    def test_detect_suspicious_tld(self):
        url = "http://example.tk"
        analysis = self.extractor.analyze_url(url)
        self.assertTrue(analysis['has_suspicious_tld'])
    
    def test_detect_url_shortener(self):
        url = "http://bit.ly/abc123"
        analysis = self.extractor.analyze_url(url)
        self.assertTrue(analysis['is_url_shortener'])
    
    def test_detect_at_symbol(self):
        url = "http://fake@example.com"
        analysis = self.extractor.analyze_url(url)
        self.assertTrue(analysis['has_at_symbol'])
        self.assertGreater(analysis['suspicious_score'], 0)
    
    def test_long_url_detection(self):
        long_url = "http://example.com/" + "a" * 150
        analysis = self.extractor.analyze_url(long_url)
        self.assertGreater(analysis['url_length'], 100)
    
    def test_extract_and_analyze_aggregate(self):
        text = "Visit http://example.com and http://192.168.1.1"
        urls, aggregate = self.extractor.extract_and_analyze_urls(text)
        self.assertEqual(aggregate['url_count'], 2)
        self.assertTrue(aggregate['has_ip_urls'])
    
    def test_remove_urls(self):
        text = "Check http://example.com and http://test.com for details"
        cleaned = self.extractor.remove_urls(text)
        self.assertNotIn('http://', cleaned)
        self.assertNotIn('example.com', cleaned)
        self.assertIn('URL', cleaned)
    
    def test_empty_text(self):
        urls = self.extractor.extract_urls("")
        self.assertEqual(len(urls), 0)
    
    def test_none_text(self):
        urls = self.extractor.extract_urls(None)
        self.assertEqual(len(urls), 0)


if __name__ == '__main__':
    unittest.main()
