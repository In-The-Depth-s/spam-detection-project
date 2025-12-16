# spam_detector_ai/loading_and_processing/url_extractor.py

import re
from urllib.parse import urlparse
from typing import List, Dict, Tuple, Any


class URLExtractor:
    """Extracts and analyzes URLs from email content for spam detection."""

    def __init__(self):
        # Comprehensive URL regex pattern that matches http, https, ftp, naked domains, and IP addresses
        self.url_pattern = re.compile(
            r'(?:(?:https?|ftp):\/\/)?'  # Optional protocol
            r'(?:'
                r'(?:\d{1,3}\.){3}\d{1,3}'  # IP address pattern
                r'|'  # OR
                r'(?:www\.)?'  # Optional www
                r'(?:[a-zA-Z0-9-]+\.)*'  # Subdomains
                r'[a-zA-Z0-9-]+\.'  # Domain name
                r'[a-zA-Z]{2,}'  # TLD
            r')'
            r'(?::[0-9]{1,5})?'  # Optional port
            r'(?:\/[^\s]*)?',  # Optional path
            re.IGNORECASE
        )

        # Patterns for suspicious URL characteristics
        self.ip_pattern = re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b')
        self.suspicious_tlds = {
            'tk', 'ml', 'ga', 'cf', 'gq',  # Free/disposable TLDs
            'xyz', 'top', 'work', 'click', 'link'  # Often used in spam
        }
        self.url_shorteners = {
            'bit.ly', 'tinyurl.com', 'goo.gl', 'ow.ly', 't.co',
            'is.gd', 'buff.ly', 'adf.ly', 'short.link'
        }

    def extract_urls(self, text: str) -> List[str]:
        """
        Extract all URLs from the given text.

        Args:
            text: The text to extract URLs from

        Returns:
            List of URLs found in the text
        """
        if not text:
            return []

        urls = self.url_pattern.findall(text)
        return [url.strip() for url in urls if url.strip()]

    def analyze_url(self, url: str) -> Dict[str, Any]:
        """
        Analyze a URL for suspicious characteristics.

        Args:
            url: The URL to analyze

        Returns:
            Dictionary containing analysis results
        """
        analysis = {
            'url': url,
            'is_ip_address': False,
            'has_suspicious_tld': False,
            'is_url_shortener': False,
            'url_length': len(url),
            'subdomain_count': 0,
            'has_at_symbol': '@' in url,
            'suspicious_score': 0.0
        }

        # Check if URL uses IP address instead of domain
        if self.ip_pattern.search(url):
            analysis['is_ip_address'] = True
            analysis['suspicious_score'] += 0.3

        # Parse URL to get components
        try:
            parsed = urlparse(url if '://' in url else f'http://{url}')
            domain = parsed.netloc or parsed.path.split('/')[0]

            # Check for suspicious TLD
            if '.' in domain:
                tld = domain.split('.')[-1].lower()
                if tld in self.suspicious_tlds:
                    analysis['has_suspicious_tld'] = True
                    analysis['suspicious_score'] += 0.2

            # Check for URL shorteners
            if any(shortener in domain.lower() for shortener in self.url_shorteners):
                analysis['is_url_shortener'] = True
                analysis['suspicious_score'] += 0.15

            # Count subdomains
            if domain:
                parts = domain.split('.')
                analysis['subdomain_count'] = max(0, len(parts) - 2)
                if analysis['subdomain_count'] > 2:
                    analysis['suspicious_score'] += 0.1
        except Exception:
            analysis['suspicious_score'] += 0.2

        # Check for unusually long URLs
        if analysis['url_length'] > 100:
            analysis['suspicious_score'] += 0.1

        # @ symbol in URL is often used to obfuscate
        if analysis['has_at_symbol']:
            analysis['suspicious_score'] += 0.25

        return analysis

    def extract_and_analyze_urls(self, text: str) -> Tuple[List[str], Dict[str, Any]]:
        """
        Extract URLs from text and provide aggregate analysis.

        Args:
            text: The text to extract and analyze URLs from

        Returns:
            Tuple of (list of URLs, aggregate analysis dict)
        """
        urls = self.extract_urls(text)

        aggregate = {
            'url_count': len(urls),
            'suspicious_url_count': 0,
            'total_suspicious_score': 0.0,
            'avg_suspicious_score': 0.0,
            'has_ip_urls': False,
            'has_url_shorteners': False,
            'urls': []
        }

        for url in urls:
            analysis = self.analyze_url(url)
            aggregate['urls'].append(analysis)
            aggregate['total_suspicious_score'] += analysis['suspicious_score']

            if analysis['suspicious_score'] > 0.3:
                aggregate['suspicious_url_count'] += 1

            if analysis['is_ip_address']:
                aggregate['has_ip_urls'] = True

            if analysis['is_url_shortener']:
                aggregate['has_url_shorteners'] = True

        if urls:
            aggregate['avg_suspicious_score'] = aggregate['total_suspicious_score'] / len(urls)

        return urls, aggregate

    def remove_urls(self, text: str) -> str:
        """
        Remove URLs from text, replacing them with a placeholder.

        Args:
            text: The text to remove URLs from

        Returns:
            Text with URLs replaced by placeholder
        """
        return self.url_pattern.sub(' URL ', text)
