import random
import math


def fastModCal(a: int, b: int, m: int):
    result = 1  # 初始化结果
    a = a % m  # 将 a 模 m，避免大数计算
    while b > 0:
        # 如果 b 是奇数
        if (b % 2) == 1:
            result = (result * a) % m
        # b 右移一位
        b //= 2
        # a 平方并模 m
        a = (a * a) % m
    return result


m = int(input("\n要检测的数m:"))
k = int(input("安全参数k: "))
i = 0

while i < k:
    a = random.randint(2, m - 2)
    print(f"k = {i+1},生成的随机数为 {a},")
    g = math.gcd(a, m)
    r = fastModCal(a, m - 1, m)
    if g != 1:
        print(f"({a},{m})={g},m是合数\n")
        break
    elif r != 1:
        print(f"{a} ** ({m}-1) mod {m} = {r},m是合数\n")
        break
    else:
        print("m可能为素数!")
        i += 1

if i == k :
    print(f"\n该数可能为素数，且概率为" + str((1 - 1 / (2**k)) * 100) + "%\n")

