import time

a = "aaa"
print(a)
before = time.time()
while time.time() - before < 2:
    continue

b = 'bbb'
print(b)