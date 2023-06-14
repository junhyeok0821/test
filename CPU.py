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
'''
'''
cf = 5 # 커피 가격을 200원
while True:
    money = int(input("돈을 입력: "))



    if money == 200:
        print("커피를 줍니다.")
        cf -= 1
    elif money > 200:
        money = money - 200
        print("커피를 주고 거스름돈을 줍니다. 거스름돈 %d" %money)
        cf -= 1
    else:
        print("이것도 못사냐 그지련아")

    if cf == 0:
        print("커피가 부족합니다. 금액을 다시 반환합니다. 반환 금액 %d" %money)
        break


'''

num1 = int(input('1보다 큰 정수 입력'))
num2 = int(input('1보다 큰 정수 입력'))
maxNum = 0

for i in range(1, (num1 + 1)):
    if num1 % i ==0 and num2 % i ==0:
        print('공약수 : {}'.format(i))
        maxNum = i
print(f'최대 공약수 : {maxNum}')

minNum= (num1 * num2) // maxNum
print('최소공배수: {}'.format(minNum))


