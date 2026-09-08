import requests


# example with query parameters
url = "https://jsonplaceholder.typicode.com/posts"

# query parameter userId
params = {
    "userId" : 1,
     "id": 1
}

# get request with parameters
response = requests.get(url,params = params)

print(response.url)
print(response.status_code)
print(response.text)
print(type(response.json()))



# example with query parameter

#query parameter
user_id = 5

url = f"https://jsonplaceholder.typicode.com/users/{user_id}"

response = requests.get(url)

print(response.url)
print(response.status_code)
user = response.json()

# printing specific fields inside the response
print(user["email"])
print(user["address"])