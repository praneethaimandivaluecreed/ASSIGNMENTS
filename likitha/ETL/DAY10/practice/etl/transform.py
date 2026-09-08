import pandas as pd

def transform_product(product_df):
    df = product_df.copy()

    df = df.rename(columns={
        'id':'product_id',
        'title':'product_name',
        'price':'product_price',
        'category':'product_category',
        'description': 'description'
    })


    df=df[[
        'product_id' , 'product_name' , 'product_price' , 'product_category' , 'description'
    ]]

    df['product_price'] = df['product_price'].astype(float)

    return df

def transform_user(user_df):
    df=user_df.copy()

    name_df = pd.json_normalize(df['name'])

    df['first_name'] = name_df['firstname']
    df['last_name'] = name_df['lastname']
    
    df['street']=df['address'].apply(lambda x: x['street'])
    df['city']=df['address'].apply(lambda x: x['city'])
    df['zipcode']=df['address'].apply(lambda x : x['zipcode'])
    
    df=df.rename(columns={
            'id':'user_id',
            'email':'user_email',
            'username':'username'
    })

    df=df[['user_id' , 'user_email' , 'username' , 'first_name' , 'last_name' , 'street' , 'city' , 'zipcode']]

    return df

