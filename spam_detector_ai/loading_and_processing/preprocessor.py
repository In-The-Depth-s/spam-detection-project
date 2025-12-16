# spam_detector_ai/loading_and_processing/preprocessor.py

import re

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


class Preprocessor:
    def __init__(self, preserve_urls=False):
        self.lemmatiser = WordNetLemmatizer()
        self.stopwords_set = set(stopwords.words('english'))
        self.special_char_pattern = re.compile('[^a-zA-Z]')
        self.preserve_urls = preserve_urls
        # URL pattern for optional preservation (matches domains and IP addresses)
        self.url_pattern = re.compile(
            r'(?:(?:https?|ftp):\/\/)?'
            r'(?:'
                r'(?:\d{1,3}\.){3}\d{1,3}'
                r'|'
                r'(?:www\.)?'
                r'(?:[a-zA-Z0-9-]+\.)*'
                r'[a-zA-Z0-9-]+\.'
                r'[a-zA-Z]{2,}'
            r')'
            r'(?::[0-9]{1,5})?'
            r'(?:\/[^\s]*)?',
            re.IGNORECASE
        )

    def preprocess_text(self, text, extract_urls=False):
        """
        Preprocess the text by removing special characters, converting to lowercase,
        removing stopwords, and lemmatizing.
        
        Args:
            text: The text to preprocess
            extract_urls: If True, extract URLs before preprocessing and replace with placeholder
            
        Returns:
            Preprocessed text (and optionally extracted URLs if extract_urls=True)
        """
        urls = []
        
        # Optionally extract URLs before preprocessing
        if extract_urls or self.preserve_urls:
            urls = self.url_pattern.findall(text)
            # Replace URLs with placeholder token
            text = self.url_pattern.sub(' URL ', text)
        
        # Remove all the special characters
        text = self.special_char_pattern.sub(' ', text)
        text = text.lower()
        text = text.split()
        # Remove stop words and lemmatise
        text = [self.lemmatiser.lemmatize(word) for word in text if word not in self.stopwords_set]
        text = ' '.join(text)
        
        if extract_urls:
            return text, urls
        return text

    def preprocess(self, data):
        """
        Apply text preprocessing to a DataFrame column 'text'.
        """
        if 'text' not in data.columns:
            raise ValueError("DataFrame must contain a 'text' column")
        data['processed_text'] = data['text'].apply(self.preprocess_text)
        return data
