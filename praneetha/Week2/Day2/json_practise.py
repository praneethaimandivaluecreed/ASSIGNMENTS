import json

#data to be inserted into json
student = {
    "name": "Praneetha",
    "marks": 85
}


#dumping the student.json
# with open("student.json","w") as file :
#     json.dump(student)



#loading the data
with open("student.json", "r") as file:
    data = json.load(file)
    print(data)