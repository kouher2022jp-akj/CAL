import random

num1 = random.randint(1, 10)
num2= random.randint(1, 10)
operator = random.choice(["+", "-", "*", "/"])

if operator == "+":
    cor_ans = num1 + num2
elif operator == "-":
    cor_ans = num1 - num2
elif operator == "*":
    cor_ans = num1 * num2
else:
    cor_ans = num1 / num2



print(f"{num1} {operator} {num2} = ")

answer = float(input("Ans: "))

if round(answer, 2) == round(cor_ans, 2):
    print("Correct!")
else:
    print(f"Wrong!, It is {round(cor_ans, 2)}")