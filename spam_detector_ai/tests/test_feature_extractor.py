import unittest
from spam_detector_ai.loading_and_processing.feature_extractor import EnhancedFeatureExtractor


class TestEnhancedFeatureExtractor(unittest.TestCase):
    
    def setUp(self):
        self.extractor = EnhancedFeatureExtractor()
    
    def test_extract_basic_features(self):
        text = "This is a test message"
        features = self.extractor.extract_features(text)
        self.assertIn('text', features)
        self.assertIn('url_features', features)
        self.assertIn('email_features', features)
        self.assertIn('content_features', features)
    
    def test_extract_with_urls(self):
        text = "Visit http://example.com for more information"
        features = self.extractor.extract_features(text)
        self.assertGreater(features['url_features']['url_count'], 0)
    
    def test_extract_with_subject(self):
        text = "Message body"
        subject = "Test Subject"
        features = self.extractor.extract_features(text, subject=subject)
        self.assertEqual(features['subject'], subject)
        self.assertGreater(features['content_features']['subject_length'], 0)
    
    def test_extract_with_sender(self):
        text = "Message body"
        sender = "test@example.com"
        features = self.extractor.extract_features(text, sender_email=sender)
        self.assertIsNotNone(features['email_features']['sender_analysis'])
        self.assertEqual(features['sender_email'], sender)
    
    def test_detect_excessive_caps(self):
        text = "THIS IS ALL CAPS MESSAGE!!!!"
        features = self.extractor.extract_features(text)
        self.assertTrue(features['content_features']['has_excessive_caps'])
    
    def test_detect_excessive_punctuation(self):
        text = "Buy now!!! Amazing deal!!! Don't miss out!!!"
        features = self.extractor.extract_features(text)
        self.assertTrue(features['content_features']['has_excessive_punctuation'])
    
    def test_combined_spam_score_high(self):
        text = "Visit http://192.168.1.1 NOW!!! AMAZING DEAL!!!"
        sender = "spam123@tempmail.com"
        features = self.extractor.extract_features(text, sender_email=sender)
        self.assertGreater(features['combined_spam_score'], 0.3)
    
    def test_combined_spam_score_low(self):
        text = "Hello, this is a normal message from a friend."
        sender = "friend@gmail.com"
        features = self.extractor.extract_features(text, sender_email=sender)
        self.assertLess(features['combined_spam_score'], 0.5)
    
    def test_get_cleaned_text(self):
        text = "Visit http://example.com and http://test.com for info"
        cleaned = self.extractor.get_cleaned_text(text)
        self.assertNotIn('http://', cleaned)
        self.assertNotIn('example.com', cleaned)
        self.assertIn('URL', cleaned)
    
    def test_multiple_urls_increase_score(self):
        text_few = "Visit http://example.com"
        text_many = "Visit http://site1.com http://site2.com http://site3.com http://site4.com"
        
        features_few = self.extractor.extract_features(text_few)
        features_many = self.extractor.extract_features(text_many)
        
        # More URLs should generally increase spam score
        self.assertGreater(features_many['url_features']['url_count'], 
                          features_few['url_features']['url_count'])
    
    def test_word_count(self):
        text = "This is a test message with several words"
        features = self.extractor.extract_features(text)
        self.assertEqual(features['content_features']['word_count'], 8)
    
    def test_empty_text(self):
        features = self.extractor.extract_features("")
        self.assertEqual(features['content_features']['text_length'], 0)
        self.assertEqual(features['url_features']['url_count'], 0)


if __name__ == '__main__':
    unittest.main()
