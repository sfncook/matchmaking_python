from flask import Flask, request, jsonify
import faiss
import numpy as np

app = Flask(__name__)

# Initialize FAISS index for 12-dimensional vectors
d = 12  # dimension
index = faiss.IndexFlatL2(d)  # L2 distance index

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

if __name__ == '__main__':
    app.run(debug=True)
