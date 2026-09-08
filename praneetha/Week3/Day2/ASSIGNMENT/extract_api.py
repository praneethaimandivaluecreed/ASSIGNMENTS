import requests
import json
import os
import time


# api 
url = "https://jsonplaceholder.typicode.com/posts"


# making a directory to store the extracted data
os.makedirs("raw_data", exist_ok=True)

# intializing parameters
page = 1
limit = 10


# extracting till there is no data left
while True:

    params = {
        "_page": page,
        "_limit": limit
    }

    try:
        response = requests.get(
            url,
            params=params,
            timeout=5  # setting timeout
        )

    except requests.exceptions.Timeout:
        print("Request timed out. Retrying...")
        time.sleep(2)
        continue

    except requests.exceptions.RequestException as e:
        print("Request failed:", e)
        break

    print("Page:", page)
    print("Status:", response.status_code)

    if response.status_code == 200:

        data = response.json()

        if len(data) == 0:
            print("No more data. Extraction complete.")
            break

        filename = f"raw_data/page_{page}.json"

        with open(filename, "w") as file:
            json.dump(data, file, indent=4)

        print("Saved:", filename)
        print("Records:", len(data))

        page += 1

    elif response.status_code == 400:
        print("Bad request.")
        break

    elif response.status_code == 401:
        print("Authentication failed.")
        break

    elif response.status_code == 403:
        print("Permission denied.")
        break

    elif response.status_code == 404:
        print("Endpoint not found.")
        break

    elif response.status_code == 429:
        print("Rate limit exceeded. Waiting...")
        time.sleep(5)

    elif response.status_code in [500, 502, 503]:
        print("Server error. Retrying...")
        time.sleep(2)

    else:
        print("Unexpected HTTP error:", response.status_code)
        break