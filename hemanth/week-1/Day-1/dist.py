import dis

def byte_code():
    x = 10
    print(x)

byte_code()
print(dis.dis(byte_code))  #returns byte code of byte_code function