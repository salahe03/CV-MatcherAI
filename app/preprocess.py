"""
Text preprocessing module
"""

import re
import string
from typing import List


# Common stopwords
STOPWORDS = {
    'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from', 'has', 'he',
    'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the', 'to', 'was', 'will', 'with',
    'the', 'this', 'but', 'they', 'have', 'had', 'what', 'when', 'where', 'who',
    'which', 'why', 'how', 'all', 'each', 'every', 'both', 'few', 'more', 'most',
    'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so',
    'than', 'too', 'very', 'can', 'will', 'just', 'should', 'now'
}


def clean_text(text: str) -> str:
    """
    Clean and normalize text.
    
    Args:
        text: Input text
        
    Returns:
        Cleaned text
    """
    # Convert to lowercase
    text = text.lower()
    
    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    
    # Remove email addresses
    text = re.sub(r'\S+@\S+', '', text)
    
    # Remove special characters but keep spaces and alphanumeric
    text = re.sub(r'[^\w\s+#.-]', ' ', text)
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    return text


def remove_stopwords(text: str) -> str:
    """
    Remove common stopwords from text.
    
    Args:
        text: Input text
        
    Returns:
        Text with stopwords removed
    """
    words = text.split()
    filtered_words = [word for word in words if word.lower() not in STOPWORDS]
    return ' '.join(filtered_words)


def tokenize(text: str) -> List[str]:
    """
    Tokenize text into words.
    
    Args:
        text: Input text
        
    Returns:
        List of tokens
    """
    # Split on whitespace and filter empty strings
    tokens = [token.strip() for token in text.split() if token.strip()]
    return tokens


def preprocess_text(text: str, remove_stops: bool = True) -> str:
    """
    Complete preprocessing pipeline.
    
    Args:
        text: Raw input text
        remove_stops: Whether to remove stopwords
        
    Returns:
        Preprocessed text
    """
    # Clean text
    text = clean_text(text)
    
    # Optionally remove stopwords
    if remove_stops:
        text = remove_stopwords(text)
    
    return text


def preprocess_for_embedding(text: str) -> str:
    """
    Preprocess text specifically for embedding generation.
    Keep more context for better embeddings.
    
    Args:
        text: Raw input text
        
    Returns:
        Preprocessed text suitable for embeddings
    """
    # Light cleaning - keep most words for context
    text = clean_text(text)
    
    # Don't remove stopwords for embeddings (they provide context)
    return text
