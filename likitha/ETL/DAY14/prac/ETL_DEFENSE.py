record = {
    "product_id": 101,
    "price": "500",
    "quantity": "2"
}


price = float(record["price"])
quantity = int(record["quantity"])

total = price * quantity

insert_into_database(
    record["product_id"],
    price,
    quantity,
    total
)