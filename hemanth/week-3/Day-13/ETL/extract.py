import json 
import pandas as pd

def extract_students(filepath):
    with open(filepath,"r",encoding='utf-8') as file:
        data = json.load(file)

        df = pd.DataFrame(data)
        return df
