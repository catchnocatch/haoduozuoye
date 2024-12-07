import math

def extended_gcd(a, b):
    """返回 gcd(a, b), x, y 满足 ax + by = gcd(a, b)"""
    if b == 0:
        return a, 1, 0
    gcd, x1, y1 = extended_gcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return gcd, x, y

def mod_inverse(a, m):
    """返回 a 关于 m 的模逆元"""
    gcd, x, _ = extended_gcd(a, m)
    if gcd != 1:
        raise ValueError("逆元不存在")
    return x % m

def judde_gcd(m_i):
    """检查 m_i 中的所有元素是否两两互质"""
    for i in range(len(m_i)):
        for j in range(i + 1, len(m_i)):
            if math.gcd(m_i[i], m_i[j]) != 1:
                return False
    return True

def cal_Mi(m_i, M):
    """计算 M_i = M / m_i"""
    return [M // mi for mi in m_i]

def cal_egcdMi(M_list, m_i):
    """计算 M_i 的模逆元"""
    return [mod_inverse(M_list[i], m_i[i]) for i in range(len(M_list))]

def chinese_remain_theory(m_i, a_i):
    """使用中国剩余定理解同余方程组"""
    if not judde_gcd(m_i):
        raise ValueError("不能直接运用中国剩余定理")
    
    # 计算模数的乘积
    m = math.prod(m_i)
    print(f"模数的乘积 M: {m}")

    # 计算 M_i
    M_list = cal_Mi(m_i, m)
    print(f"\nM_i 计算结果：{M_list}")

    # 计算 M_i 的模逆元
    egcdM_list = cal_egcdMi(M_list, m_i)
    print(f"\nM_i 模逆计算结果：{egcdM_list}")

    # 计算最终结果 x
    x = 0
    for i in range(len(a_i)):
        x_i = M_list[i] * egcdM_list[i] * a_i[i]
        print(f"\nx_{i} 计算结果：{x_i}")
        x += x_i
        x %= m
    
    print("************************************************")
    print(f"\n中国剩余定理计算结果：{x}")

# 输入部分
print("依次输入 a_i（每个数换行分隔）：")

a_i = []
while True:
    try:
        line = input()
        if line == "":
            break
        a_i.append(int(line))
    except ValueError:
        print("请输入有效的整数。")
        
print("\n依次输入 m_i（每个数换行分隔）：")
m_i = []
while True:
    try:
        line = input()
        if line == "":
            break
        m_i.append(int(line))
    except ValueError:
        print("请输入有效的整数。")



# 调用函数
try:
    chinese_remain_theory(m_i, a_i)
except ValueError as e:
    print(e)