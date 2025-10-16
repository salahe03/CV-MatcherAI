"""
Embedding generation and similarity matching using DistilBERT
"""

import torch
from transformers import AutoTokenizer, AutoModel
from sklearn.metrics.pairwise import cosine_similarity  
import numpy as np
from typing import Tuple


class EmbeddingModel:
    """
    Wrapper for DistilBERT model to generate embeddings and compute similarity.
    """
    
    def __init__(self, model_name: str = "distilbert-base-uncased"):
        """
        Initialize the model and tokenizer.
        
        Args:
            model_name: Name of the pretrained model to use
        """
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(f"Using device: {self.device}")
        
        # Load tokenizer and model
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)
        self.model.to(self.device)
        self.model.eval()  # Set to evaluation mode
        
    def generate_embedding(self, text: str) -> np.ndarray:
        """
        Generate embedding vector for input text.
        
        Args:
            text: Input text
            
        Returns:
            Embedding vector as numpy array
        """
        # Tokenize and prepare input
        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            max_length=512,
            padding=True
        )
        
        # Move inputs to device
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        
        # Generate embeddings
        with torch.no_grad():
            outputs = self.model(**inputs)
            
        # Use mean pooling of last hidden state
        embeddings = outputs.last_hidden_state.mean(dim=1)
        
        # Convert to numpy and return
        return embeddings.cpu().numpy()
    
    def compute_similarity(self, text1: str, text2: str) -> float:
        """
        Compute cosine similarity between two texts.
        
        Args:
            text1: First text (e.g., CV)
            text2: Second text (e.g., job description)
            
        Returns:
            Similarity score between 0 and 1
        """
        # Generate embeddings
        emb1 = self.generate_embedding(text1)
        emb2 = self.generate_embedding(text2)
        
        # Compute cosine similarity
        similarity = cosine_similarity(emb1, emb2)[0][0]
        
        # Ensure the score is between 0 and 1
        # Cosine similarity ranges from -1 to 1, normalize to 0-1
        normalized_score = (similarity + 1) / 2
        
        return float(normalized_score)
    
    def batch_similarity(self, texts1: list, texts2: list) -> np.ndarray:
        """
        Compute similarity for multiple text pairs.
        
        Args:
            texts1: List of first texts
            texts2: List of second texts
            
        Returns:
            Array of similarity scores
        """
        if len(texts1) != len(texts2):
            raise ValueError("Text lists must have same length")
        
        scores = []
        for t1, t2 in zip(texts1, texts2):
            score = self.compute_similarity(t1, t2)
            scores.append(score)
        
        return np.array(scores)


# Global model instance (initialized once)
_model_instance = None


def get_model() -> EmbeddingModel:
    """
    Get or create the global model instance (singleton pattern).
    
    Returns:
        EmbeddingModel instance
    """
    global _model_instance
    if _model_instance is None:
        _model_instance = EmbeddingModel()
    return _model_instance


def calculate_match_score(cv_text: str, jd_text: str) -> float:
    """
    Calculate match score between CV and job description.
    
    Args:
        cv_text: Preprocessed CV text
        jd_text: Preprocessed job description text
        
    Returns:
        Match score between 0 and 1
    """
    model = get_model()
    return model.compute_similarity(cv_text, jd_text)
