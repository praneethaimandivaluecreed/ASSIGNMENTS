import requests
import pandas as pd
import time


def extract_products(url):

    session = requests.Session()

    session.headers.update({
        "Accept": "application/json"
    })

    all_products = []

    page = 1

    while True:

        params = {
            "page": page,
            "limit": 100
        }

        for attempt in range(3):

            try:

                response = session.get(
                    url,
                    params=params,
                    timeout=10
                )

                if response.status_code == 429:

                    wait_time = int(
                        response.headers.get(
                            "Retry-After", 5
                        )
                    )

                    print(
                        f"Rate limit reached. "
                        f"Waiting {wait_time} seconds..."
                    )

                    time.sleep(wait_time)

                    continue

                response.raise_for_status()

                data = response.json()

                break

            except requests.RequestException as e:

                print(
                    f"Request failed: {e}"
                )

                if attempt == 2:
                    raise

                time.sleep(2 ** attempt)

        #if pages have no data and also if any interruptions caused an exception in one page ( it doesnt move to next page )
        if not data:
            break

        all_products.extend(data)

        page += 1

    return pd.DataFrame(all_products)

extract_products("https://fakestoreapi.com/products")