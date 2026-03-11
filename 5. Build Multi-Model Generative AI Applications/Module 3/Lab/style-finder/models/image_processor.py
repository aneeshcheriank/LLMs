# models/image_processor.py
"""
Module for image processing, encoding, and similarity matching.
This module handles the conversion of images to vectors and finding
similar images in the dataset.
"""

import torch
import torchvision.transforms as transforms
from torchvision.models import resnet50
from PIL import Image
import requests
import base64
from io import BytesIO
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class ImageProcessor:
    """
    Handles image processing, encoding, and similarity comparisons.
    """
    
    def __init__(self, image_size=(224, 224), 
                 norm_mean=[0.485, 0.456, 0.406], 
                 norm_std=[0.229, 0.224, 0.225]):
        """
        Initialize the image processor with a pre-trained ResNet50 model.
        
        Args:
            image_size (tuple): Target size for input images
            norm_mean (list): Normalization mean values for RGB channels
            norm_std (list): Normalization standard deviation values for RGB channels
        """
        # TODO: Initialize the device (CPU or GPU)
        # Hint: Use torch.device to determine if CUDA is available
        self.device = None  # YOUR CODE HERE
        
        # TODO: Load the pre-trained ResNet50 model and set it to evaluation mode
        # Hint: Use resnet50(pretrained=True) and move it to the device
        self.model = None  # YOUR CODE HERE
        
        # TODO: Create the preprocessing pipeline using transforms.Compose
        # The pipeline should resize, convert to tensor, and normalize the image
        self.preprocess = None  # YOUR CODE HERE
    
    def encode_image(self, image_input, is_url=True):
        """
        Encode an image and extract its feature vector.
        
        Args:
            image_input: URL or local path to the image
            is_url: Whether the input is a URL (True) or a local file path (False)
            
        Returns:
            dict: Contains 'base64' string and 'vector' (feature embedding)
        """
        try:
            # TODO: Load the image based on the input type (URL or file path)
            # Hint: Use requests.get for URLs and Image.open for file paths
            # Don't forget to convert to RGB format
            image = None  # YOUR CODE HERE
            
            # TODO: Convert image to Base64
            # Hint: Use BytesIO and base64.b64encode
            base64_string = None  # YOUR CODE HERE
            
            # TODO: Preprocess the image for ResNet50
            # Hint: Use the preprocess pipeline and add a batch dimension with unsqueeze(0)
            input_tensor = None  # YOUR CODE HERE
            
            # TODO: Extract features using ResNet50 and convert to numpy array
            # Hint: Use torch.no_grad() to disable gradient calculation
            feature_vector = None  # YOUR CODE HERE
            
            return {"base64": base64_string, "vector": feature_vector}
        except Exception as e:
            print(f"Error encoding image: {e}")
            return {"base64": None, "vector": None}

    def find_closest_match(self, user_vector, dataset):
        """
        Find the closest match in the dataset based on cosine similarity.
        
        Args:
            user_vector: Feature vector of the user-uploaded image
            dataset: DataFrame containing precomputed feature vectors
            
        Returns:
            tuple: (Closest matching row, similarity score)
        """
        try:
            # TODO: Extract all embedding vectors from the dataset
            # Hint: Use np.vstack on the 'Embedding' column
            dataset_vectors = None  # YOUR CODE HERE
            
            # TODO: Calculate cosine similarity between user vector and all dataset vectors
            # Hint: Use cosine_similarity from sklearn and reshape user_vector to (1, -1)
            similarities = None  # YOUR CODE HERE
            
            # TODO: Find the index of the most similar vector and its similarity score
            # Hint: Use np.argmax to find the index with the highest similarity
            closest_index = None  # YOUR CODE HERE
            similarity_score = None  # YOUR CODE HERE
            
            # Retrieve the closest matching row
            closest_row = dataset.iloc[closest_index]
            return closest_row, similarity_score
        except Exception as e:
            print(f"Error finding closest match: {e}")
            return None, None