import requests as req

url = "https://jsonplaceholder.typicode.com/posts"

data = {
    "title" : "My post",
    "body": "Hello World!",
    "userId": 1
}

response = req.post(url,json = data)
 # json=data,This tells requests that you want to send the Python object as JSON.
print(response)
print(response.status_code)
print(response.content)