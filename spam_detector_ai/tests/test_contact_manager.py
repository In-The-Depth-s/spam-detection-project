import unittest
from datetime import datetime
from spam_detector_ai.formatting import ContactManager, Contact


class TestContact(unittest.TestCase):
    """Test Contact dataclass functionality."""

    def test_contact_creation(self):
        """Test creating a contact."""
        contact = Contact(
            email="test@example.com",
            name="Test User",
            organization="Test Org"
        )

        self.assertEqual(contact.email, "test@example.com")
        self.assertEqual(contact.name, "Test User")
        self.assertEqual(contact.organization, "Test Org")
        self.assertFalse(contact.legal_consent)
        self.assertFalse(contact.terms_accepted)

    def test_update_legal_state(self):
        """Test updating legal acceptance states."""
        contact = Contact(email="test@example.com")

        self.assertFalse(contact.is_legally_compliant())

        contact.update_legal_state(terms=True, privacy=True, consent=True)

        self.assertTrue(contact.terms_accepted)
        self.assertTrue(contact.privacy_accepted)
        self.assertTrue(contact.legal_consent)
        self.assertTrue(contact.is_legally_compliant())
        self.assertIsNotNone(contact.consent_date)

    def test_to_dict(self):
        """Test converting contact to dictionary."""
        contact = Contact(
            email="test@example.com",
            name="Test User"
        )
        contact.update_legal_state(terms=True, privacy=True, consent=True)

        contact_dict = contact.to_dict()

        self.assertIsInstance(contact_dict, dict)
        self.assertEqual(contact_dict['email'], "test@example.com")
        self.assertEqual(contact_dict['name'], "Test User")
        self.assertTrue(contact_dict['legally_compliant'])


class TestContactManager(unittest.TestCase):
    """Test ContactManager functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.manager = ContactManager(language='en')

    def test_initialization(self):
        """Test manager initialization."""
        self.assertEqual(self.manager.language, 'en')
        self.assertIsInstance(self.manager.contacts, dict)

    def test_add_contact(self):
        """Test adding a contact."""
        contact = self.manager.add_contact(
            email="test@example.com",
            name="Test User",
            organization="Test Org",
            role="admin"
        )

        self.assertIsInstance(contact, Contact)
        self.assertEqual(contact.email, "test@example.com")
        self.assertEqual(contact.role, "admin")

        # Check it's stored in manager
        retrieved = self.manager.get_contact("test@example.com")
        self.assertEqual(retrieved.email, "test@example.com")

    def test_get_contact(self):
        """Test retrieving a contact."""
        self.manager.add_contact(email="test@example.com", name="Test User")

        contact = self.manager.get_contact("test@example.com")
        self.assertIsNotNone(contact)
        self.assertEqual(contact.email, "test@example.com")

        # Non-existent contact
        non_existent = self.manager.get_contact("nonexistent@example.com")
        self.assertIsNone(non_existent)

    def test_update_contact_credentials(self):
        """Test updating contact credentials."""
        self.manager.add_contact(email="test@example.com")

        result = self.manager.update_contact_credentials(
            "test@example.com",
            {"api_key": "abc123", "token": "xyz789"}
        )

        self.assertTrue(result)

        contact = self.manager.get_contact("test@example.com")
        self.assertEqual(contact.credentials["api_key"], "abc123")

    def test_update_legal_states(self):
        """Test updating legal states."""
        self.manager.add_contact(email="test@example.com")

        result = self.manager.update_legal_states(
            "test@example.com",
            terms=True,
            privacy=True,
            consent=True
        )

        self.assertTrue(result)

        contact = self.manager.get_contact("test@example.com")
        self.assertTrue(contact.is_legally_compliant())

    def test_format_communication(self):
        """Test formatting communications."""
        self.manager.add_contact(
            email="test@example.com",
            name="Test User"
        )

        message = self.manager.format_communication(
            'spam_notification',
            'test@example.com',
            sender='spam@bad.com',
            subject='Spam Subject',
            score=0.85
        )

        self.assertIsNotNone(message)
        self.assertIn('subject', message)
        self.assertIn('body', message)
        self.assertIn('Test User', message['body'])
        self.assertIn('85%', message['body'])

    def test_get_legal_status_report(self):
        """Test getting legal status report."""
        self.manager.add_contact(email="test@example.com")
        self.manager.update_legal_states(
            "test@example.com",
            terms=True,
            privacy=True
        )

        report = self.manager.get_legal_status_report("test@example.com")

        self.assertIsNotNone(report)
        self.assertIn('email', report)
        self.assertIn('legally_compliant', report)
        self.assertTrue(report['terms_accepted'])
        self.assertTrue(report['privacy_accepted'])
        self.assertFalse(report['legally_compliant'])  # Missing consent

    def test_list_non_compliant_contacts(self):
        """Test listing non-compliant contacts."""
        # Add compliant contact
        self.manager.add_contact(email="compliant@example.com")
        self.manager.update_legal_states(
            "compliant@example.com",
            terms=True,
            privacy=True,
            consent=True
        )

        # Add non-compliant contact
        self.manager.add_contact(email="noncompliant@example.com")

        non_compliant = self.manager.list_non_compliant_contacts()

        self.assertIn("noncompliant@example.com", non_compliant)
        self.assertNotIn("compliant@example.com", non_compliant)

    def test_export_contacts(self):
        """Test exporting all contacts."""
        self.manager.add_contact(email="user1@example.com", name="User 1")
        self.manager.add_contact(email="user2@example.com", name="User 2")

        exported = self.manager.export_contacts()

        self.assertEqual(len(exported), 2)
        self.assertIsInstance(exported, list)
        self.assertIsInstance(exported[0], dict)


if __name__ == '__main__':
    unittest.main()
