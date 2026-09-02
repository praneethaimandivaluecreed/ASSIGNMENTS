data = b"Hello Python"
#writing data in binary file 

with open("data.bin","wb") as file:
    file.write(data)
print("Binary file created")


#reading binary file
with open("data.bin",'rb') as file:
    content = file.read()
    print(content)
    
    print(type(content))

    for byte in content:
        print(byte)

# opening and reading file in chunks
with open("data.bin", "rb") as f:

    chunk = f.read(5)

    print(chunk)
    print(type(chunk))

#comparing reading of binary file with text file
with open("data.txt", "r") as f:
    content = f.read()

    print(content)
    print(type(content))