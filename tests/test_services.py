
import requests

PRODUCT_URL = "http://127.0.0.1:5001"
ORDER_URL = "http://127.0.0.1:5002"
PAYMENT_URL = "http://127.0.0.1:5003"


def test_product_service_health():
    response = requests.get(f"{PRODUCT_URL}/")
    assert response.status_code == 200
    assert response.json()["status"] == "running"


def test_get_products():
    response = requests.get(f"{PRODUCT_URL}/products")
    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_get_product_by_id():
    response = requests.get(f"{PRODUCT_URL}/products/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Laptop"


def test_order_service_health():
    response = requests.get(f"{ORDER_URL}/")
    assert response.status_code == 200
    assert response.json()["status"] == "running"


def test_create_order():
    response = requests.post(
        f"{ORDER_URL}/orders",
        json={"product_id": 1, "quantity": 2}
    )
    assert response.status_code == 201

    order = response.json()
    assert order["quantity"] == 2
    assert order["total_price"] == 90000



def test_product_service_health():
    response = requests.get(f"{PRODUCT_URL}/")
    assert response.status_code == 200
    assert response.headers["Content-Type"].startswith(
        "application/json"
    )
    assert response.json() is not None

