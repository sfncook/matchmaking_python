from flask import Blueprint, request, jsonify
import numpy as np
from pprint import pprint

api = Blueprint('api', __name__)

def create_api_blueprint(vector_store):
    @api.route('/hello', methods=['GET'])
    def hello_world():
        
        return "hello", 200

    # @api.route('/point', methods=['POST'])
    # def add_point():
    #     data = request.json
    #     if not data or 'vector' not in data or 'id' not in data:
    #         return jsonify({'error': 'Invalid input'}), 400

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
