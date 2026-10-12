import pandas as pd
import requests
BASE_URL='https://fakestoreapi.com'

#product data
def extract_product():
    url = f'{BASE_URL}/products'
    response = requests.get(url)
    response.raise_for_status()

    data = response.json()
    product_df= pd.DataFrame(data)

    return product_df


#user data
def extract_user():
    url=f'{BASE_URL}/users'
    response = requests.get(url)
    response.raise_for_status()

    data = response.json()
    user_df=pd.DataFrame(data)
    return user_df