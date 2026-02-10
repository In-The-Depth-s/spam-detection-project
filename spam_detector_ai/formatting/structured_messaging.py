# spam_detector_ai/formatting/structured_messaging.py
"""
Structured messaging with word line limits and configurable standards.
Provides utilities for formatting messages with constraints and standards compliance.
"""

from typing import List, Dict, Optional
from dataclasses import dataclass
from enum import Enum


class MessageStandard(Enum):
    """Message formatting standards."""
    RFC5322 = "rfc5322"  # Internet Message Format
    PLAIN_TEXT = "plain_text"
    HTML = "html"
    STRUCTURED = "structured"


@dataclass
class MessageConstraints:
    """Configuration for message formatting constraints."""
    max_line_length: int = 78  # RFC 5322 recommendation
    max_lines: int = 1000
    max_total_chars: int = 50000
    wrap_long_lines: bool = True
    enforce_limits: bool = True
    standard: MessageStandard = MessageStandard.PLAIN_TEXT


class StructuredMessage:
    """Represents a structured message with enforced constraints."""

    def __init__(self, content: str, constraints: Optional[MessageConstraints] = None):
        """
        Initialize structured message.

        Args:
            content: Message content
            constraints: Message constraints configuration
        """
        self.content = content
        self.constraints = constraints or MessageConstraints()
        self.lines: List[str] = []
        self.metadata: Dict = {}
        self._process_content()

    def _process_content(self):
        """Process content according to constraints."""
        if not self.content:
            return

        # Split into lines
        raw_lines = self.content.split('\n')

        # Apply constraints
        for line in raw_lines:
            if self.constraints.wrap_long_lines and len(line) > self.constraints.max_line_length:
                # Wrap long lines
                wrapped = self._wrap_line(line, self.constraints.max_line_length)
                self.lines.extend(wrapped)
            else:
                if self.constraints.enforce_limits and len(line) > self.constraints.max_line_length:
                    # Truncate if enforcing limits
                    self.lines.append(line[:self.constraints.max_line_length])
                else:
                    self.lines.append(line)

        # Enforce max lines limit
        if self.constraints.enforce_limits and len(self.lines) > self.constraints.max_lines:
            self.lines = self.lines[:self.constraints.max_lines]

        # Update metadata
        self.metadata = {
            'total_lines': len(self.lines),
            'total_chars': sum(len(line) for line in self.lines),
            'max_line_length': max(len(line) for line in self.lines) if self.lines else 0,
            'truncated': len(raw_lines) > len(self.lines),
            'standard': self.constraints.standard.value
        }

    def _wrap_line(self, line: str, max_length: int) -> List[str]:
        """
        Wrap a long line into multiple lines.

        Args:
            line: Line to wrap
            max_length: Maximum line length

        Returns:
            List of wrapped lines
        """
        if len(line) <= max_length:
            return [line]

        wrapped = []
        while len(line) > max_length:
            # Try to break at word boundary
            break_point = line.rfind(' ', 0, max_length)
            if break_point == -1:
                # No space found, break at max_length
                break_point = max_length

            wrapped.append(line[:break_point])
            line = line[break_point:].lstrip()

        if line:
            wrapped.append(line)

        return wrapped

    def get_formatted_content(self) -> str:
        """Get formatted content as string."""
        return '\n'.join(self.lines)

    def get_line_count(self) -> int:
        """Get number of lines."""
        return len(self.lines)

    def get_char_count(self) -> int:
        """Get total character count."""
        return sum(len(line) for line in self.lines)

    def is_compliant(self) -> bool:
        """Check if message meets all constraints."""
        if not self.constraints.enforce_limits:
            return True

        return (
            len(self.lines) <= self.constraints.max_lines and
            all(len(line) <= self.constraints.max_line_length for line in self.lines) and
            self.get_char_count() <= self.constraints.max_total_chars
        )

    def get_compliance_report(self) -> Dict:
        """Get detailed compliance report."""
        return {
            'is_compliant': self.is_compliant(),
            'constraints': {
                'max_line_length': self.constraints.max_line_length,
                'max_lines': self.constraints.max_lines,
                'max_total_chars': self.constraints.max_total_chars,
                'standard': self.constraints.standard.value
            },
            'actual': {
                'line_count': self.get_line_count(),
                'char_count': self.get_char_count(),
                'max_line_length': self.metadata.get('max_line_length', 0)
            },
            'violations': self._get_violations()
        }

    def _get_violations(self) -> List[str]:
        """Get list of constraint violations."""
        violations = []

        if self.get_line_count() > self.constraints.max_lines:
            violations.append(
                f"Exceeds max lines: {self.get_line_count()} > {self.constraints.max_lines}"
            )

        if self.get_char_count() > self.constraints.max_total_chars:
            violations.append(
                f"Exceeds max chars: {self.get_char_count()} > {self.constraints.max_total_chars}"
            )

        max_line_len = self.metadata.get('max_line_length', 0)
        if max_line_len > self.constraints.max_line_length:
            violations.append(
                f"Line too long: {max_line_len} > {self.constraints.max_line_length}"
            )

        return violations


