from flask import Flask
from flask_cors import CORS
import os
from api.endpoints import create_api_blueprint
from storage.flatfile_cartesian_vector_store import FlatFile_LatLonSpherical_VectorStore
from storage.review_events_store import Review_Events_Store

app = Flask(__name__)
CORS(app)

vector_store = FlatFile_LatLonSpherical_VectorStore()
review_events_store = Review_Events_Store()

app.register_blueprint(create_api_blueprint(vector_store, review_events_store))

@app.before_first_request
def initialize_app():
    vector_store.initialize()
    review_events_store.initialize()

if __name__ == '__main__':
    app.run(debug=True)  # Keep debug=True for development; consider setting to False in production
