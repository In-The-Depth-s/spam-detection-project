# spam_detector_ai/formatting/contact_manager.py
"""
Contact management and communication utilities for spam detection services.
Provides structured contact information handling and communication templates.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Contact:
    """Represents a contact entity with credentials and legal state."""
    email: str
    name: Optional[str] = None
    organization: Optional[str] = None
    role: str = "user"
    credentials: Dict[str, str] = field(default_factory=dict)
    legal_consent: bool = False
    consent_date: Optional[datetime] = None
    privacy_accepted: bool = False
    terms_accepted: bool = False
    contact_preferences: Dict[str, bool] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    last_updated: datetime = field(default_factory=datetime.now)

    def update_legal_state(self, terms: bool = False, privacy: bool = False, consent: bool = False):
        """Update legal acceptance states."""
        if terms:
            self.terms_accepted = True
        if privacy:
            self.privacy_accepted = True
        if consent:
            self.legal_consent = True
            self.consent_date = datetime.now()
        self.last_updated = datetime.now()

    def is_legally_compliant(self) -> bool:
        """Check if contact has accepted all required legal terms."""
        return self.terms_accepted and self.privacy_accepted and self.legal_consent

    def to_dict(self) -> Dict:
        """Convert contact to dictionary."""
        return {
            'email': self.email,
            'name': self.name,
            'organization': self.organization,
            'role': self.role,
            'legal_consent': self.legal_consent,
            'consent_date': self.consent_date.isoformat() if self.consent_date else None,
            'privacy_accepted': self.privacy_accepted,
            'terms_accepted': self.terms_accepted,
            'legally_compliant': self.is_legally_compliant(),
            'created_at': self.created_at.isoformat(),
            'last_updated': self.last_updated.isoformat()
        }


class ContactManager:
    """Manages contacts and communication templates with legal compliance tracking."""

    def __init__(self, language: str = 'en'):
        """
        Initialize contact manager.

        Args:
            language: Language code for communication templates
        """
        self.language = language
        self.contacts: Dict[str, Contact] = {}
        self._load_communication_templates()

    def _load_communication_templates(self):
        """Load communication templates in multiple languages."""
        self.communication_templates = {
            'en': {
                'spam_notification': {
                    'subject': 'Spam Detected in Your Message',
                    'body': (
                        "Dear {name},\n\n"
                        "Our spam detection system has flagged a message from {sender} "
                        "with subject '{subject}' as potential spam.\n\n"
                        "Confidence Score: {score:.0%}\n\n"
                        "Please review the message and take appropriate action.\n\n"
                        "Best regards,\n"
                        "Spam Detection Service"
                    )
                },
                'legal_consent_request': {
                    'subject': 'Legal Consent Required - Spam Detection Service',
                    'body': (
                        "Dear {name},\n\n"
                        "To use our spam detection service, we require your consent to:\n"
                        "- Analyze email content for spam detection\n"
                        "- Process sender information and URLs\n"
                        "- Apply machine learning models to your messages\n\n"
                        "Please review our Terms of Service and Privacy Policy.\n\n"
                        "By continuing to use this service, you agree to these terms.\n\n"
                        "Best regards,\n"
                        "Spam Detection Service"
                    )
                },
                'credentials_update': {
                    'subject': 'Credentials Update Required',
                    'body': (
                        "Dear {name},\n\n"
                        "Your credentials for the spam detection service need to be updated.\n\n"
                        "Please log in to update your authentication information.\n\n"
                        "Best regards,\n"
                        "Spam Detection Service"
                    )
                }
            },
            'es': {
                'spam_notification': {
                    'subject': 'Spam Detectado en su Mensaje',
                    'body': (
                        "Estimado/a {name},\n\n"
                        "Nuestro sistema de detección de spam ha marcado un mensaje de {sender} "
                        "con asunto '{subject}' como posible spam.\n\n"
                        "Puntuación de Confianza: {score:.0%}\n\n"
                        "Por favor, revise el mensaje y tome las medidas apropiadas.\n\n"
                        "Atentamente,\n"
                        "Servicio de Detección de Spam"
                    )
                },
                'legal_consent_request': {
                    'subject': 'Consentimiento Legal Requerido - Servicio de Detección de Spam',
                    'body': (
                        "Estimado/a {name},\n\n"
                        "Para utilizar nuestro servicio de detección de spam, requerimos su "
                        "consentimiento para:\n"
                        "- Analizar el contenido del correo electrónico para detectar spam\n"
                        "- Procesar información del remitente y URLs\n"
                        "- Aplicar modelos de aprendizaje automático a sus mensajes\n\n"
                        "Por favor, revise nuestros Términos de Servicio y Política de Privacidad.\n\n"
                        "Al continuar usando este servicio, acepta estos términos.\n\n"
                        "Atentamente,\n"
                        "Servicio de Detección de Spam"
                    )
                },
                'credentials_update': {
                    'subject': 'Actualización de Credenciales Requerida',
                    'body': (
                        "Estimado/a {name},\n\n"
                        "Sus credenciales para el servicio de detección de spam necesitan ser "
                        "actualizadas.\n\n"
                        "Por favor, inicie sesión para actualizar su información de autenticación.\n\n"
                        "Atentamente,\n"
                        "Servicio de Detección de Spam"
                    )
                }
            }
        }

    def add_contact(self, email: str, name: Optional[str] = None,
                   organization: Optional[str] = None, role: str = "user") -> Contact:
        """
        Add a new contact to the manager.

        Args:
            email: Contact email address
            name: Contact name
            organization: Organization name
            role: Contact role (user, admin, etc.)

        Returns:
            Created Contact object
        """
        contact = Contact(
            email=email,
            name=name,
            organization=organization,
            role=role
        )
        self.contacts[email] = contact
        return contact

    def get_contact(self, email: str) -> Optional[Contact]:
        """Get contact by email address."""
        return self.contacts.get(email)

    def update_contact_credentials(self, email: str, credentials: Dict[str, str]) -> bool:
        """
        Update contact credentials.

        Args:
            email: Contact email
            credentials: Dictionary of credential key-value pairs

        Returns:
            True if successful, False if contact not found
        """
        contact = self.contacts.get(email)
        if contact:
            contact.credentials.update(credentials)
            contact.last_updated = datetime.now()
            return True
        return False

    def update_legal_states(self, email: str, terms: bool = False,
                          privacy: bool = False, consent: bool = False) -> bool:
        """
        Update legal acceptance states for a contact.

        Args:
            email: Contact email
            terms: Accept terms of service
            privacy: Accept privacy policy
            consent: Provide legal consent

        Returns:
            True if successful, False if contact not found
        """
        contact = self.contacts.get(email)
        if contact:
            contact.update_legal_state(terms, privacy, consent)
            return True
        return False

    def format_communication(self, template_type: str, recipient_email: str,
                           **kwargs) -> Optional[Dict[str, str]]:
        """
        Format a communication message using templates.

        Args:
            template_type: Type of communication template
            recipient_email: Recipient contact email
            **kwargs: Template variables

        Returns:
            Dictionary with 'subject' and 'body' or None if contact not found
        """
        contact = self.contacts.get(recipient_email)
        if not contact:
            return None

        templates = self.communication_templates.get(
            self.language,
            self.communication_templates['en']
        )

        template = templates.get(template_type)
        if not template:
            return None

        # Add contact info to kwargs
        kwargs['name'] = contact.name or contact.email

        return {
            'subject': template['subject'],
            'body': template['body'].format(**kwargs)
        }

    def get_legal_status_report(self, email: str) -> Optional[Dict]:
        """
        Get legal compliance status report for a contact.

        Args:
            email: Contact email

        Returns:
            Dictionary with legal status information
        """
        contact = self.contacts.get(email)
        if not contact:
            return None

        return {
            'email': contact.email,
            'legally_compliant': contact.is_legally_compliant(),
            'terms_accepted': contact.terms_accepted,
            'privacy_accepted': contact.privacy_accepted,
            'legal_consent': contact.legal_consent,
            'consent_date': contact.consent_date.isoformat() if contact.consent_date else None,
            'last_updated': contact.last_updated.isoformat()
        }

    def list_non_compliant_contacts(self) -> List[str]:
        """Get list of contacts who haven't accepted all legal terms."""
        return [
            email for email, contact in self.contacts.items()
            if not contact.is_legally_compliant()
        ]

    def export_contacts(self) -> List[Dict]:
        """Export all contacts as list of dictionaries."""
        return [contact.to_dict() for contact in self.contacts.values()]
