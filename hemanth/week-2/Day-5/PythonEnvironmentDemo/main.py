import pandas as pd
import requests

print("Virtual environment is working!")

data = {
    "Name": ["Alice", "Bob"],
    "Salary": [50000, 60000]
}

df = pd.DataFrame(data)

print(df)