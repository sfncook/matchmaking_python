import json
import os
from pprint import pprint
from .metadata_store import MetadataStore

class FlatFileMetadataStore(MetadataStore):
    def __init__(self, matadata_db_file):
        self.matadata_db_file
        self.metadatas = []

    def initialize(self):
        if os.path.exists(self.matadata_db_file):
            with open(self.matadata_db_file, 'r') as f:
                self.metadatas = json.load(f)
                print("Loaded metadata:")
                pprint(metadatas)
        

    def add_metadata(self, unique_id, metadata):
        self.metadata_db.append(metadata)

    def get_metadata(self, index):
        """Get metadata by FAISS index."""
        if index < 0 or index >= len(self.metadata_db):
            raise IndexError("Index out of bounds.")
        return self.metadata_db[index]

    def get_all_metadata(self):
        """Get all metadata."""
        return self.metadata_db

    def save_metadata(self):
        """Save metadata and ID mapping to a JSON file."""
        data = {
            'metadata_db': self.metadata_db,
            'id_to_index': self.id_to_index
        }
        with open(self.matadata_db_file, 'w') as f:
            json.dump(data, f, indent=4)

    def load_metadata(self):
        """Load metadata and ID mapping from a JSON file."""
        if os.path.exists(self.matadata_db_file):
            with open(self.matadata_db_file, 'r') as f:
                data = json.load(f)
                self.metadata_db = data['metadata_db']
                self.id_to_index = data['id_to_index']
                print("Loaded metadata:")
                pprint(self.metadata_db)
                pprint(self.id_to_index)
        else:
            print(f"Metadata file '{self.matadata_db_file}' not found. Starting with an empty metadata store.")

    def clear(self):
        """Clear all metadata."""
        self.metadata_db = []
        self.id_to_index = {}
        # if os.path.exists(self.matadata_db_file):
        #     os.remove(self.matadata_db_file)
        # print("Index cleared and vector database file deleted.")

    def __repr__(self):
        return f"MetadataStore(metadata_db={self.metadata_db}, id_to_index={self.id_to_index})"
