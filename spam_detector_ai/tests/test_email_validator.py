import unittest
from spam_detector_ai.loading_and_processing.email_validator import EmailValidator


class TestEmailValidator(unittest.TestCase):
    
    def setUp(self):
        self.validator = EmailValidator()
    
    def test_validate_valid_email(self):
        email = "user@example.com"
        self.assertTrue(self.validator.validate_email_format(email))
    
    def test_validate_invalid_email(self):
        email = "invalid.email"
        self.assertFalse(self.validator.validate_email_format(email))
    
    def test_extract_emails_from_text(self):
        text = "Contact us at support@example.com or sales@test.com"
        emails = self.validator.extract_emails(text)
        self.assertEqual(len(emails), 2)
        self.assertIn("support@example.com", emails)
        self.assertIn("sales@test.com", emails)
    
    def test_extract_no_emails(self):
        text = "This text has no email addresses"
        emails = self.validator.extract_emails(text)
        self.assertEqual(len(emails), 0)
    
    def test_detect_disposable_email(self):
        email = "user@tempmail.com"
        analysis = self.validator.analyze_email(email)
        self.assertTrue(analysis['is_disposable'])
        self.assertGreater(analysis['suspicious_score'], 0)
    
    def test_detect_free_provider(self):
        email = "user@gmail.com"
        analysis = self.validator.analyze_email(email)
        self.assertTrue(analysis['is_free_provider'])
    
    def test_detect_numbers_in_email(self):
        email = "user123@example.com"
        analysis = self.validator.analyze_email(email)
        self.assertTrue(analysis['has_numbers'])
    
    def test_detect_suspicious_chars(self):
        email = "12345678@example.com"
        analysis = self.validator.analyze_email(email)
        self.assertTrue(analysis['has_suspicious_chars'])
    
    def test_detect_long_local_part(self):
        email = "verylongusernamethatisverylong@example.com"
        analysis = self.validator.analyze_email(email)
        self.assertGreater(analysis['local_part_length'], 20)
    
    def test_detect_consecutive_special_chars(self):
        email = "user..name@example.com"
        analysis = self.validator.analyze_email(email)
        self.assertTrue(analysis['has_suspicious_chars'])
    
    def test_extract_sender_domain(self):
        email = "user@example.com"
        domain = self.validator.extract_sender_domain(email)
        self.assertEqual(domain, "example.com")
    
    def test_extract_domain_invalid_email(self):
        email = "invalid-email"
        domain = self.validator.extract_sender_domain(email)
        self.assertEqual(domain, "")
    
    def test_empty_text(self):
        emails = self.validator.extract_emails("")
        self.assertEqual(len(emails), 0)
    
    def test_none_text(self):
        emails = self.validator.extract_emails(None)
        self.assertEqual(len(emails), 0)
    
    def test_invalid_format_high_score(self):
        email = "not-an-email"
        analysis = self.validator.analyze_email(email)
        self.assertFalse(analysis['is_valid_format'])
        self.assertEqual(analysis['suspicious_score'], 1.0)


if __name__ == '__main__':
    unittest.main()
