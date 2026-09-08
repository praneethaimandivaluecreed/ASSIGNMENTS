import requests

# api
url = "https://jsonplaceholder.typicode.com/users"

# get request to the api
response = requests.get(url)

#response of the api
print(response)  # prints the status code

print("Response object:")
print(response)

print("URL:")
print(response.url)

print("\nStatus code:")
print(response.status_code)

print("\nHeaders:")
print(response.headers)

print("\nBody:")
print(response.text)
