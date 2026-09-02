#step1 - writing data into file

# with open("student.txt","w") as file:
#     file.write("Name : Praneetha \n Course : Data analytics")
    

# step2 - appending data into file

# with open("student.txt", "a") as file :
#     file.write("\nLearning: Python File Handling")


#step3 - reading complete file


#write+read mode
with open("student.txt", "w+") as file:
    file.write("Niharika")
    print("first")
    print(file.read())  
    file.seek(0)
    print("second")
    print(file.read()) 
    file.seek(4) 
    file.write("Rajeswari")
    file.seek(0)
    print(file.read())  



# read + write mode
with open("student.txt", "r+") as file:
    file.write("Niharika")
    print("first")
    print(file.read())  
    file.seek(0)
    print("second")
    print(file.read()) 
    file.seek(4) 
    file.write("Rajeswari")
    file.seek(0)
    print(file.read())  


#append + read mode
with open("student.txt", "a+") as file:
    file.write("Niharika")
    print("first")
    print(file.read())  
    file.seek(0)
    print("second")
    print(file.read()) 
    file.seek(4) 
    file.write("Rajeswari")
    file.seek(0)
    print(file.read())  


       
# with open("student.txt", "r+") as file:
#     file.write("Niharika")
#     print("first")
#     print(file.read())  
#     file.seek(0)
   
#     file.write("Rajeswari")
#     file.seek(0)
#     print("second")
#     print(file.read())  