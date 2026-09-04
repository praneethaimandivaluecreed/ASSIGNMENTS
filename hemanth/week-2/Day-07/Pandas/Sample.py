import pandas as pd

#Printing empty dataframe
df = pd.DataFrame()
print(df)


#Loading Data in DataFrame
Data = {
    "Name":["Alice","Bob","Charlie","David"],
    "Age":[23,22,25,26],
    'Salary':[20000.00,24999.99,35000,40000]
}
df = pd.DataFrame(Data)
print(df)
df = df.set_index("Name")
print(df)
df = df.reset_index()
print(df)
df = df.set_index("Name")
print(df)
df = df.reset_index(drop=True)
print(df)

#Loading missing Data
df = pd.read_csv("data.csv")
print(df)

#understanding the syntax of pd.DataFrame

data = [
    [101, "Rahul", "IT"],
    [102, "Priya", "HR"],
    [103, "Arjun", "Finance"]
]
cols =["ID","Name","Department"]
df = pd.DataFrame(data,columns=cols,index=[101,102,103])

print(df)
print(df[df["Name"]=="Rahul"])
print(df.iloc[2])
print(df.loc[101:103,['Name','Department']])
print(df['ID']==101)
print(df[df['ID']==101])
print(df.at[101,"Department"]) #access value for row/column label pair
print(df.query("ID > 101 ")) #query the database using condition

#Accessing the df

Data = {
    "Name":["Alice","Bob","Charlie","David"],
    "Age":[23,22,25,26],
    'Salary':[20000.00,24999.99,35000,40000]
}
df = pd.DataFrame(Data)
print(df["Age"])
print(df[["Age",'Salary']])
print(df.loc[[0,2],["Name","Salary"]]) # row_labels and col_labels
print(df.loc[:,["Name","Age",'Salary']])
print(df.iloc[3])
print(df.iloc[[0,1,2]])
print(df.iloc[[0,1,2],[0,1]]) #row_positions ,col_positions
print(df.iloc[:])

#Summary

df = pd.read_csv('nba.csv')
print(df.index)
print(type(df))
print(df.head())
print(df.tail())
print(df.info())
print(df.describe())

#filtering the dataFrame

df = pd.DataFrame({'Name': [' RACHEL  ', ' MONICA  ', ' PHOEBE  ',
                                   '  ROSS    ', 'CHANDLER', ' JOEY    '],
                          
                          'Age': [30, 35, 37, 33, 34, 30],
                          
                          'Salary': [100000, 93000, 88000, 120000, 94000, 95000],
                          
                          'JOB': ['DESIGNER', 'CHEF', 'MASUS', 'PALENTOLOGY',
                                  'IT', 'ARTIST']})

print(df[(df["Salary"]>= 100000) & (df["Age"]<40 ) &(df["JOB"].str.startswith("D"))])
print(df.query('Salary  <= 100000 & Age < 40 & JOB.str.startswith("C").values'))
# similar function is eval

# Merging, Joining and Concatenating


data1 = {'Name': ['Jai', 'Princi', 'Gaurav', 'Anuj'],
         'Age': [27, 24, 22, 32],
         'Address': ['Nagpur', 'Kanpur', 'Allahabad', 'Kannuaj'],   
         'Qualification': ['Msc', 'MA', 'MCA', 'Phd']}

data2 = {'Name': ['Abhi', 'Ayushi', 'Dhiraj', 'Hitesh'],
         'Age': [17, 14, 12, 52],
         'Address': ['Nagpur', 'Kanpur', 'Allahabad', 'Kannuaj'],
         'Qualification': ['Btech', 'B.A', 'Bcom', 'B.hons']}

df = pd.DataFrame(data1, index=[0, 1, 2, 3])

df1 = pd.DataFrame(data2, index=[4, 5, 6, 7])

print(pd.concat([df,df1]))  #pd.concat([object1, object2])

# default syntax 
# pd.concat(
#     [object1, object2, object3],
#     axis=0,
#     join='outer', when concating all coloums are added with NaN values,but with inner only commmon coloums are 
#     ignore_index=False
# )

print(pd.concat([df,df1],axis=1))
print(pd.concat([df,df1],axis=1,ignore_index=True))

data1 = {'key': ['K0', 'K1', 'K2', 'K3'],
         'Name':['Jai', 'Princi', 'Gaurav', 'Anuj'],
        'Age':[27, 24, 22, 32],}

data2 = {'key': ['K0', 'K1', 'K2', 'K3'],
         'Address':['Nagpur', 'Kanpur', 'Allahabad', 'Kannuaj'],
        'Qualification':['Btech', 'B.A', 'Bcom', 'B.hons']}

df = pd.DataFrame(data1)

df1 = pd.DataFrame(data2)

print(df.merge(df1,on='key'))
print(df.merge(df1,how="left",on='key'))
print(df.merge(df1,how='right',on='key'))

# df.sort_values(by = "Age",ascending=False,inplace=True,na_position="first",kind='quicksort') #key=lambda col: col.str.lower()

#working with csv files

df = pd.read_csv("people.csv")
print(df.info())

df = pd.read_csv("people.csv", parse_dates=["Date of birth"])
print(df.info())

#writing data in csv

Data = {
    "Name":["Alice","Bob","Charlie","David"],
    "Age":[23,22,25,26],
    'Salary':[20000.00,24999.99,35000,None]
}
df = pd.DataFrame(Data)
df.to_csv("written_csv.csv",header =False,index=False,sep='\t',na_rep="nothing")


df = pd.read_csv("written_csv.csv",sep="\t")
print(df)


#working with json

df = pd.read_json("details.json")
print(df)

df1=pd.read_json("nestedjson.json")
print(df1)