class MessageFormatter:
    """Formats messages according to various standards and constraints."""

    def __init__(self, default_constraints: Optional[MessageConstraints] = None):
        """
        Initialize message formatter.

        Args:
            default_constraints: Default constraints to use
        """
        self.default_constraints = default_constraints or MessageConstraints()

    def format_message(self, content: str,
                      constraints: Optional[MessageConstraints] = None) -> StructuredMessage:
        """
        Format a message with constraints.

        Args:
            content: Message content
            constraints: Optional constraints (uses default if not provided)

        Returns:
            StructuredMessage object
        """
        constraints = constraints or self.default_constraints
        return StructuredMessage(content, constraints)

    def format_with_header(self, content: str, header: Dict[str, str],
                          constraints: Optional[MessageConstraints] = None) -> str:
        """
        Format message with RFC 5322-style header.

        Args:
            content: Message body
            header: Dictionary of header fields
            constraints: Optional constraints

        Returns:
            Formatted message with header
        """
        header_lines = []
        for key, value in header.items():
            # Wrap header values if needed
            if len(f"{key}: {value}") > 78:
                # Simple wrap for header
                header_lines.append(f"{key}: {value[:70]}")
                remaining = value[70:]
                while remaining:
                    header_lines.append(f"  {remaining[:76]}")
                    remaining = remaining[76:]
            else:
                header_lines.append(f"{key}: {value}")

        header_text = '\n'.join(header_lines)
        full_message = f"{header_text}\n\n{content}"

        message = self.format_message(full_message, constraints)
        return message.get_formatted_content()

    def validate_standards_compliance(self, content: str,
                                     standard: MessageStandard) -> Dict:
        """
        Validate message compliance with a specific standard.

        Args:
            content: Message content
            standard: Standard to validate against

        Returns:
            Validation report dictionary
        """
        # Create constraints based on standard
        if standard == MessageStandard.RFC5322:
            constraints = MessageConstraints(
                max_line_length=78,
                max_lines=10000,
                max_total_chars=1000000,
                standard=standard
            )
        elif standard == MessageStandard.PLAIN_TEXT:
            constraints = MessageConstraints(
                max_line_length=80,
                max_lines=10000,
                standard=standard
            )
        else:
            constraints = MessageConstraints(standard=standard)

        message = StructuredMessage(content, constraints)
        return message.get_compliance_report()

    def apply_word_limits(self, content: str, max_words: int) -> str:
        """
        Apply word count limit to content.

        Args:
            content: Input content
            max_words: Maximum word count

        Returns:
            Truncated content if necessary
        """
        words = content.split()
        if len(words) <= max_words:
            return content

        truncated_words = words[:max_words]
        return ' '.join(truncated_words) + '...'

    def create_summary(self, content: str, max_lines: int = 5,
                      max_chars_per_line: int = 80) -> str:
        """
        Create a summary with strict line and character limits.

        Args:
            content: Content to summarize
            max_lines: Maximum number of lines
            max_chars_per_line: Maximum characters per line

        Returns:
            Formatted summary
        """
        lines = content.split('\n')[:max_lines]
        summary_lines = []

        for line in lines:
            if len(line) <= max_chars_per_line:
                summary_lines.append(line)
            else:
                summary_lines.append(line[:max_chars_per_line - 3] + '...')

        return '\n'.join(summary_lines)
