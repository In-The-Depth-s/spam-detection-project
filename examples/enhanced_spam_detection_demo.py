#!/usr/bin/env python3
"""
Example usage of the Enhanced Spam Detector with URL and email analysis.

This demonstrates the new features added for processing email content,
including URL extraction, email validation, and enhanced spam scoring.
"""

import sys
from pathlib import Path

# Add project root to path for running without installation
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from spam_detector_ai.prediction.enhanced_predict import EnhancedSpamDetector


def main():
    print("=" * 80)
    print("Enhanced Spam Detector - Demo")
    print("=" * 80)
    print()
    
    # Initialize the enhanced spam detector
    print("Initializing Enhanced Spam Detector (loading ML models)...")
    detector = EnhancedSpamDetector()
    print("✓ Detector initialized")
    print()
    
    # Test cases with different characteristics
    test_cases = [
        {
            'name': 'Suspicious URL with IP address',
            'message': 'Visit http://192.168.1.1/prize to claim your $1000 reward NOW!!!',
            'subject': 'URGENT: Claim Your Prize!',
            'sender': 'prize@tempmail.com'
        },
        {
            'name': 'Multiple suspicious URLs',
            'message': 'Check out http://bit.ly/abc and http://example.tk for amazing deals! '
                      'Limited time offer!!!',
            'subject': 'LIMITED TIME OFFER',
            'sender': 'deals123@disposable.com'
        },
        {
            'name': 'Legitimate message',
            'message': 'Hi, I saw your portfolio at https://github.com/yourusername and '
                      'wanted to discuss a potential project.',
            'subject': 'Project Collaboration',
            'sender': 'john.doe@company.com'
        },
        {
            'name': 'Message with excessive formatting',
            'message': 'BUY NOW!!! AMAZING DEALS!!! LIMITED TIME!!! CLICK HERE!!!',
            'subject': 'SALE SALE SALE',
            'sender': 'spam@freemail.com'
        },
        {
            'name': 'Simple spam without URLs',
            'message': 'Congratulations! You have won a million dollars. '
                      'Send us your bank details to claim.',
            'subject': 'You Won!',
            'sender': 'winner@lottery.xyz'
        }
    ]
    
    for i, test in enumerate(test_cases, 1):
        print(f"Test Case {i}: {test['name']}")
        print("-" * 80)
        print(f"Subject: {test['subject']}")
        print(f"From: {test['sender']}")
        print(f"Message: {test['message'][:100]}...")
        print()
        
        # Analyze the message
        result = detector.analyze_message(
            message=test['message'],
            subject=test['subject'],
            sender_email=test['sender']
        )
        
        # Display results
        print(f"Verdict: {'🚫 SPAM' if result['is_spam'] else '✓ HAM (Not Spam)'}")
        print(f"Combined Score: {result['combined_score']:.3f}")
        print(f"ML Score: {result['ml_score']:.3f}")
        print(f"Feature Score: {result['feature_score']:.3f}")
        print()
        
        # Display detailed analysis
        print("Detailed Analysis:")
        details = result['details']
        print(f"  ML Verdict: {details['ml_verdict']}")
        print(f"  URL Analysis: {details['url_analysis']}")
        print(f"  Email Analysis: {details['email_analysis']}")
        print(f"  Content Analysis: {details['content_analysis']}")
        print()
        
        # Show URL features if any
        url_features = result['features']['url_features']
        if url_features['url_count'] > 0:
            print(f"URL Details:")
            print(f"  Total URLs: {url_features['url_count']}")
            print(f"  Suspicious URLs: {url_features['suspicious_url_count']}")
            print(f"  Has IP-based URLs: {url_features['has_ip_urls']}")
            print(f"  Has URL shorteners: {url_features['has_url_shorteners']}")
            print()
        
        print("=" * 80)
        print()


if __name__ == "__main__":
    main()
