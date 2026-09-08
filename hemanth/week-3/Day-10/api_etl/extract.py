import json
import time
from pathlib import Path
import requests


def request_with_retry(url,params=None,max_retries=3):
    for attempt in range(1, max_retries + 1):

        try:
            response = requests.get(
                url,
                params=params,
                timeout=10
            )

            if response.status_code == 429:

                if attempt == max_retries:
                    response.raise_for_status()

                retry_after = response.headers.get("Retry-After")

                if retry_after:
                    wait_time = int(retry_after)
                else:
                    wait_time = 2 ** (attempt - 1)

                print(
                    f"429 received. "
                    f"Waiting {wait_time}s."
                )

                time.sleep(wait_time)
                continue
            if response.status_code in (
                500,
                502,
                503,
                504
            ):

                if attempt == max_retries:
                    response.raise_for_status()

                wait_time = 2 ** (attempt - 1)

                print(
                    f"Server error {response.status_code}. "
                    f"Retrying in {wait_time}s."
                )

                time.sleep(wait_time)
                continue

            response.raise_for_status()

            return response

        except requests.exceptions.Timeout:

            if attempt == max_retries:
                raise

            wait_time = 2 ** (attempt - 1)

            print(
                f"Timeout. "
                f"Retrying in {wait_time}s."
            )

            time.sleep(wait_time)

        except requests.exceptions.ConnectionError:

            if attempt == max_retries:
                raise

            wait_time = 2 ** (attempt - 1)

            print(
                f"Connection error. "
                f"Retrying in {wait_time}s."
            )

            time.sleep(wait_time)

    raise RuntimeError(
        "Request failed after retries."
    )


BASE_URL = "https://dummyjson.com/products"


raw_dir = Path("raw")
raw_dir.mkdir(exist_ok=True)
#creating directory to store paginated results


limit = 10
skip = 0
page_num = 0
#offset pagination params

while True:

    params = {
        "limit": limit,
        "skip": skip
    }

    try:

        # Use the retry function here
        response = request_with_retry(BASE_URL,params=params,max_retries=3)

    except requests.exceptions.Timeout:
        print("Request timed out.")
        raise

    except requests.exceptions.ConnectionError:
        print("Connection failed.")
        raise

    except requests.exceptions.HTTPError as e:
        print(
            f"HTTP error on page {page_num}: {e}"
        )
        raise

    data = response.json()

    products = data["products"]


    if not products:
        break #if not data available,break out of loop

    raw_file = raw_dir / f"products_{page_num:03d}.json"

    with open(raw_file,"w",encoding="utf-8") as file:
      json.dump(data,file,indent=3) #converting python object into json file

    print(f"Page {page_num}: "f"{len(products)} products")

    skip += limit
    page_num += 1