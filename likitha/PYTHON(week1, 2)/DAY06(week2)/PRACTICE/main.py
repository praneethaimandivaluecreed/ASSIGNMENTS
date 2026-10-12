import os
import csv 

# print(os.getcwd())

# print(os.path.abspath("/data/info.txt"))


################### emoji's are not printed in cp1252 encoding ############## 
######### default for windows is cp1252 ###########################

# file_path="data/info.txt"

# file=open(file_path,'r', encoding="utf-8")
# content=file.read()
# print(content)
# print(file)
# file.close()

####################### printing without read , directly from file object ################################

# file=open("data/info.txt" , 'r')
# for line in file:
#     print(line)

################## opening same file for many times to make os limit hit #################
# for i in range(100000):
#     file = open("data/info.txt", "r")

###################### exclusive mode ##########################################
# with open("data/newfile.txt" , 'x') as file:
#     file.write("hello , its an exclusive mode")


############################ how does a cursor working and writing ###########################
# with open("data/newfile.txt" , 'r+') as file:
#     file.write("oye")

# with open("data/newfile.txt" , 'w') as file:
#     file.write("oye")

# with open("data/newfile.txt" , 'r+') as file:
#     file.seek(5)
#     file.write("what is this")

# with open("data/newfile.txt" , 'a') as file:
#     file.seek(5)
#     file.write("what is this")


##################################################### file read in appending mode ##########################
# with open("data/newfile.txt" , 'a+') as file:
    # file.seek(5)
    # print(file.read())  
#     file.write("what is this")
#     print(file.read())


#prints nothing 
# with open("data/newfile.txt" , 'a+') as file:
#     print(file.read())  


################################################### binary file ##############################################
# with open("data/binnewfile.bin", 'wb') as file:
#     file.write(b"Hello")

# with open("data/binnewfile.bin", 'rb') as file:
#     print(type(file.read()))

# text = "Hello नमस्ते 😊"

# encoded = text.encode("utf-8")

# print(encoded)

# decoded=encoded.decode("utf-8")

# print(decoded)


################################################## csv ################################################################
# with open("data/data.csv" , 'r') as file:
#     print(file.read())
#     reader=csv.reader(file)
#     for row in reader:
#         print(row)

# with open("data/data.csv" , 'w' , newline='') as file:
#     # print(file.read())
#     writer=csv.writer(file)
#     writer.writerow(["name" , "age "])
#     writer.writerow(["honey" , 45])
#     writer.writerow(["nicky" , 30])


############### tried for understanding exception###############

# try:
# print("first")
# 10/0
#     print("second")
# except Exception as e:
#     print("error", e)

# print("third")


# print("first")
# 10/0
# print("third")