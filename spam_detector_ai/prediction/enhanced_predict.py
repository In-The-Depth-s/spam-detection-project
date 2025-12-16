# spam_detector_ai/prediction/enhanced_predict.py
"""
Enhanced spam detector that incorporates URL analysis, email validation,
and content features for improved spam detection accuracy.
"""

from typing import Optional, Dict, Union
from spam_detector_ai.prediction.predict import VotingSpamDetector
from spam_detector_ai.loading_and_processing.feature_extractor import EnhancedFeatureExtractor


class EnhancedSpamDetector:
    """
    Enhanced spam detector that combines traditional ML models with 
    URL analysis and email validation for improved accuracy.
    """
    
    def __init__(self):
        self.base_detector = VotingSpamDetector()
        self.feature_extractor = EnhancedFeatureExtractor()
        
        # Threshold for combined scoring
        self.spam_threshold = 0.5
        # Weight for feature-based scoring vs ML-based scoring
        self.feature_weight = 0.3
        self.ml_weight = 0.7
    
    def is_spam(self, 
                message: str,
                subject: Optional[str] = None,
                sender_email: Optional[str] = None,
                return_details: bool = False) -> Union[bool, Dict]:
        """
        Determine if a message is spam using enhanced features.
        
        Args:
            message: The email message content
            subject: Optional email subject line
            sender_email: Optional sender email address
            return_details: If True, return detailed analysis instead of just boolean
            
        Returns:
            Boolean indicating if message is spam, or dict with details if return_details=True
        """
        # Extract enhanced features
        features = self.feature_extractor.extract_features(
            text=message,
            subject=subject,
            sender_email=sender_email
        )
        
        # Get ML prediction (using traditional model)
        ml_prediction = self.base_detector.is_spam(message)
        ml_score = 1.0 if ml_prediction else 0.0
        
        # Get feature-based score
        feature_score = features['combined_spam_score']
        
        # Combine scores with weights
        combined_score = (ml_score * self.ml_weight) + (feature_score * self.feature_weight)
        
        # Make final decision
        is_spam_result = combined_score >= self.spam_threshold
        
        if return_details:
            return {
                'is_spam': is_spam_result,
                'combined_score': combined_score,
                'ml_score': ml_score,
                'feature_score': feature_score,
                'features': features,
                'details': self._generate_details(features, ml_prediction)
            }
        
        return is_spam_result
    
    def _generate_details(self, features: Dict, ml_prediction: bool) -> Dict[str, str]:
        """Generate human-readable details about the decision."""
        details = {
            'ml_verdict': 'Spam' if ml_prediction else 'Ham',
            'url_analysis': '',
            'email_analysis': '',
            'content_analysis': ''
        }
        
        # URL analysis details
        url_features = features.get('url_features', {})
        url_count = url_features.get('url_count', 0)
        if url_count > 0:
            suspicious_count = url_features.get('suspicious_url_count', 0)
            details['url_analysis'] = (
                f"Found {url_count} URL(s), {suspicious_count} suspicious. "
                f"Average suspicion score: {url_features.get('avg_suspicious_score', 0.0):.2f}"
            )
            if url_features.get('has_ip_urls'):
                details['url_analysis'] += " Contains IP-based URLs."
            if url_features.get('has_url_shorteners'):
                details['url_analysis'] += " Contains URL shorteners."
        else:
            details['url_analysis'] = "No URLs found."
        
        # Email analysis details
        email_features = features.get('email_features', {})
        sender_analysis = email_features.get('sender_analysis')
        if sender_analysis:
            email = sender_analysis.get('email', '')
            score = sender_analysis.get('suspicious_score', 0.0)
            details['email_analysis'] = f"Sender {email} has suspicion score: {score:.2f}"
            if sender_analysis.get('is_disposable'):
                details['email_analysis'] += " (disposable email)"
        else:
            details['email_analysis'] = "No sender email provided."
        
        # Content analysis
        content_features = features.get('content_features', {})
        flags = []
        if content_features.get('has_excessive_caps'):
            flags.append("excessive capitals")
        if content_features.get('has_excessive_punctuation'):
            flags.append("excessive punctuation")
        
        if flags:
            details['content_analysis'] = f"Content has: {', '.join(flags)}"
        else:
            details['content_analysis'] = "Content appears normal."
        
        return details
    
    def analyze_message(self, 
                       message: str,
                       subject: Optional[str] = None,
                       sender_email: Optional[str] = None) -> Dict:
        """
        Perform a detailed analysis of a message.
        
        Args:
            message: The email message content
            subject: Optional email subject line  
            sender_email: Optional sender email address
            
        Returns:
            Dictionary with detailed analysis results
        """
        return self.is_spam(
            message=message,
            subject=subject,
            sender_email=sender_email,
            return_details=True
        )
