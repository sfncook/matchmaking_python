from flask import Blueprint, request, jsonify
import numpy as np
import random
import uuid
from pprint import pprint
import pickle
import json
import os

api = Blueprint('api', __name__)

def create_api_blueprint(vector_store, consumer_store):
    def get_all_data():
        all_uuids = vector_store.get_all_uuids()
        pprint(all_uuids)
        all_vector_data = []

        for uuid in all_uuids:
            vector = vector_store.get_vector_for_uuid(uuid)
            pprint(vector)
            faiss_index = next(md["faiss_index"] for md in vector_store.metadatas if md["uuid"] == uuid)
            all_vector_data.append({
                "vector": vector,
                "faiss_index": faiss_index,
                "uuid": uuid
            })
        pprint(all_vector_data)

        # Sort by faiss_index
        all_vector_data.sort(key=lambda x: x["faiss_index"])

        # Return the zipped data as a list of objects
        return jsonify(all_vector_data)

    @api.route('/hello', methods=['GET'])
    def hello_world():
        return get_all_data(), 200

    @api.route('/consumers/random', methods=['POST'])
    def add_random_consumer():
        consumer_uuid = str(uuid.uuid4())
        consumer_store.add_new_consumer_random(consumer_uuid)
        return consumer_uuid, 201

    @api.route('/vectors/random', methods=['GET'])
    def points_random():
        try:
            # Get query parameters
            dimensions = int(request.args.get('dimensions', 10))  # Default to 10 if not provided
            min_value = float(request.args.get('min_value', 0.0))  # Default to 0.0 if not provided
            max_value = float(request.args.get('max_value', 1.0))  # Default to 1.0 if not provided

            # Validate min_value and max_value
            if min_value > max_value:
                return jsonify({'error': 'min_value cannot be greater than max_value'}), 400

            # Generate random list of float values
            random_floats = [random.uniform(min_value, max_value) for _ in range(dimensions)]

            return jsonify(random_floats)
        except ValueError as e:
            return jsonify({'error': str(e)}), 400

    @api.route('/vectors', methods=['POST'])
    def add_new_vector():
        try:
            data = request.json
            if not data or not isinstance(data, list):
                return jsonify({'error': 'Invalid data format. Expected a JSON array of numbers.'}), 400
            # Ensure all elements in the list are numbers (integers or floats)
            if not all(isinstance(item, (int, float)) for item in data):
                return jsonify({'error': 'All elements in the input data must be numbers.'}), 400
            vector_id = str(uuid.uuid4())
            vector_store.add_vector_data(vector_id, data)
            return jsonify({'uuid': str(vector_id)}), 201
        except Exception as e:
            # Handle any other unexpected errors
            return jsonify({'uuid': vector_id}), 201

    @api.route('/vectors/load_from_file', methods=['POST'])
    def load_from_file():
        data = request.json
        if not data or 'metadata_db_file' not in data or 'vector_db_file' not in data:
            return jsonify({'error': 'Invalid input'}), 400

        metadata_db_file = data['metadata_db_file']
        vector_db_file = data['vector_db_file']

        metadata_db_file_with_dir = os.path.join("data", metadata_db_file)
        vector_db_file_with_dir = os.path.join("data", vector_db_file)

        # Load metadata from the metadata database file
        if os.path.exists(metadata_db_file_with_dir):
            with open(metadata_db_file_with_dir, 'r') as f:
                metadata_entries = json.load(f)

                # Load vectors from the vector database file
                if os.path.exists(vector_db_file_with_dir):
                    with open(vector_db_file_with_dir, 'rb') as f:
                        all_vectors = pickle.load(f)
                        pprint(all_vectors)

                        vector_store.clear()

                        many_vectors_loaded = 0

                        # Rebuild the FAISS index and metadata
                        for entry in metadata_entries:
                            uuid = entry["uuid"]
                            faiss_index = entry["faiss_index"]

                            # Retrieve the correct vector using the faiss_index
                            vector_tuple = next((v for v in all_vectors if v[0] == faiss_index), None)
                            if vector_tuple:
                                _, vector = vector_tuple
                                vector_store.add_vector_data(uuid, vector)
                                many_vectors_loaded += 1
                            else:
                                print(f"MISSING vector for faiss_index: {faiss_index}")

                        return jsonify({"many_vectors_loaded":many_vectors_loaded}), 200
                else:
                    return jsonify({'error': 'Vector file does not exist.'}), 400
        else:
            return jsonify({'error': 'Metadata file does not exist.'}), 400

    @api.route('/vectors/save_to_file', methods=['POST'])
    def save_to_file():
        data = request.json
        if not data or 'metadata_db_file' not in data or 'vector_db_file' not in data:
            return jsonify({'error': 'Invalid input'}), 400

        metadata_db_file = data['metadata_db_file']
        vector_db_file = data['vector_db_file']

        metadata_db_file_with_dir = os.path.join("data", metadata_db_file)
        vector_db_file_with_dir = os.path.join("data", vector_db_file)

        try:
            all_vectors, all_metadata = get_all_data()
            # Save vector data and metadata to flat files
            with open(vector_db_file_with_dir, 'wb') as f:
                pickle.dump(all_vectors, f)
                print("Vector data saved successfully.")

            with open(metadata_db_file_with_dir, 'w') as f:
                print("Metadata to be saved:", all_metadata)
                json.dump(all_metadata, f, indent=4)
                print("Metadata saved successfully.")
        
        except Exception as e:
            print(f"An error occurred while saving files: {e}")
            return jsonify({'error': str(e)}), 500

        return jsonify({'message': 'Files saved successfully'}), 200

    return api
