def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

# 定义素数 p 和 q
p = 1009
q = 3643

s = 0
P = (p - 1) * (q - 1)

# 遍历 e 的值
for e in range(2, P):
    if gcd(e, P) == 1 and gcd(e - 1, p - 1) == 2 and gcd(e - 1, q - 1) == 2:
        s += e

print(s)