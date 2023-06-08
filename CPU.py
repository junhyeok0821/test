'''
a = 1
b = 10
c = [1, 2, 3, 4, 5]

while a < b:
    a += 1
    print(a)
for item in c:
    print(item)

for index in range(0, len(c), 1):
    print(c[index])
'''

a = int(input("수를 입력: "))
b = int(input("수를 입력: "))
c = input("기호를 입력: ")

if c == "+":
    print(a+b)

elif c == "-":
    print(a-b)

elif c == "*":
    print(a*b)

elif c == "/":
    print(a/b)