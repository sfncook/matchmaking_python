import faiss
import numpy as np
import pickle
import os
import json
from pprint import pprint
from .vector_store import VectorStore
from typing import List

VECTOR_DB_FILE = 'vector_db_003.pkl'
METADATA_DB_FILE = 'metadata_db_003.json'

class FlatFileVectorStore(VectorStore):
    def __init__(self, dimensions):
        self.dimensions = dimensions
        self.vector_db_file = VECTOR_DB_FILE
        self.metadata_db_file = METADATA_DB_FILE
        self.index = faiss.IndexFlatL2(self.dimensions)
        self.metadatas = []

    def initialize(self):
        # Load metadata from the metadata database file
        if os.path.exists(self.metadata_db_file):
            with open(self.metadata_db_file, 'r') as f:
                metadata_entries = json.load(f)
                print("Loaded metadata:")
                pprint(metadata_entries)

                # Load vectors from the vector database file
                if os.path.exists(self.vector_db_file):
                    with open(self.vector_db_file, 'rb') as f:
                        all_vectors = pickle.load(f)

                        # Convert NumPy array to a simple 2D list
                        if isinstance(all_vectors, np.ndarray):
                            all_vectors = all_vectors.tolist()

                        print("Loaded vectors:")
                        pprint(all_vectors)

                        # Add each vector to the index using UUIDs from metadata
                        for entry in metadata_entries:
                            uuid = entry["uuid"]
                            faiss_index = entry["faiss_index"]
                            vector = all_vectors[faiss_index]  # Retrieve the vector using the FAISS index
                            self.add_vector_data(uuid, vector, False)
        else:
            print("Metadata file does not exist.")

    def add_vector_data(self, uuid: str, vector: List[float], save_to_files: bool = True):
        vector_np = np.array(vector, dtype='float32').reshape(1, -1)
        current_count = self.index.ntotal
        self.index.add(vector_np)
        new_faiss_index = current_count  # The index of the newly added vector

        # Append metadata without resetting the list
        self.metadatas.append({
            "uuid": uuid,
            "faiss_index": new_faiss_index
        })

        if save_to_files:
            # Save vector data and metadata to flat files
            with open(self.vector_db_file, 'wb') as f:
                # Save all vectors from the index
                all_vectors = self.index.reconstruct_n(0, self.index.ntotal)
                pickle.dump(all_vectors, f)
                
            with open(self.metadata_db_file, 'w') as f:
                # Save metadata
                json.dump(self.metadatas, f, indent=4)
    
    def search_nearest(self, vector, limit):
        vector_np = np.array(vector, dtype='float32').reshape(1, -1)
        distances, indices = self.index.search(vector_np, limit)
        distances = distances.flatten()
        indices = indices.flatten()
        uuids = [md["uuid"] for md in self.metadatas if md["faiss_index"] in indices]
        return distances, indices, uuids
    
    def count(self):
        return self.index.ntotal

    def clear(self):
        self.index = faiss.IndexFlatL2(self.dimensions)
        self.metadatas = []


