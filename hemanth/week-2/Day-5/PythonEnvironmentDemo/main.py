import pandas as pd # type: ignore
import requests # type: ignore

print("Virtual environment is working!")

data = {
    "Name": ["Alice", "Bob"],
    "Salary": [50000, 60000]
}

df = pd.DataFrame(data)

print(df)