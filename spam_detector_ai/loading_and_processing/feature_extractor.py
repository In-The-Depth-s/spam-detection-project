# spam_detector_ai/loading_and_processing/feature_extractor.py

from typing import Dict, Optional, Any
from spam_detector_ai.loading_and_processing.url_extractor import URLExtractor
from spam_detector_ai.loading_and_processing.email_validator import EmailValidator


class EnhancedFeatureExtractor:
    """
    Extracts enhanced features from email content including URLs, 
    sender information, and content patterns for improved spam detection.
    """
    
    def __init__(self):
        self.url_extractor = URLExtractor()
        self.email_validator = EmailValidator()
    
    def extract_features(self, 
                        text: str, 
                        subject: Optional[str] = None,
                        sender_email: Optional[str] = None) -> Dict[str, Any]:
        """
        Extract comprehensive features from email content.
        
        Args:
            text: The main email content/body
            subject: Optional email subject line
            sender_email: Optional sender email address
            
        Returns:
            Dictionary containing extracted features
        """
        features = {
            'text': text,
            'subject': subject or '',
            'sender_email': sender_email or '',
            'url_features': {},
            'email_features': {},
            'content_features': {},
            'combined_spam_score': 0.0
        }
        
        # Extract URL features from text
        urls, url_analysis = self.url_extractor.extract_and_analyze_urls(text)
        features['url_features'] = url_analysis
        
        # Extract email addresses from content
        content_emails = self.email_validator.extract_emails(text)
        features['email_features']['emails_in_content'] = content_emails
        features['email_features']['email_count_in_content'] = len(content_emails)
        
        # Analyze sender email if provided
        if sender_email:
            sender_analysis = self.email_validator.analyze_email(sender_email)
            features['email_features']['sender_analysis'] = sender_analysis
        else:
            features['email_features']['sender_analysis'] = None
        
        # Extract content features
        features['content_features'] = self._extract_content_features(text, subject)
        
        # Calculate combined spam score
        features['combined_spam_score'] = self._calculate_combined_score(features)
        
        return features
    
    def _extract_content_features(self, text: str, subject: Optional[str] = None) -> Dict[str, Any]:
        """Extract basic content features."""
        features = {
            'text_length': len(text) if text else 0,
            'subject_length': len(subject) if subject else 0,
            'has_excessive_caps': False,
            'has_excessive_punctuation': False,
            'word_count': 0
        }
        
        if text:
            # Count uppercase characters
            uppercase_count = sum(1 for c in text if c.isupper())
            if len(text) > 0:
                uppercase_ratio = uppercase_count / len(text)
                features['has_excessive_caps'] = uppercase_ratio > 0.3
            
            # Count exclamation marks and question marks
            exclamation_count = text.count('!')
            question_count = text.count('?')
            features['has_excessive_punctuation'] = (exclamation_count + question_count) > 5
            
            # Word count
            features['word_count'] = len(text.split())
        
        return features
    
    def _calculate_combined_score(self, features: Dict[str, any]) -> float:
        """
        Calculate a combined spam score based on all features.
        
        Returns:
            Float between 0 and 1, where higher values indicate more spam-like characteristics
        """
        score = 0.0
        weight_sum = 0.0
        
        # URL-based scoring (weight: 0.4)
        url_features = features.get('url_features', {})
        if url_features.get('url_count', 0) > 0:
            url_weight = 0.4
            url_score = min(1.0, url_features.get('avg_suspicious_score', 0.0))
            
            # Bonus for multiple suspicious URLs
            if url_features.get('suspicious_url_count', 0) > 1:
                url_score = min(1.0, url_score + 0.2)
            
            # Bonus for many URLs
            if url_features.get('url_count', 0) > 3:
                url_score = min(1.0, url_score + 0.15)
            
            score += url_score * url_weight
            weight_sum += url_weight
        
        # Email-based scoring (weight: 0.3)
        email_features = features.get('email_features', {})
        sender_analysis = email_features.get('sender_analysis')
        if sender_analysis:
            email_weight = 0.3
            email_score = sender_analysis.get('suspicious_score', 0.0)
            score += email_score * email_weight
            weight_sum += email_weight
        
        # Multiple emails in content can be suspicious
        if email_features.get('email_count_in_content', 0) > 2:
            score += 0.1
            weight_sum += 0.1
        
        # Content-based scoring (weight: 0.2)
        content_features = features.get('content_features', {})
        content_weight = 0.2
        content_score = 0.0
        
        if content_features.get('has_excessive_caps'):
            content_score += 0.3
        if content_features.get('has_excessive_punctuation'):
            content_score += 0.2
        
        score += content_score * content_weight
        weight_sum += content_weight
        
        # Normalize score
        if weight_sum > 0:
            return min(1.0, score / weight_sum)
        else:
            return 0.0
    
    def get_cleaned_text(self, text: str) -> str:
        """
        Get text with URLs removed for traditional ML processing.
        
        Args:
            text: The text to clean
            
        Returns:
            Text with URLs replaced by placeholder
        """
        return self.url_extractor.remove_urls(text)
