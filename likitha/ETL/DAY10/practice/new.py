import pandas as pd
import requests
import time

### concepts we need to implement are ##########
#session
#authentication header
#pagination
#retry
#timeout
#rate limit
#exception raise for status 


# Timeout detects a request taking too long. 429 detects rate limiting. 
# Retry-After tells us how long to wait. sleep() performs the waiting.
#  continue moves to another retry attempt.
#  for attempt in range(3) provides the retry attempts. 
# while True handles pagination.
# timeout and Retry-After themselves do not perform retries. 
# They are conditions/instructions; the retry loop is what gives the program another chance.

def extract_products():
    BASE_URL="https://fakestoreapi.com"

    url=f'{BASE_URL}/products'

    session=requests.Session()
    session.headers.update({
        "Accept": "application/json"
    })

    all_products=[]

    page=1
    limit=100

    while True:
        params={
            "page":page,
            "limit":limit        }
        data=None
        for attempt in range(3):
            try:
                response=session.get(url , params=params , timeout=10)

                if response.status_code == 429:
                    retry_after=response.headers.get("Retry_After" , 5)
                    waitTime=int(retry_after)
                    print(
                        f"Rate limit reached. "
                        f"Waiting {waitTime} seconds..."
                        )
                    
                    time.sleep(waitTime)
                    
                    continue
                response.raise_for_status()
                
                data = response.json()
                print(data)
                break

            except requests.RequestException as e:
            
                print(
                        f"Request failed: {e}"
                    )
                #for 3rd (last attempt)
                if attempt == 2:
                        raise
                #for 1 and 2 attempts , we are increasing waiting time (exponential backoff)- increasing each time 
                time.sleep(2 ** attempt)

        #if no data in the page ( leave the pagination loop )
        if not data:
             break

        #if present extend the list

        all_products.extend(data)
        page+=1
        # FakeStoreAPI returns all items at once; break early to avoid infinite loop
        # Remove this condition if using a real paginated endpoint
        if len(data) < limit:
            break
    return pd.DataFrame(all_products)

extract_products()
