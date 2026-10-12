import pandas as pd 
from config import SOURCE_FILE

def extract():
    print("Starting Extracting")
    data=pd.read_csv(SOURCE_FILE)
    print(f"Extract {len(data)} records")

    return data