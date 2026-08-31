departments = {"HR", "IT", "Finance", "IT", "HR"}

print(departments)
print(len(departments))
#duplicates are not present becuase it is a set. it is internally using a hashmap

departments.add("Operations")
departments.add("IT")
departments.remove("Finance")
print(departments)


team_a = {"HR", "IT", "Finance"}
team_b = {"IT", "Marketing", "Finance"}
print(team_a.union(team_b))
print(team_a.intersection(team_b))
print(team_a | team_b)
print(team_a & team_b)


print(team_a - team_b)
print(team_b - team_a)
print(team_a ^ team_b)


#5. Remove Duplicates from a List
employee_departments = [
    "HR", "IT", "HR",
    "Finance", "IT",
    "Operations"
]

s = set(employee_departments)
print(s)


#6. find duplicate ids
ids = [101, 102, 103, 101, 104, 102, 105, 101]
s1 = set()
l = []
for item  in ids:
    if item  in s1 and item not in l:
        l.append(item)
    else:
        s1.add(item)
print(l)