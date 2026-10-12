
from flask import Flask, jsonify, request
import uuid

app = Flask(__name__)

payments = []

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "service": "CloudCart Payment Service",
        "status": "running"
    })

@app.route("/payments", methods=["POST"])
def create_payment():
    data = request.get_json(silent=True) or {}

    order_id = data.get("order_id")
    amount = data.get("amount")

    if not isinstance(order_id, str) or not order_id.strip():
        return jsonify({"error": "Valid order_id is required"}), 400

    if (
        isinstance(amount, bool)
        or not isinstance(amount, (int, float))
        or amount <= 0
    ):
        return jsonify({"error": "Amount must be positive"}), 400

    payment = {
        "payment_id": str(uuid.uuid4()),
        "order_id": order_id,
        "amount": amount,
        "status": "SUCCESS",
        "message": "Simulated payment completed"
    }

    payments.append(payment)
    return jsonify(payment), 201

@app.route("/payments", methods=["GET"])
def get_payments():
    return jsonify(payments)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003, debug=False)
