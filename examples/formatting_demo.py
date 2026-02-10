#!/usr/bin/env python3
"""
Demo script for email formatting, contact management, and structured messaging features.
Demonstrates the new capabilities added for email scripting, layout structure,
language translation, and legal compliance.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from spam_detector_ai.formatting import (
    EmailFormatter,
    LegalTemplates,
    ContactManager,
    MessageFormatter,
    MessageConstraints,
    MessageStandard
)


def demo_email_formatting():
    """Demonstrate multi-language email formatting."""
    print("=" * 80)
    print("Email Formatting Demo")
    print("=" * 80)
    print()

    # Create sample analysis (simulated)
    analysis = {
        'is_spam': True,
        'combined_score': 0.85,
        'ml_score': 1.0,
        'feature_score': 0.5,
        'details': {
            'ml_verdict': 'Spam',
            'url_analysis': 'Found 2 suspicious URLs with IP address',
            'email_analysis': 'Disposable email detected (tempmail.com)',
            'content_analysis': 'Excessive punctuation detected'
        }
    }

    # Format in English
    print("1. English Text Report:")
    print("-" * 80)
    formatter_en = EmailFormatter(language='en')
    report = formatter_en.format_text_report(
        analysis,
        "Visit http://suspicious-site.tk NOW!!! Amazing deals!!!",
        subject="LIMITED OFFER",
        sender="spam@tempmail.com"
    )
    print(report)
    print()

    # Format in Spanish
    print("2. Spanish Text Report:")
    print("-" * 80)
    formatter_es = EmailFormatter(language='es')
    report_es = formatter_es.format_text_report(
        analysis,
        "Visit http://suspicious-site.tk NOW!!! Amazing deals!!!",
        subject="LIMITED OFFER",
        sender="spam@tempmail.com"
    )
    print(report_es)
    print()

    # JSON Format
    print("3. JSON Format:")
    print("-" * 80)
    json_report = formatter_en.format_json_report(
        analysis,
        "Visit http://suspicious-site.tk NOW!!! Amazing deals!!!",
        subject="LIMITED OFFER",
        sender="spam@tempmail.com"
    )
    import json
    print(json.dumps(json_report, indent=2))
    print()


def demo_legal_templates():
    """Demonstrate legal compliance templates."""
    print("=" * 80)
    print("Legal Templates Demo")
    print("=" * 80)
    print()

    # English legal notices
    legal_en = LegalTemplates(language='en')
    print("1. English Legal Footer:")
    print("-" * 80)
    print(legal_en.format_footer())
    print()

    # German legal notices
    legal_de = LegalTemplates(language='de')
    print("2. German Privacy Notice:")
    print("-" * 80)
    print(legal_de.get_privacy_notice())
    print()


def demo_contact_management():
    """Demonstrate contact management with legal states."""
    print("=" * 80)
    print("Contact Management Demo")
    print("=" * 80)
    print()

    manager = ContactManager(language='en')

    # Add contacts
    manager.add_contact(
        email="john@example.com",
        name="John Doe",
        organization="Example Corp",
        role="admin"
    )

    manager.add_contact(
        email="jane@example.com",
        name="Jane Smith",
        role="user"
    )

    # Update legal states
    manager.update_legal_states(
        "john@example.com",
        terms=True,
        privacy=True,
        consent=True
    )

    # Check compliance
    print("1. Legal Status Reports:")
    print("-" * 80)
    for email in ["john@example.com", "jane@example.com"]:
        status = manager.get_legal_status_report(email)
        print(f"\n{email}:")
        print(f"  Legally Compliant: {status['legally_compliant']}")
        print(f"  Terms Accepted: {status['terms_accepted']}")
        print(f"  Privacy Accepted: {status['privacy_accepted']}")
        print(f"  Legal Consent: {status['legal_consent']}")

    print()
    print("2. Non-Compliant Contacts:")
    print("-" * 80)
    non_compliant = manager.list_non_compliant_contacts()
    print(f"Non-compliant contacts: {', '.join(non_compliant)}")
    print()

    # Format communication
    print("3. Formatted Communication:")
    print("-" * 80)
    message = manager.format_communication(
        'legal_consent_request',
        'jane@example.com'
    )
    if message:
        print(f"Subject: {message['subject']}")
        print(f"\n{message['body']}")
    print()


def demo_structured_messaging():
    """Demonstrate structured messaging with constraints."""
    print("=" * 80)
    print("Structured Messaging Demo")
    print("=" * 80)
    print()

    formatter = MessageFormatter()

    # Test 1: Long line wrapping
    print("1. Line Wrapping (max 50 chars per line):")
    print("-" * 80)
    long_text = "This is a very long line that will be automatically wrapped at word boundaries to ensure compliance with message formatting standards and readability requirements."

    constraints = MessageConstraints(max_line_length=50, wrap_long_lines=True)
    message = formatter.format_message(long_text, constraints)

    print(message.get_formatted_content())
    print(f"\nLines: {message.get_line_count()}, Chars: {message.get_char_count()}")
    print()

    # Test 2: RFC 5322 compliance
    print("2. RFC 5322 Message Format:")
    print("-" * 80)
    header = {
        'From': 'sender@example.com',
        'To': 'recipient@example.com',
        'Subject': 'Spam Detection Report',
        'Date': '2026-02-10 12:00:00'
    }
    body = "This is the message body content."

    formatted = formatter.format_with_header(body, header)
    print(formatted)
    print()

    # Test 3: Compliance validation
    print("3. Standards Compliance Check:")
    print("-" * 80)
    test_message = "Short message"
    report = formatter.validate_standards_compliance(test_message, MessageStandard.RFC5322)

    print(f"Is Compliant: {report['is_compliant']}")
    print(f"Actual Lines: {report['actual']['line_count']}")
    print(f"Actual Chars: {report['actual']['char_count']}")
    print(f"Violations: {report['violations']}")
    print()


def main():
    """Run all demos."""
    print("\n")
    print("╔" + "═" * 78 + "╗")
    print("║" + "Email Scripting, Formatting & Legal Compliance Demo".center(78) + "║")
    print("╚" + "═" * 78 + "╝")
    print()

    try:
        demo_email_formatting()
        demo_legal_templates()
        demo_contact_management()
        demo_structured_messaging()

        print("=" * 80)
        print("Demo completed successfully!")
        print("=" * 80)

    except Exception as e:
        print(f"\nError during demo: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
