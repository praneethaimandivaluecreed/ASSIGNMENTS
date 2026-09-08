import requests as r
import pandas as pd
url = "https://jsonplaceholder.typicode.com/posts"
params ={
    'id' : 1
}
response = r.get(url,params=params) # params = params,appends the json as parameters to the us

print(response) #python response object
print(type(response))
print(response.status_code) # returns the status code of response
print(response.headers) # prints headers of the response
print(response.url) #api url

print("---------------------------------------------------------")
print(response.content) # prints the response as byte array

data = response.json() #parses json into python object
# print(data)
print(type(data))

df = pd.DataFrame(data)
print(df.head())
print(df.tail())
print(df.info())
print(df.describe())
print(df.dtypes)