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
        print("init")

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
        print(self.metadatas)

        # if save_to_files:
        #     try:
        #         # Save vector data and metadata to flat files
        #         with open(self.vector_db_file, 'wb') as f:
        #             # Save all vectors from the index
        #             all_vectors = self.index.reconstruct_n(0, self.index.ntotal)
        #             pickle.dump(all_vectors, f)
        #             print("Vector data saved successfully.")

        #         with open(self.metadata_db_file, 'w') as f:
        #             # Print the metadata for debugging
        #             print("Metadata to be saved:", self.metadatas)
        #             # Save metadata
        #             json.dump(self.metadatas, f, indent=4)
        #             print("Metadata saved successfully.")
                    
        #     except Exception as e:
        #         print(f"An error occurred while saving files: {e}")
    
    def search_nearest(self, vector, limit):
        vector_np = np.array(vector, dtype='float32').reshape(1, -1)
        distances, indices = self.index.search(vector_np, limit)
        distances = distances.flatten()
        indices = indices.flatten()
        uuids = [md["uuid"] for md in self.metadatas if md["faiss_index"] in indices]
        return distances, indices, uuids

    def get_all_uuids(self):
        return [md["uuid"] for md in self.metadatas]

    def get_vector_for_uuid(self, uuid: str):
        metadata_entry = next((md for md in self.metadatas if md["uuid"] == uuid), None)
        if metadata_entry is None:
            raise ValueError(f"No metadata found for uuid: {uuid}")
        faiss_index = metadata_entry["faiss_index"]
        try:
            vector = self.index.reconstruct(faiss_index)
        except Exception as e:
            raise RuntimeError(f"Failed to reconstruct vector for faiss_index {faiss_index}: {e}")
        return faiss_index, vector.tolist()

    
    def count(self):
        return self.index.ntotal

    def clear(self):
        self.index = faiss.IndexFlatL2(self.dimensions)
        self.metadatas = []


