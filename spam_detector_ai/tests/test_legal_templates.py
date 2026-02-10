import unittest
from spam_detector_ai.formatting import LegalTemplates


class TestLegalTemplates(unittest.TestCase):
    """Test legal templates functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.templates_en = LegalTemplates(language='en')
        self.templates_es = LegalTemplates(language='es')
        self.templates_fr = LegalTemplates(language='fr')
        self.templates_de = LegalTemplates(language='de')

    def test_initialization(self):
        """Test templates initialization."""
        self.assertEqual(self.templates_en.language, 'en')
        self.assertEqual(self.templates_es.language, 'es')

    def test_get_disclaimer_english(self):
        """Test getting disclaimer in English."""
        disclaimer = self.templates_en.get_disclaimer()
        self.assertIsInstance(disclaimer, str)
        self.assertIn('DISCLAIMER', disclaimer)
        self.assertIn('spam detection', disclaimer)
        self.assertIn('warranty', disclaimer)

    def test_get_disclaimer_spanish(self):
        """Test getting disclaimer in Spanish."""
        disclaimer = self.templates_es.get_disclaimer()
        self.assertIn('DESCARGO DE RESPONSABILIDAD', disclaimer)

    def test_get_data_processing_notice(self):
        """Test getting data processing notice."""
        notice = self.templates_en.get_data_processing_notice()
        self.assertIn('DATA PROCESSING', notice)
        self.assertIn('analyzes email content', notice)

    def test_get_terms_of_service(self):
        """Test getting terms of service."""
        terms = self.templates_en.get_terms_of_service()
        self.assertIn('TERMS OF SERVICE', terms)
        self.assertIn('using this spam detection service', terms)

    def test_get_privacy_notice(self):
        """Test getting privacy notice."""
        privacy = self.templates_en.get_privacy_notice()
        self.assertIn('PRIVACY NOTICE', privacy)
        self.assertIn('privacy', privacy)

    def test_get_legal_compliance(self):
        """Test getting legal compliance notice."""
        compliance = self.templates_en.get_legal_compliance()
        self.assertIn('LEGAL COMPLIANCE', compliance)
        self.assertIn('data protection', compliance)

    def test_get_all_notices(self):
        """Test getting all notices at once."""
        all_notices = self.templates_en.get_all_notices()
        self.assertIsInstance(all_notices, dict)
        self.assertIn('disclaimer', all_notices)
        self.assertIn('data_processing', all_notices)
        self.assertIn('terms_of_service', all_notices)
        self.assertIn('privacy_notice', all_notices)
        self.assertIn('legal_compliance', all_notices)

    def test_format_footer(self):
        """Test formatting complete legal footer."""
        footer = self.templates_en.format_footer()
        self.assertIn('DISCLAIMER', footer)
        self.assertIn('PRIVACY NOTICE', footer)
        self.assertIn('LEGAL COMPLIANCE', footer)
        self.assertIn('=' * 70, footer)

    def test_all_languages_have_templates(self):
        """Test that all languages have all required templates."""
        languages = ['en', 'es', 'fr', 'de']
        required_keys = [
            'disclaimer',
            'data_processing',
            'terms_of_service',
            'privacy_notice',
            'legal_compliance'
        ]

        for lang in languages:
            templates = LegalTemplates(language=lang)
            all_notices = templates.get_all_notices()
            for key in required_keys:
                self.assertIn(key, all_notices, f"Missing {key} in {lang}")
                self.assertTrue(len(all_notices[key]) > 0)


if __name__ == '__main__':
    unittest.main()
