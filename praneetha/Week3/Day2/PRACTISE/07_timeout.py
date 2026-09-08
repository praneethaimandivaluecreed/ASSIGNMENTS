import requests

url = "https://jsonplaceholder.typicode.com/users"

try:
    response = requests.get(url, timeout=5)

    print("Status:", response.status_code)
    print("Data received successfully")

except requests.exceptions.Timeout:
    print("The API took too long to respond")