from flask import Flask, request, jsonify
import faiss
import numpy as np
from flask_cors import CORS
import os
import pickle

app = Flask(__name__)
CORS(app)  # Enable CORS

# Initialize FAISS index for 12-dimensional vectors
d = 12  # dimension
index = faiss.IndexFlatL2(d)  # L2 distance index

# Metadata storage
metadata_db = []
id_to_index = {}

VECTOR_DB_FILE = 'vector_db.pkl'

# Function to save the FAISS index and metadata to a file
def save_db():
    with open(VECTOR_DB_FILE, 'wb') as f:
        pickle.dump((index.reconstruct_n(0, index.ntotal), metadata_db, id_to_index), f)

# Function to load the FAISS index and metadata from a file
def load_db():
    if os.path.exists(VECTOR_DB_FILE):
        with open(VECTOR_DB_FILE, 'rb') as f:
            vectors, metadata, id_index = pickle.load(f)
            index.add(vectors)
            global metadata_db, id_to_index
            metadata_db = metadata
            id_to_index = id_index

# Function to initialize the FAISS index with random vectors and metadata
def initialize_db(num_vectors=10, dimension=12):
    np.random.seed(0)  # For reproducibility
    random_vectors = np.random.rand(num_vectors, dimension).astype('float32') * 100  # Scale values to [0, 100]
    index.add(random_vectors)

    # Adding metadata
    for i in range(num_vectors):
        unique_id = i
        metadata_db.append({'id': unique_id, 'description': f'Random vector {i}'})
        id_to_index[unique_id] = i

    print("Initialized vectors and metadata:")
    print(random_vectors)
    print(metadata_db)

# Load the FAISS index and metadata from file, if available
if __name__ == '__main__' and not os.environ.get('WERKZEUG_RUN_MAIN'):
    load_db()
    if index.ntotal == 0:  # If no data was loaded, initialize with default data
        initialize_db()

@app.route('/hello', methods=['GET'])
def hello_world():
    return 'Hello, World!'

@app.route('/point', methods=['POST'])
def add_point():
    data = request.json
    if not data or 'vector' not in data or 'id' not in data:
        return jsonify({'error': 'Invalid input'}), 400

    vector = data['vector']
    unique_id = data['id']
    if len(vector) != 12:
        return jsonify({'error': 'Vector must be 12-dimensional'}), 400

    if unique_id in id_to_index:
        return jsonify({'error': 'ID must be unique'}), 400

    vector_np = np.array(vector, dtype='float32').reshape(1, -1)  # Convert to NumPy array and reshape
    index.add(vector_np)  # Add vector to FAISS index

    # Add metadata
    metadata = data.get('metadata', {})
    metadata['id'] = unique_id
    metadata_db.append(metadata)
    id_to_index[unique_id] = index.ntotal - 1

    # Save the updated database
    save_db()

    return jsonify({'message': 'Vector and metadata added successfully', 'total_vectors': index.ntotal}), 201

@app.route('/point/nearest', methods=['POST'])
def nearest_point():
    data = request.json
    if not data or 'point' not in data or 'limit' not in data:
        return jsonify({'error': 'Invalid input'}), 400

    point = data['point']
    limit = data['limit']

    if limit <= 0:
        return jsonify({'error': 'Limit must be a positive integer'}), 400

    if len(point) != 12:
        return jsonify({'error': 'Point must be 12-dimensional'}), 400

    point_np = np.array(point, dtype='float32').reshape(1, -1)  # Convert to NumPy array and reshape
    distances, indices = index.search(point_np, limit)  # Perform nearest-neighbor search

    nearest_points = [{'index': int(idx), 'distance': float(dist), 'metadata': metadata_db[int(idx)]} for dist, idx in zip(distances[0], indices[0])]
    return jsonify({'nearest_points': nearest_points}), 200

if __name__ == '__main__':
    app.run(debug=True)
