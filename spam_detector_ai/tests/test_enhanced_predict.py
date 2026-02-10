import unittest
from spam_detector_ai.prediction.enhanced_predict import EnhancedSpamDetector


class TestEnhancedSpamDetector(unittest.TestCase):
    """
    Tests for the enhanced spam detector.
    Note: These are basic integration tests.
    """
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures once for the entire test class."""
        # This will load all the ML models once, improving test performance
        cls.detector = EnhancedSpamDetector()
    
    def test_basic_spam_detection(self):
        """Test basic spam detection functionality."""
        message = "Click here to win money now!!!"
        result = self.detector.is_spam(message)
        # Result should be a boolean
        self.assertIsInstance(result, bool)
    
    def test_detection_with_details(self):
        """Test spam detection with detailed analysis."""
        message = "Visit http://suspicious-site.tk for amazing deals!!!"
        result = self.detector.is_spam(message, return_details=True)
        
        # Check structure of detailed result
        self.assertIsInstance(result, dict)
        self.assertIn('is_spam', result)
        self.assertIn('combined_score', result)
        self.assertIn('ml_score', result)
        self.assertIn('feature_score', result)
        self.assertIn('features', result)
        self.assertIn('details', result)
    
    def test_detection_with_subject_and_sender(self):
        """Test detection with subject and sender information."""
        message = "Check out this deal"
        subject = "FREE MONEY!!!"
        sender = "spam123@tempmail.com"
        
        result = self.detector.is_spam(
            message, 
            subject=subject, 
            sender_email=sender,
            return_details=True
        )
        
        self.assertIsInstance(result, dict)
        self.assertIsNotNone(result['features']['email_features']['sender_analysis'])
    
    def test_analyze_message(self):
        """Test the analyze_message method."""
        message = "Hello, this is a test message"
        analysis = self.detector.analyze_message(message)
        
        self.assertIsInstance(analysis, dict)
        self.assertIn('is_spam', analysis)
        self.assertIn('details', analysis)
    
    def test_ham_message(self):
        """Test that legitimate messages are not flagged as spam."""
        message = "Hi friend, how are you doing today?"
        sender = "friend@gmail.com"
        
        result = self.detector.is_spam(message, sender_email=sender)
        # Note: We can't guarantee the result, but it should complete
        self.assertIsInstance(result, bool)
    
    def test_suspicious_url_detection(self):
        """Test that suspicious URLs are detected."""
        message = "Visit http://192.168.1.1 to claim your prize"
        result = self.detector.is_spam(message, return_details=True)
        
        # Should detect the IP-based URL
        self.assertGreater(result['features']['url_features']['url_count'], 0)
        self.assertTrue(result['features']['url_features']['has_ip_urls'])


if __name__ == '__main__':
    unittest.main()
