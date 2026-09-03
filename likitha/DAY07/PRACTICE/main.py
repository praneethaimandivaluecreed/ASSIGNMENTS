#######################################  PANDAS   ######################################################

import pandas as pd


data=[1,2,3,4]

series=pd.Series(data)
print(series)


############### length of the index need to match ###################
series=pd.Series(data , index=["how", "are" , 4 , 5 ])
print(series)

# series=pd.Series(data , index=["how", "are" , 4 ]) ## Value error

calories = {"day1": 420, "day2": 380, "day3": 390}
myvar = pd.Series(calories)
print(myvar)



#DataFrame
df=pd.DataFrame() #calling dataframe constructor
print(df) # EMpty data frame

list=["rgukt", "students" , "portal" , "cse"]
df=pd.DataFrame(list)
print(df)

########### load files in pandas ##########
df = pd.read_csv(r'C:\Users\Likhita\Desktop\engineering\vc\DataAnalytics\ASSIGNMENTS\likitha\DAY07\PRACTICE\employee.csv', on_bad_lines='skip')
print(df)
print(df.to_string())

### for excel we have .read_excel()
### output into a file with pandas 
# df.to_excel("diabetes_out.xlsx", index=False)
## requires external openpyxl ot be installed
# df.to_csv("diabetes_out.csv", index=False)

# df.to_json("diabetes_out.json")

# df.to_csv('diabetes_out.txt', header=df.columns, index=None, sep=' ')


print(df.head())
print(df.tail())
print(df.head(2))
print(df.tail(2))
print(df.info())
print(df.describe())
print(df.describe(include=[int]))
print(df.describe(percentiles=[0.3,0.5,0.7]))
print(df.describe().T)


print(df.shape)
print(df.shape[0])
print(df.shape[1])
print(df.columns)
print(df.dtypes)

print(df["salary"].max())
print(series.max())


####### getting subset of a data frame 
# if one column then
print(df["salary"]) # doesnt print salary column , instead gives name and dtype . used for doing df["salary"].shape
# for multiple columns
print(df[["name", "salary"]])

### filtering the rows 
print(df[df["salary"]> 10000])
print(df["salary"]> 10000)
# print(df[ (["salary"]==40000) | (["salary"]==45000)] )
print(df["salary"].isin([40000 , 42000]))

print(df["salary"].notna())

#### filtering row and column
print(df.loc[df["salary"]>40000 , "name"])
print(df.iloc[2:4, 0:2])
print(df.iloc[2:4 , 3]== 45000)

### deriving new columns from existing ones
df["bonus"]=df["salary"]+3000
print(df.head())


### Rename columns
df_name=df.rename(
    columns={
        "id":"emp_id",
        "name":"emp_name"
    }
)
print(df)
print(df_name)

############# statistics
print(df["salary"].mean())
print(df["salary"].median())
print(df[["salary" , "bonus"]].mean())
print(df.agg({
    "salary":["min","max","median","skew"],
    "bonus":["min","max","median","mean"],
}
))


####### Aggregrate values and group by
print(df[["department" , "bonus"]].groupby("department").max())

print(df.groupby("department").mean(numeric_only=True))

print(df.groupby("department")["bonus"].mean())
print(df["name"].value_counts())

#sort table
print(df.sort_values(by="salary" , ascending=False))

#pivot table
print(df.pivot(columns="department", values="salary"))

#### combining multiple tables
# df2=pd.concat([df , df1] , axis=0)

############ JOIN TABLES

# df2= pd.merge(df , df1 , how="left" , left_on="left_id" , right_on="right_id")

########## parsing data time , gives some advantages
# dddf=pd.read_csv("../data/air_quality_no2_long.csv", parse_dates=["datetime"])
# dddf["datetime"].min() 
# dddf["datetime"].max()
# these gives dates , handles in better way 

# dddf["month"]=dddf["datetime"].dt.month



######## resampling

#### manipulate textual data
print(df["name"].str.lower())
print(df["name"].str.contains("Ravi"))
print(df[df["name"].str.contains("Ravi")])
print(df.loc[df["name"].str.contains("Ravi") , "id"])
print(df["name"].replace({"Ravi":"R"}))
