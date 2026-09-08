import requests


# not found url
url = "https://jsonplaceholder.typicode.com/abc"

response = requests.get(url)

print("Status:", response.status_code) # 404
print("Response:", response.text)