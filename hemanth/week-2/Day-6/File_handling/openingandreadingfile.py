#open() creates a file object so that you can perform operations on it
# and file name will be reference to that object

file = open("data.txt",'r')
content = file.read()

#prints the actual file object- various details of file object
print(file)

print(file.name)
print(file.mode)
print(file.encoding)
print(file.closed)

print(content)
file.close()
print(file.closed) 
#returns false ,because file is closed (actual system file is closed) .but file object stills exists

#opening file usin with statement:

with open('data.txt','r') as f:
    print(f.read())
    print(f.closed)
print(f.closed)


#reading multiple lines from file

with open("data.txt", "r") as file:

    #the line in the file already contains \n, and print() adds its own newline too, 
    # producing the blank lines.
    for line in file:
        print(line.strip())
        #strip() removes the newline character from the end of each line.

    print()
    print("without striping")
    print()

    file.seek(0)

    for line in file:
        print(line)

with open("data.txt",'r') as f:
    lines = f.readlines()
    count = 0
    for line in lines:
        count += 1
        print(f'Line {count} - {line.strip()}')

with open("data.txt",'r') as f:
    line = f.readline()
    while line:
        print(line.strip())
        line = f.readline()
