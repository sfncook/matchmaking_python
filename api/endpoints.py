from flask import Blueprint, request, jsonify
import numpy as np
import random
import uuid
from pprint import pprint
import pickle
import json
import os

api = Blueprint('api', __name__)

def create_api_blueprint(vector_store):
    def get_all_data():
        all_uuids = vector_store.get_all_uuids()
        all_vector_data = []

        for uuid in all_uuids:
            vector = vector_store.get_vector_for_uuid(uuid)
            faiss_index = next(md["faiss_index"] for md in vector_store.metadatas if md["uuid"] == uuid)
            all_vector_data.append({
                "vector": vector,
                "faiss_index": faiss_index,
                "uuid": uuid
            })

        # Sort by faiss_index
        all_vector_data.sort(key=lambda x: x["faiss_index"])

        # Extract vectors and metadata
        all_vectors = [v["vector"] for v in all_vector_data]
        all_metadata = [{"faiss_index": v["faiss_index"], "uuid": v["uuid"]} for v in all_vector_data]

        return all_vectors, all_metadata

    @api.route('/hello', methods=['GET'])
    def hello_world():
        all_vectors, all_metadata = get_all_data()
        return "hello", 200


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

                        # Rebuild the FAISS index and metadata
                        for entry in metadata_entries:
                            uuid = entry["uuid"]
                            faiss_index = entry["faiss_index"]

                            # Retrieve the correct vector using the faiss_index
                            vector_tuple = next((v for v in all_vectors if v[0] == faiss_index), None)
                            if vector_tuple:
                                _, vector = vector_tuple
                                print(f"FOUND vector for faiss_index:{faiss_index} vector:{vector}")
                                vector_store.add_vector_data(uuid, vector)
                            else:
                                print(f"MISSING vector for faiss_index: {faiss_index}")

                        return jsonify({
                            "metadata_entries": metadata_entries,
                            "all_vectors": all_vectors
                        }), 200
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

        # 

    #     vector = data['vector']
    #     unique_id = data['id']
    #     if len(vector) != 12:
    #         return jsonify({'error': 'Vector must be 12-dimensional'}), 400

    #     if unique_id in metadata_store.id_to_index:
    #         return jsonify({'error': 'ID must be unique'}), 400

    #     vector_np = np.array(vector, dtype='float32').reshape(1, -1)  # Convert to NumPy array and reshape
    #     faiss_manager.index.add(vector_np)  # Add vector to FAISS index

    #     # Add metadata
    #     metadata = data.get('metadata', {})
    #     metadata['id'] = unique_id
    #     metadata_store.add_metadata(unique_id, metadata)

    #     print("Added vector and metadata:")
    #     pprint(vector_np)
    #     pprint(metadata_store.metadata_db)

    #     return jsonify({'message': 'Vector and metadata added successfully', 'total_vectors': faiss_manager.index.ntotal}), 201

    # @api.route('/point/nearest', methods=['POST'])
    # def nearest_point():
    #     data = request.json
    #     if not data or 'point' not in data or 'limit' not in data:
    #         return jsonify({'error': 'Invalid input'}), 400

    #     point = data['point']
    #     limit = data['limit']

    #     if limit <= 0:
    #         return jsonify({'error': 'Limit must be a positive integer'}), 400

    #     if len(point) != 12:
    #         return jsonify({'error': 'Point must be 12-dimensional'}), 400

    #     point_np = np.array(point, dtype='float32').reshape(1, -1)  # Convert to NumPy array and reshape
    #     distances, indices = faiss_manager.index.search(point_np, limit)  # Perform nearest-neighbor search

    #     nearest_points = [
    #         {
    #             'index': int(idx),
    #             'distance': float(dist),
    #             'metadata': metadata_store.metadata_db[int(idx)],
    #             'coordinates': faiss_manager.index.reconstruct(int(idx)).tolist()
    #         }
    #         for dist, idx in zip(distances[0], indices[0])
    #     ]

    #     return jsonify({'nearest_points': nearest_points}), 200

    return api
