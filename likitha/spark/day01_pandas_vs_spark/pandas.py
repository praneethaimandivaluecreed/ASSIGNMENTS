import pandas as pd

df=pd.read_csv('employees.csv')
print(df)


# 3. Filter employees
# Salary greater than 60,000
high_salary = df[df["salary"] > 60000]
print(high_salary)


# 4. Group by department
# and calculate average salary

department_salary = (
    df.groupby("department", as_index=False)["salary"]
      .mean()
      .rename(columns={"salary": "average_salary"})
)



# 5. Sort by average salary

department_salary = department_salary.sort_values(
    by="average_salary",
    ascending=False
)



print(department_salary)