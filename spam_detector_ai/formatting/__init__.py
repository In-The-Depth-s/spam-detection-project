# spam_detector_ai/formatting/__init__.py

from .email_formatter import EmailFormatter
from .legal_templates import LegalTemplates
from .contact_manager import ContactManager, Contact
from .structured_messaging import (
    StructuredMessage,
    MessageFormatter,
    MessageConstraints,
    MessageStandard
)

__all__ = [
    'EmailFormatter',
    'LegalTemplates',
    'ContactManager',
    'Contact',
    'StructuredMessage',
    'MessageFormatter',
    'MessageConstraints',
    'MessageStandard',
]
