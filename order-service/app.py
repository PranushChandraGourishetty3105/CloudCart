
from flask import Flask, jsonify, request
from urllib.request import urlopen
from urllib.error import URLError, HTTPError
import json
import os
import uuid

app = Flask(__name__)

PRODUCT_SERVICE_URL = os.getenv(
    "PRODUCT_SERVICE_URL",
    "http://127.0.0.1:5001"
)

orders = []


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "service": "CloudCart Order Service",
        "status": "running"
    })


@app.route("/orders", methods=["GET"])
def get_orders():
    return jsonify(orders)


@app.route("/orders", methods=["POST"])
def create_order():
    data = request.get_json(silent=True) or {}

    product_id = data.get("product_id")
    quantity = data.get("quantity")

    if (
        isinstance(product_id, bool)
        or not isinstance(product_id, int)
        or product_id < 1
    ):
        return jsonify({
            "error": "product_id must be a positive integer"
        }), 400

    if (
        isinstance(quantity, bool)
        or not isinstance(quantity, int)
        or quantity < 1
    ):
        return jsonify({
            "error": "quantity must be a positive integer"
        }), 400

    try:
        url = f"{PRODUCT_SERVICE_URL}/products/{product_id}"

        with urlopen(url, timeout=3) as response:
            product = json.loads(response.read().decode("utf-8"))

    except HTTPError as error:
        if error.code == 404:
            return jsonify({"error": "Product not found"}), 404

        return jsonify({"error": "Product Service request failed"}), 502

    except (URLError, TimeoutError):
        return jsonify({"error": "Product Service unavailable"}), 503

    order = {
        "order_id": str(uuid.uuid4()),
        "product_id": product["id"],
        "product_name": product["name"],
        "quantity": quantity,
        "unit_price": product["price"],
        "total_price": product["price"] * quantity
    }

    orders.append(order)

    return jsonify(order), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=False)
