
from flask import Flask, jsonify

app = Flask(__name__)

products = [
    {"id": 1, "name": "Laptop", "price": 45000},
    {"id": 2, "name": "Headphones", "price": 1500},
    {"id": 3, "name": "Keyboard", "price": 800}
]


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "service": "CloudCart Product Service",
        "status": "running"
    })


@app.route("/products", methods=["GET"])
def get_products():
    return jsonify(products)


@app.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    for product in products:
        if product["id"] == product_id:
            return jsonify(product)

    return jsonify({"error": "Product not found"}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=False)
