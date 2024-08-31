import numpy as np
import pickle
import os
from .vector_data import VectorData

class DataInitializer:
    def __init__(self, vector_store, metadata_store):
        self.vector_store = vector_store
        self.metadata_store = metadata_store

    # Function to initialize the FAISS index with random vectors and metadata
    def randomize_and_store_new_vectors(many_vectors):        
        np.random.seed(0)
        random_vectors = (np.random.rand(many_vectors, self.vector_store.dimensions).astype('float32') * 20) - 10  # Scale values to [-10, 10]

        for i in range(many_vectors):
            unique_id = i
            vector_data = VectorData(unique_id, random_vectors[i], {'id': unique_id, 'description': f'Random vector {i}'})
            self.vector_store.add_vector(vector_data)
            pprint(vector_data)

    def initialize(self, num_vectors=10, dimension=12):
        print("**************************")
        print("**************************")
        print("**************************")
        """Initialize the FAISS index and metadata, loading from disk if available."""
        if self.vector_store.vector_count() == 0:  # If no data was loaded, initialize with default data
            print("Vector db empty, randomizing new vectors for testing:")
            randomize_and_store_new_vectors(10)
        print("**************************")
        print("**************************")
        print("**************************")
        pprint(metadata_db)

    def clear_data(self):
        """Clear the FAISS index and metadata."""
        self.persistence_manager.clear_db(self.faiss_manager.index, self.metadata_store)
