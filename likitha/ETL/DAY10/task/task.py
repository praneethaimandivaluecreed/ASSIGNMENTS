import requests
import json
import time

url = "https://dummyjson.com/products"

page = 0
limit = 10

while True:

    skip = page * limit

    try:
        response = requests.get(
            url,
            params={"limit": limit, "skip": skip},
            timeout=10
        )

        if response.status_code == 200:

            data = response.json()

            products = data["products"]

            # Stop when no more products
            if len(products) == 0:
                break

            # Save raw response
            with open(f"raw_page_{page + 1}.json", "w") as file:
                json.dump(data, file, indent=4)

            print(f"Page {page + 1} saved")

            page += 1

            time.sleep(1)

        elif response.status_code == 404:
            print("Error: API endpoint not found")
            break

        elif response.status_code == 429:
            print("Too many requests. Waiting...")
            time.sleep(5)

        elif response.status_code >= 500:
            print("Server error. Try again later.")
            break

        else:
            print("HTTP Error:", response.status_code)
            break

    except requests.exceptions.Timeout:
        print("Request timed out")
        break

    except requests.exceptions.ConnectionError:
        print("Connection error")
        break

    except requests.exceptions.RequestException as e:
        print("Request failed:", e)
        break