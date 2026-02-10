import unittest
from spam_detector_ai.formatting import (
    StructuredMessage,
    MessageFormatter,
    MessageConstraints,
    MessageStandard
)


class TestStructuredMessage(unittest.TestCase):
    """Test StructuredMessage functionality."""

    def test_basic_message(self):
        """Test creating a basic structured message."""
        content = "This is a test message.\nWith multiple lines.\nThird line."
        message = StructuredMessage(content)

        self.assertEqual(message.get_line_count(), 3)
        self.assertGreater(message.get_char_count(), 0)
        self.assertTrue(message.is_compliant())

    def test_long_line_wrapping(self):
        """Test wrapping of long lines."""
        # Create a line longer than default 78 chars
        long_line = "a" * 100

        constraints = MessageConstraints(max_line_length=78, wrap_long_lines=True)
        message = StructuredMessage(long_line, constraints)

        # Should be wrapped into multiple lines
        self.assertGreater(message.get_line_count(), 1)
        for line in message.lines:
            self.assertLessEqual(len(line), 78)

    def test_enforce_line_limit(self):
        """Test enforcing maximum line limit."""
        # Create content with many lines
        content = '\n'.join([f"Line {i}" for i in range(100)])

        constraints = MessageConstraints(max_lines=50, enforce_limits=True)
        message = StructuredMessage(content, constraints)

        self.assertEqual(message.get_line_count(), 50)
        self.assertTrue(message.metadata['truncated'])

    def test_word_boundary_wrapping(self):
        """Test that wrapping respects word boundaries."""
        content = "This is a very long line that should be wrapped at word boundaries " * 2

        constraints = MessageConstraints(max_line_length=50, wrap_long_lines=True)
        message = StructuredMessage(content, constraints)

        # Lines shouldn't have content after max length (except last line)
        for i, line in enumerate(message.lines[:-1]):  # Check all but last line
            self.assertLessEqual(len(line), 50)

    def test_compliance_report(self):
        """Test generating compliance report."""
        content = "Test message"
        message = StructuredMessage(content)

        report = message.get_compliance_report()

        self.assertIn('is_compliant', report)
        self.assertIn('constraints', report)
        self.assertIn('actual', report)
        self.assertIn('violations', report)
        self.assertTrue(report['is_compliant'])

    def test_violations_detected(self):
        """Test that violations are properly detected."""
        # Create many lines to violate line count limit
        content = '\n'.join([f"Line {i}" for i in range(200)])

        constraints = MessageConstraints(
            max_lines=100,
            enforce_limits=False  # Don't truncate, just report
        )
        message = StructuredMessage(content, constraints)

        # Should detect violations in the report (even if enforce_limits=False)
        violations = message._get_violations()
        self.assertGreater(len(violations), 0)
        self.assertIn('Exceeds max lines', violations[0])


class TestMessageFormatter(unittest.TestCase):
    """Test MessageFormatter functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.formatter = MessageFormatter()

    def test_format_message(self):
        """Test basic message formatting."""
        content = "Test message content"
        message = self.formatter.format_message(content)

        self.assertIsInstance(message, StructuredMessage)
        self.assertEqual(message.get_formatted_content(), content)

    def test_format_with_custom_constraints(self):
        """Test formatting with custom constraints."""
        content = "a" * 100

        constraints = MessageConstraints(max_line_length=50)
        message = self.formatter.format_message(content, constraints)

        # Should be wrapped
        self.assertGreater(message.get_line_count(), 1)

    def test_format_with_header(self):
        """Test formatting message with RFC 5322-style header."""
        content = "Message body"
        header = {
            'From': 'sender@example.com',
            'To': 'recipient@example.com',
            'Subject': 'Test Subject'
        }

        formatted = self.formatter.format_with_header(content, header)

        self.assertIn('From: sender@example.com', formatted)
        self.assertIn('To: recipient@example.com', formatted)
        self.assertIn('Subject: Test Subject', formatted)
        self.assertIn('Message body', formatted)

    def test_format_with_long_header(self):
        """Test formatting with very long header value."""
        content = "Body"
        header = {
            'Subject': 'This is a very long subject line that exceeds the normal line length limit and should be wrapped properly'
        }

        formatted = self.formatter.format_with_header(content, header)

        # Should contain wrapped subject
        self.assertIn('Subject:', formatted)
        lines = formatted.split('\n')
        # Check no single line is too long
        for line in lines:
            self.assertLessEqual(len(line), 80)

    def test_validate_rfc5322_compliance(self):
        """Test RFC 5322 compliance validation."""
        content = "Standard email message content"

        report = self.formatter.validate_standards_compliance(
            content,
            MessageStandard.RFC5322
        )

        self.assertIn('is_compliant', report)
        self.assertIn('constraints', report)
        self.assertEqual(report['constraints']['standard'], 'rfc5322')

    def test_apply_word_limits(self):
        """Test applying word count limits."""
        content = "This is a test message with many words in it"
        words = content.split()

        limited = self.formatter.apply_word_limits(content, max_words=5)

        limited_words = limited.replace('...', '').split()
        self.assertLessEqual(len(limited_words), 5)
        self.assertTrue(limited.endswith('...'))

    def test_create_summary(self):
        """Test creating message summary."""
        content = '\n'.join([
            "First line of content",
            "Second line of content",
            "Third line of content",
            "Fourth line of content",
            "Fifth line of content",
            "Sixth line of content"
        ])

        summary = self.formatter.create_summary(content, max_lines=3)

        summary_lines = summary.split('\n')
        self.assertEqual(len(summary_lines), 3)

    def test_summary_with_long_lines(self):
        """Test summary with lines exceeding character limit."""
        long_line = "a" * 100

        summary = self.formatter.create_summary(long_line, max_lines=1, max_chars_per_line=50)

        self.assertTrue(len(summary) <= 50)
        self.assertTrue(summary.endswith('...'))


class TestMessageConstraints(unittest.TestCase):
    """Test MessageConstraints configuration."""

    def test_default_constraints(self):
        """Test default constraint values."""
        constraints = MessageConstraints()

        self.assertEqual(constraints.max_line_length, 78)
        self.assertEqual(constraints.max_lines, 1000)
        self.assertTrue(constraints.wrap_long_lines)
        self.assertEqual(constraints.standard, MessageStandard.PLAIN_TEXT)

    def test_custom_constraints(self):
        """Test custom constraint values."""
        constraints = MessageConstraints(
            max_line_length=100,
            max_lines=500,
            wrap_long_lines=False,
            standard=MessageStandard.RFC5322
        )

        self.assertEqual(constraints.max_line_length, 100)
        self.assertEqual(constraints.max_lines, 500)
        self.assertFalse(constraints.wrap_long_lines)
        self.assertEqual(constraints.standard, MessageStandard.RFC5322)


if __name__ == '__main__':
    unittest.main()
