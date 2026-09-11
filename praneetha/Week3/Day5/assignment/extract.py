# extraction part of our pipeline
# here we are simply extracting our data from the diff sources we had

import pandas as pd


# fxn to extract the data from the files
def extract_data():
    customers = pd.read_csv("data/customers.csv")
    orders = pd.read_csv("data/orders.csv")
    payments = pd.read_json("data/payments.json")

    return customers, orders, payments


# calling the fxn
if __name__ == "__main__":

    customers, orders, payments = extract_data()

    print("Customers:", customers.shape)
    print("Orders:", orders.shape)
    print("Payments:", payments.shape)