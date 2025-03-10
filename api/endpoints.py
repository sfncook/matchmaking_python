from flask import Blueprint, request, jsonify
import uuid
from pprint import pprint

api = Blueprint('api', __name__)

def create_api_blueprint(vector_store, review_events_store):

    @api.route('/hello', methods=['GET'])
    def hello_world():
        return jsonify({
            "consumers": vector_store.get_all_consumers(),
            "products": vector_store.get_all_products(),
        }), 200

    @api.route('/consumers', methods=['POST'])
    def add_random_consumer():
        """
        Add a new consumer with a randomly generated UUID.

        This endpoint creates a new consumer by generating a random UUID and 
        storing the consumer's information in the vector store. The UUID is 
        returned in the response as confirmation of successful creation.

        Endpoint:
            POST /consumers

        Response:
            JSON: A dictionary with the key 'uuid' containing the generated UUID.
            Status Code: 201 (Created)

        Example Response:
            {
                "uuid": "123e4567-e89b-12d3-a456-426614174000"
            }

        Returns:
            flask.Response: A JSON response with the UUID of the newly created consumer.
        """
        consumer_uuid = str(uuid.uuid4())
        vector_store.add_new_consumer_random(consumer_uuid)
        return jsonify({"uuid":consumer_uuid}), 201

    @api.route('/consumers', methods=['GET'])
    def get_all_consumers():
        return jsonify({"consumers":vector_store.get_all_consumers()}), 200

    @api.route('/products', methods=['POST'])
    def add_random_product():
        product_uuid = str(uuid.uuid4())
        vector_store.add_new_product_random(product_uuid)
        return jsonify({"uuid":product_uuid}), 201

    @api.route('/products', methods=['GET'])
    def get_all_products():
        return jsonify({"products":vector_store.get_all_products()}), 200

    @api.route('/products/<string:product_uuid>', methods=['GET'])
    def get_single_product(product_uuid):
        product = vector_store.get_product_by_uuid(product_uuid)
        if product is None:
            return jsonify({'error': 'Product not found'}), 404
        return jsonify(product), 200

    @api.route('/consumers/<string:consumer_uuid>', methods=['GET'])
    def get_single_consumer(consumer_uuid):
        product = vector_store.get_consumer_by_uuid(consumer_uuid)
        if product is None:
            return jsonify({'error': 'Consumer not found'}), 404
        return jsonify(product), 200

    @api.route('/recommendations', methods=['GET'])
    def get_recommendations():
        # Get query parameters
        consumer_uuid = request.args.get('consumer_uuid')
        limit = int(request.args.get('limit', 10))
        nearest_product_uuids = vector_store.find_nearest_products(consumer_uuid, limit)
        predictions = vector_store.get_predictions(consumer_uuid, nearest_product_uuids)
        return jsonify({"recommendations": predictions}), 200

    @api.route('/distances/between_consumer_and_product', methods=['GET'])
    def get_distance_between():
        consumer_uuid = request.args.get('consumer_uuid')
        product_uuid = request.args.get('product_uuid')
        distance = vector_store.get_distance_between(consumer_uuid, product_uuid)
        return jsonify({"distance":distance}), 200

    @api.route('/distances/max', methods=['GET'])
    def get_max_distance():
        distance = vector_store.get_max_distance()
        return jsonify({"max_distance":distance}), 200

    @api.route('/distances/to_all_products', methods=['GET'])
    def get_all_distances():
        consumer_uuid = request.args.get('consumer_uuid')
        distance = vector_store.get_all_distances(consumer_uuid)
        return jsonify({"distance":distance}), 200


    @api.route('/reviews', methods=['POST'])
    def add_review():
        data = request.json
        review_quantitative = data['review_quantitative']
        consumer_uuid = data['consumer_uuid']
        product_uuid = data['product_uuid']
        consumer_reviews_count = review_events_store.get_count_review_events_for_consumer(consumer_uuid)
        product_reviews_count = review_events_store.get_count_review_events_for_product(product_uuid)
        new_review_event_uuid = str(uuid.uuid4())
        review_events_store.add_new_review_event(
            new_review_event_uuid, 
            consumer_uuid, 
            product_uuid,
            review_quantitative
        )
        vector_store.add_review(
            consumer_uuid, 
            product_uuid, 
            review_quantitative,
            consumer_reviews_count,
            product_reviews_count
        )
        return "ok", 201

    @api.route('/reviews', methods=['GET'])
    def get_all_review_events():
        return jsonify({"reviews":review_events_store.get_all_review_events()}), 200

    @api.route('/reviews/consumers/<string:consumer_uuid>/count', methods=['GET'])
    def get_reviews_consumer_count(consumer_uuid):
        return jsonify({"count":review_events_store.get_count_review_events_for_consumer(consumer_uuid)}), 200

    @api.route('/reviews/products/<string:product_uuid>/count', methods=['GET'])
    def get_reviews_product_count(product_uuid):
        return jsonify({"count":review_events_store.get_count_review_events_for_product(product_uuid)}), 200

    return api



