def transform(data):
    print("Starting transformation...")
    data=data.copy()
    data["product_name"]=data["product_name"].str.strip()
    data["category"]=data["category"].str.strip().str.title()
    data["price"]=data["price"].astype(float)
    data=data[data["price"]>0]

    return data