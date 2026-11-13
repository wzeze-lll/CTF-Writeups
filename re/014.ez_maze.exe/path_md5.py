import hashlib

path = "sssssssddddwwwddsssssssdddsssddddd"

md5 = hashlib.md5(path.encode()).hexdigest()
print(md5)