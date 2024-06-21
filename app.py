from flask import Flask, request, jsonify
import faiss
import numpy as np

app = Flask(__name__)

# Initialize FAISS index for 12-dimensional vectors
d = 12  # dimension
index = faiss.IndexFlatL2(d)  # L2 distance index

# Function to initialize the FAISS index with random vectors
def initialize_db(num_vectors=10, dimension=12):
    np.random.seed(0)  # For reproducibility
    random_vectors = np.random.rand(num_vectors, dimension).astype('float32') * 100
    index.add(random_vectors)
    print("Initialized vectors:")
    print(random_vectors)

# Initialize the FAISS index with 10 random vectors
initialize_db()

@app.route('/hello', methods=['GET'])
def hello_world():
    return 'Hello, World!'

@app.route('/point', methods=['POST'])
def add_point():
    data = request.json
    if not data or 'vector' not in data:
        return jsonify({'error': 'Invalid input'}), 400

    vector = data['vector']
    if len(vector) != 12:
        return jsonify({'error': 'Vector must be 12-dimensional'}), 400

    vector_np = np.array(vector, dtype='float32').reshape(1, -1)  # Convert to NumPy array and reshape
    index.add(vector_np)  # Add vector to FAISS index

    return jsonify({'message': 'Vector added successfully', 'total_vectors': index.ntotal}), 201

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

    nearest_points = [{'index': int(idx), 'distance': float(dist)} for dist, idx in zip(distances[0], indices[0])]
    return jsonify({'nearest_points': nearest_points}), 200

if __name__ == '__main__':
    app.run(debug=True)
