from flask import Blueprint, request, jsonify
import numpy as np
import random
import uuid
from pprint import pprint

api = Blueprint('api', __name__)

def create_api_blueprint(vector_store):
    @api.route('/hello', methods=['GET'])
    def hello_world():
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
            # Get the JSON data from the request
            data = request.json

            # Validate the input data
            if not data or not isinstance(data, list):
                return jsonify({'error': 'Invalid data format. Expected a JSON array of numbers.'}), 400
            
            # Ensure all elements in the list are numbers (integers or floats)
            if not all(isinstance(item, (int, float)) for item in data):
                return jsonify({'error': 'All elements in the input data must be numbers.'}), 400
            
            # Generate a new UUID
            vector_id = uuid.uuid4()

            # Assuming vector_store is an object with an add_vector_data method
            # and the method requires an ID and vector data.
            vector_store.add_vector_data(vector_id, data)

            # Return success response with the new UUID
            return jsonify({'uuid': str(vector_id)}), 201

        except Exception as e:
            # Handle any other unexpected errors
            return jsonify({'uuid': str(vector_id)}), 201


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
