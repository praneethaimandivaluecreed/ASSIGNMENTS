import requests
import time

url = "https://jsonplaceholder.typicode.com/users"

max_attempts = 3

for attempt in range(1, max_attempts + 1):

    try:
        response = requests.get(url, timeout=5)

        if response.status_code == 200:
            print("Success!")
            data = response.json()
            break

        elif response.status_code == 429:
            print("Rate limit exceeded")

        elif response.status_code in [500, 502, 503]:
            print("Temporary server error:", response.status_code)

        else:
            print("Permanent failure:", response.status_code)
            break

    except requests.exceptions.Timeout:
        print("Request timed out")

    except requests.exceptions.RequestException as e:
        print("Network error:", e)

    if attempt < max_attempts:
        wait_time = 2 ** (attempt - 1)
        print("Waiting", wait_time, "seconds...")
        time.sleep(wait_time)