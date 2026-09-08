import requests


# requesting data from page 1 to page 4
url = "https://jsonplaceholder.typicode.com/posts"

for page in range(1, 5):
    params = {
        "_page": page,
        "_limit": 5
    }

    response = requests.get(url, params=params)
    data = response.json()

    print("PAGE:", page)

    for post in data:
        print(post["id"], post["title"])

    print()




#requesting pages till complete data is retrieve
url = "https://jsonplaceholder.typicode.com/posts"

all_posts = []

page = 1
limit = 12

while True:

    params = {
        "_page": page,
        "_limit": limit
    }

    response = requests.get(url, params=params)
    data = response.json()

    # If the page contains no records, stop
    if len(data) == 0:
        break

    # Add this page's records to our main list
    all_posts.extend(data)

    print("Page", page, "→", len(data), "records")

    page += 1

print("Total records:", len(all_posts))