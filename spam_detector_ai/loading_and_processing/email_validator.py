# spam_detector_ai/loading_and_processing/email_validator.py

import re
from typing import Dict


class EmailValidator:
    """Validates and analyzes email addresses for spam detection."""
    
    def __init__(self):
        # Email regex pattern
        self.email_pattern = re.compile(
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        )
        
        # Suspicious email patterns
        self.disposable_domains = {
            'tempmail.com', 'guerrillamail.com', 'mailinator.com',
            '10minutemail.com', 'throwaway.email', 'temp-mail.org',
            'maildrop.cc', 'sharklasers.com', 'spam4.me'
        }
        
        # Common free email providers (not necessarily suspicious but worth tracking)
        self.free_email_providers = {
            'gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com',
            'aol.com', 'icloud.com', 'mail.com', 'protonmail.com'
        }
    
    def extract_emails(self, text: str) -> list:
        """
        Extract email addresses from text.
        
        Args:
            text: The text to extract emails from
            
        Returns:
            List of email addresses found
        """
        if not text:
            return []
        return self.email_pattern.findall(text)
    
    def validate_email_format(self, email: str) -> bool:
        """
        Validate email address format.
        
        Args:
            email: The email address to validate
            
        Returns:
            True if email format is valid, False otherwise
        """
        return bool(self.email_pattern.match(email))
    
    def analyze_email(self, email: str) -> Dict[str, any]:
        """
        Analyze an email address for suspicious characteristics.
        
        Args:
            email: The email address to analyze
            
        Returns:
            Dictionary containing analysis results
        """
        analysis = {
            'email': email,
            'is_valid_format': self.validate_email_format(email),
            'is_disposable': False,
            'is_free_provider': False,
            'has_numbers': False,
            'has_suspicious_chars': False,
            'local_part_length': 0,
            'suspicious_score': 0.0
        }
        
        if not analysis['is_valid_format']:
            analysis['suspicious_score'] = 1.0
            return analysis
        
        try:
            local_part, domain = email.lower().split('@')
            
            # Check domain
            if domain in self.disposable_domains:
                analysis['is_disposable'] = True
                analysis['suspicious_score'] += 0.5
            
            if domain in self.free_email_providers:
                analysis['is_free_provider'] = True
                analysis['suspicious_score'] += 0.05
            
            # Analyze local part
            analysis['local_part_length'] = len(local_part)
            
            # Check for numbers
            if any(char.isdigit() for char in local_part):
                analysis['has_numbers'] = True
            
            # Check for suspicious character patterns
            if len(re.findall(r'[0-9]', local_part)) > len(local_part) / 2:
                # More than half numbers
                analysis['has_suspicious_chars'] = True
                analysis['suspicious_score'] += 0.2
            
            # Very long local part
            if len(local_part) > 20:
                analysis['suspicious_score'] += 0.1
            
            # Multiple consecutive dots or underscores
            if '..' in local_part or '__' in local_part:
                analysis['has_suspicious_chars'] = True
                analysis['suspicious_score'] += 0.15
            
            # Starts or ends with special characters
            if local_part[0] in '._-' or local_part[-1] in '._-':
                analysis['has_suspicious_chars'] = True
                analysis['suspicious_score'] += 0.1
                
        except (ValueError, IndexError):
            analysis['suspicious_score'] = 1.0
        
        return analysis
    
    def extract_sender_domain(self, email: str) -> str:
        """
        Extract the domain from an email address.
        
        Args:
            email: The email address
            
        Returns:
            The domain part of the email, or empty string if invalid
        """
        try:
            return email.split('@')[1].lower()
        except (ValueError, IndexError):
            return ""
