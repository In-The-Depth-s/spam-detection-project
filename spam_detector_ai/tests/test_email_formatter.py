import unittest
from spam_detector_ai.formatting import EmailFormatter


class TestEmailFormatter(unittest.TestCase):
    """Test email formatting functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.formatter_en = EmailFormatter(language='en')
        self.formatter_es = EmailFormatter(language='es')

        self.sample_analysis = {
            'is_spam': True,
            'combined_score': 0.85,
            'ml_score': 1.0,
            'feature_score': 0.5,
            'details': {
                'ml_verdict': 'Spam',
                'url_analysis': 'Found 2 suspicious URLs',
                'email_analysis': 'Disposable email detected',
                'content_analysis': 'Excessive punctuation'
            }
        }

    def test_initialization(self):
        """Test formatter initialization."""
        self.assertEqual(self.formatter_en.language, 'en')
        self.assertIn('en', self.formatter_en.templates)
        self.assertIn('es', self.formatter_es.templates)

    def test_format_text_report_english(self):
        """Test text report formatting in English."""
        report = self.formatter_en.format_text_report(
            self.sample_analysis,
            "Test message content",
            subject="Test Subject",
            sender="test@example.com"
        )

        self.assertIn('Spam Analysis Report', report)
        self.assertIn('SPAM DETECTED', report)
        self.assertIn('85.00%', report)  # Changed from '85%'
        self.assertIn('Test Subject', report)
        self.assertIn('test@example.com', report)
        self.assertIn('URL Analysis', report)

    def test_format_text_report_spanish(self):
        """Test text report formatting in Spanish."""
        report = self.formatter_es.format_text_report(
            self.sample_analysis,
            "Contenido del mensaje",
            subject="Asunto de Prueba",
            sender="prueba@ejemplo.com"
        )

        self.assertIn('Informe de Análisis de Spam', report)
        self.assertIn('SPAM DETECTADO', report)
        self.assertIn('Asunto de Prueba', report)

    def test_format_html_report(self):
        """Test HTML report formatting."""
        html = self.formatter_en.format_html_report(
            self.sample_analysis,
            "Test message",
            subject="Test",
            sender="test@example.com"
        )

        self.assertIn('<!DOCTYPE html>', html)
        self.assertIn('SPAM DETECTED', html)
        self.assertIn('85.00%', html)  # Changed from '85%'
        self.assertIn('test@example.com', html)
        self.assertIn('<style>', html)

    def test_format_json_report(self):
        """Test JSON report formatting."""
        json_report = self.formatter_en.format_json_report(
            self.sample_analysis,
            "Test message content",
            subject="Test",
            sender="test@example.com"
        )

        self.assertIsInstance(json_report, dict)
        self.assertEqual(json_report['verdict'], 'spam')
        self.assertEqual(json_report['confidence_score'], 0.85)
        self.assertEqual(json_report['sender'], 'test@example.com')
        self.assertIn('timestamp', json_report)

    def test_not_spam_verdict(self):
        """Test formatting for non-spam messages."""
        analysis = {
            'is_spam': False,
            'combined_score': 0.2,
            'details': {}
        }

        report = self.formatter_en.format_text_report(
            analysis,
            "Legitimate message"
        )

        self.assertIn('NOT SPAM', report)
        self.assertIn('20.00%', report)  # Changed from '20%'

    def test_without_optional_fields(self):
        """Test formatting without subject and sender."""
        report = self.formatter_en.format_text_report(
            self.sample_analysis,
            "Test message"
        )

        # Should still work without optional fields
        self.assertIn('Spam Analysis Report', report)
        self.assertIn('SPAM DETECTED', report)


if __name__ == '__main__':
    unittest.main()
