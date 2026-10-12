record = {
    "product_id": 101,
    "price": "500",
    "quantity": "2"
}
try:
    if record.get("product_id") is None:
        raise ValueError("No product_id value")
    if record.get("price") is None:
        raise ValueError("No price value")
    if record.get("quantity") is None:
        raise ValueError("No quantity value")
    try:
        price = float(record["price"])
        quantity = int(record["quantity"])
    except ValueError as e:
        print(e)

    if price < 0:
        raise ValueError("Price cannot be negative")

    if quantity <= 0:
        raise ValueError("Quantity must be greater than 0")
    total = price * quantity
except ValueError as e:
    print(e)

try:
    insert_into_database(
    record["product_id"],
    price,
    quantity,
    total
    )
except ConnectionError as e:
    print(e)