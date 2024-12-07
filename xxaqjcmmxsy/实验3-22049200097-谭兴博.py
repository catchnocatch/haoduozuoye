import random
import os
import math

def extended_gcd(a, b):
    """扩展欧几里得算法，返回 gcd(a, b) 及 x, y，使得 ax + by = gcd(a, b)"""
    if b == 0:
        return a, 1, 0
    gcd_val, x1, y1 = extended_gcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return gcd_val, x, y

def mod_inverse(a, m):
    """计算 a 在模 m 下的逆元"""
    gcd_val, x, _ = extended_gcd(a, m)
    if gcd_val != 1:
        raise ValueError("Inverse does not exist")
    return x % m

def calculate_products(m):
    """计算每个 m_j 的值，返回一个列表"""
    products = [1] * len(m)
    for i in range(len(m)):
        for j in range(len(m)):
            if i != j:
                products[i] *= m[j]  # products[i] = Π m_j (j ≠ i)
    return products

def calculate_N_and_M(moduli, threshold):
    """计算 N 和 M 的值"""
    N_product = 1
    M_product = 1
    for i in range(threshold):
        N_product *= moduli[i]
    for i in range(len(moduli) - threshold + 1, len(moduli)):
        M_product *= moduli[i]
    return N_product, M_product

def compute_subsecrets(moduli, secret):
    """计算 secret 在每个 moduli[i] 模下的值"""
    return [secret % di for di in moduli]

def recover_secret(subsecrets, moduli, threshold):
    """根据中国剩余定理恢复秘密"""
    mod_values = moduli[:threshold]
    secret_values = subsecrets[:threshold]
    
    M_total = 1
    for mi in mod_values:
        M_total *= mi  # 计算 M = Π m_i

    products = calculate_products(mod_values)
    inverses = [mod_inverse(products[i], mod_values[i]) for i in range(threshold)]
    
    recovered_value = sum(products[i] * inverses[i] * secret_values[i] for i in range(threshold))
    
    return recovered_value % M_total

def are_coprime(moduli, count):
    """判断 moduli 中的所有数是否两两互素"""
    for i in range(count):
        for j in range(i + 1, count):
            if math.gcd(moduli[i], moduli[j]) != 1:
                return False
    return True

def generate_moduli(secret_value, count=5):
    """随机生成互素的 moduli 值，确保 N > k > M"""
    moduli = [1] * count
    while True:
        for i in range(count):
            moduli[i] = random.randint(pow(10, 167), pow(10, 168))
        if are_coprime(moduli, count):
            N_product, M_product = calculate_N_and_M(moduli, 3)
            if N_product > secret_value and M_product < secret_value:
                break
    return sorted(moduli)

# 验证 t-1 个子秘密不能恢复 k
def test_recovery_failure(threshold, secret_value, moduli):
    """验证使用 t-1 个子秘密无法恢复 k"""
    sub_secret_values = compute_subsecrets(moduli, secret_value)[:threshold-1]  # 取前 t-1 个子秘密
    try:
        result = recover_secret(sub_secret_values, moduli, threshold-1)
        print(f"\n使用 {threshold-1} 个子秘密恢复的结果: {result}")
        if result == secret_value:
            print("恢复正确，测试失败！")
        else:
            print("恢复错误，测试成功！")
    except Exception as e:
        print(f"发生错误: {e}")

# 主程序
if __name__ == "__main__":
    threshold = 3
    n = 5
    file_path = os.path.join("xxaqjcmmxsy", "secret1.txt")
    
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            secret_value = int(file.read().strip())  # 去除首尾空白字符并转换为整数
            print("成功读取秘密:", secret_value)
    except FileNotFoundError:
        print(f"错误: 文件未找到: {file_path}")
        exit(1)  # 退出程序
    except IOError as error:
        print(f"文件读取错误: {error}")
        exit(1)  # 退出程序
    except Exception as error:
        print(f"发生未知错误: {error}")
        exit(1)  # 退出程序

    moduli = generate_moduli(secret_value)
    print("\n生成的模数数组di为:")
    for i in moduli:
        print(f"\n{i}")
    
    N_product, M_product = calculate_N_and_M(moduli, threshold)
    print("\nN的值为:", N_product)
    print("\nM的值为:", M_product)

    sub_secret_values = compute_subsecrets(moduli, secret_value)
    result = recover_secret(sub_secret_values, moduli, threshold)
    print("最后恢复的明文为:", result)

    if result == secret_value:
        print("恢复正确！")
    else:
        print("恢复错误！")

    # 验证 t-1 个子秘密不能恢复 k
    test_recovery_failure(threshold, secret_value, moduli)