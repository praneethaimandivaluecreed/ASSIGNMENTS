from pathlib import Path


# creation and joining
path=Path("data") / "employee.csv"

# #file name details
# print(path.name)
# print(path.suffix)
# print(path.parent)
# print(path.stem)
# print(path.parent.parent)
# print(path.parts)
# print(path.anchor)

# print(path.exists())
# print(path.is_dir())
# print(path.is_file())

######## file operation #############

# with path.open("r", encoding="utf-8") as file:
#     print(file.read())

# content=path.read_text(encoding="utf-8")
# path.write_text("", encoding="utf-8")

############### touch , creating an empty file ######

# p=Path("data") / "emp.txt"
# p.touch()

############ for directory #################

# d=Path("data/dic")
# d.mkdir()

# dd=Path("data/demo/emo") # didnt give an error but didnt create it 
# dd.mkdir

# So lets try this 

# ddd=Path("data/demo/emo")
# ddd.mkdir(parents=True) # now it got created , # trying to run the same code again , got error . 

# to overcome it 
# ddd=Path("data/demo/emo")
# ddd.mkdir(exist_ok=True) # now no error

############################################# prints iterdir() ##########################
folder=Path("data")
# for i in folder.iterdir():
#     print(i)


################################################  glob , rglob ###################################

# for i in folder.glob("*.csv"):
#    print(i)

# for i in folder.rglob("*.csv"):
#    print(i)


########################################## PATH CONVERSION /RESOLUTION ################################

print(path.absolute())
print(path.resolve())
print(path.relative_to("data")) #### should mention only the path you wrote in Path , not , if you try "DAY06 " , it doesnt work 