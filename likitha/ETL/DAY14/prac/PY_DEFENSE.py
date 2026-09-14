records = [
    {"product_id": 101, "price": "500"},
    {"product_id": 102},
    {"product_id": 103, "price": None},
    {"product_id": 104, "price": "abc"},
    {"product_id": 105, "price": "-200"},
    {"product_id": 106, "price": "300"}
]

for d in records:
    try:
        product_id = d.get("product_id")
        price = d.get("price")

        if product_id is None:
            raise ValueError("Product ID is missing")

        if price is None:
            raise ValueError("Price is missing")

        try:
            price = float(price)
        except (ValueError, TypeError):
            raise ValueError("Price is not a valid number")

        if price < 0:
            raise ValueError("Price cannot be negative")

        print(f"Product {product_id}: Valid price = {price}")

    except ValueError as e:
        print(f"Product {product_id}: Rejected - {e}")