import requests

# Data to be posted
data = {
    "title": "API Practice",
    "body": "Learning GET and POST",
    "userId": 1
}

# API URL
url = "https://jsonplaceholder.typicode.com/posts"

# POST request
response = requests.post(url, json=data)

print(response.status_code)
print(response.text)