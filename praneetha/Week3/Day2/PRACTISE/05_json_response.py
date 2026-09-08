import requests

url = "https://jsonplaceholder.typicode.com/users"

response = requests.get(url)

# converting the json response into python list
data = response.json()
print(len(data))


# print name and city of all people
for user in data:
    print(user["name"])
    print(user["address"]["city"])