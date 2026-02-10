# spam_detector_ai/prediction/__init__.py

from .predict import SpamDetector, VotingSpamDetector
from .enhanced_predict import EnhancedSpamDetector

__all__ = [
    'SpamDetector',
    'VotingSpamDetector',
    'EnhancedSpamDetector',
]
