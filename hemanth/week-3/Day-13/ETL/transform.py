from extract import extract_students
import pandas as pd

def inspect(df):
  print(df.head())
  print(df.tail())

  print("info: ")
  print(df.info())

  print("\n describe: ")
  print(df.describe())

  print('\n datatypes:')
  print(df.dtypes)

  print('\n duplicate sum')
  print(df.duplicated().sum())

  print('\n null values')
  print(df.isna().sum())

def convert_data_types(df):

 #[19 20 21 22 23 24 25 18 '22' None 'twenty' '21' '19']
 #performing replacement and type conversion on age
 df['age'] = df['age'].replace('twenty',20)
 df['age'] = df['age'].apply(pd.to_numeric,errors='coerce')

 #similary for marks
 df['marks'] = df['marks'].replace('eighty',80)
 df['marks'] = pd.to_numeric(df['marks'], errors='coerce')

 #similary for attendance
 df['attendance'] = df['attendance'].replace('eighty',80)
 df['attendance'] = pd.to_numeric(df['attendance'],errors='coerce')

 return df



def handle_missing_values(df):
  df['age'] = df['age'].fillna(df['age'].median())

  df['marks'] = df['marks'].fillna(df['marks'].median())

  df['attendance'] = df['attendance'].fillna(df['attendance'].median())

  df['gender'] = df['gender'].fillna("Unknown")
  df['city'] = df['city'].fillna("Unknown")

  return df

def handle_duplicates(df):
  df = df.drop_duplicates()
  return df

def standardize_text(df):
    
    # student_name
    df["student_name"] = df["student_name"].str.strip()

    # gender
    df["gender"] = df["gender"].str.strip().str.lower()

    gender_mapping = {
        "m": "Male",
        "male": "Male",
        "f": "Female",
        "female": "Female"
    }

    df["gender"] = df["gender"].replace(gender_mapping)

    # course
    df["course"] = df["course"].str.strip().str.lower()

    course_mapping = {
        "python": "Python",
        "sql": "SQL",
        "data science": "Data Science",
        "computer science": "Computer Science"
    }

    df["course"] = df["course"].replace(course_mapping)

    # city
    df["city"] = df["city"].str.strip().str.title()

    return df

def apply_bussiness_rules(df):
  df.loc[(df["age"] < 18) | (df["age"] > 60), "age"] = df["age"].median()

  df.loc[(df['marks']<0),'marks'] = 0
  df.loc[(df['marks']>100),'marks'] = 100

  df.loc[(df['attendance']<0) ,'attendance'] = 0
  df.loc[(df['attendance']>100),'attendance'] = 100

  return df
  

def check(df):
  print(df.head())
  print(df.tail())
  print(df.info())
  print(df.describe())
  print(df.dtypes)
  print(df.duplicated().sum())
  print(df.isna().sum())


def transform_products(df):
#   inspect(df)
  converted_df =convert_data_types(df)
  Non_nulled_df =handle_missing_values(converted_df)
  deduplicated_df= handle_duplicates(Non_nulled_df)
  standardized_df = standardize_text(deduplicated_df)
  valid_df = apply_bussiness_rules(standardized_df)
  return valid_df
