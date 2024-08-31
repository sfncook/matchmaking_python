from abc import ABC, abstractmethod

class MetadataStore(ABC):
    @abstractmethod
    def initialize(self):
        """Initialize the data store."""
        pass

    @abstractmethod
    def add_metadata(self, unique_id, metadata):
        """Add metadata and map the unique ID to the FAISS index."""
        pass

    @abstractmethod
    def get_metadata(self, index):
        """Get metadata by FAISS index."""
        pass

    @abstractmethod
    def get_all_metadata(self):
        """Get all metadata."""
        pass

    @abstractmethod
    def save_metadata(self, filepath):
        """Save metadata and ID mapping to a JSON file."""
        pass

    @abstractmethod
    def clear(self):
        """Clear all metadata."""
        pass
