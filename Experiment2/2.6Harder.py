from base64 import b64decode
from Cryptodome import Random
from Cryptodome.Cipher import AES
from random import randint

UNKNOWN_STRING = b"""
Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg
aGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq
dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg
YnkK"""

KEY = Random.new().read(16)
random_pre=Random.new().read(randint(0,255))

def pad(your_string, msg):
 
    paddedMsg = your_string + msg

    size = 16
    length = len(paddedMsg)
    if length % size == 0:
        return paddedMsg

    padding = size - (length % size)
    padValue = bytes([padding])
    paddedMsg += padValue * padding

    return paddedMsg


def encryption_oracle(your_string):
   
   # msg = bytes('The unknown string given to you was:\n', 'ascii')
    # append the `UNKNOWN_STRING` given to us to the `msg`
    #plaintext = msg + b64decode(UNKNOWN_STRING)
    #添加随机长度字节
    plaintext = b64decode(UNKNOWN_STRING)
    # add `your_string` to prepend to `plaintext` and apply `PKCS#7` padding to correct size
    paddedPlaintext = pad(random_pre+your_string, plaintext)

    cipher = AES.new(KEY, AES.MODE_ECB)
    ciphertext = cipher.encrypt(paddedPlaintext)

    return ciphertext

"""using the managable string before the unkown 
increase the len of managable string bit by bit,when the len of managable string and unkown encrypted changes,that means the number of block changes,then the blocking size is the changed len substract the before len;
"""
def detect_block_size():
    feed = b"A"  # 初始输入
    length = 0   # 上一次密文长度
    while True:
        cipher = encryption_oracle(feed)  # 调用加密oracle
        current_length = len(cipher)  # 获取当前密文长度
        
        if length != 0 and current_length > length:
            # 如果密文长度增加了，返回当前长度减去上一次长度
            return current_length - length
        
        length = current_length  # 更新长度
        feed += b"A"  # 每次迭代添加一个字符


def detect_mode(cipher):
    
    chunkSize = 16
    chunks = []
    for i in range(0, len(cipher), chunkSize):
        chunks.append(cipher[i:i+chunkSize])

    uniqueChunks = set(chunks)
    if len(chunks) > len(uniqueChunks):
        return "ECB"
    return "not ECB"

def detect_random_length():

    block_size=detect_block_size()

    sample1=encryption_oracle(b'a')
    sample2=encryption_oracle(b'b')

    length1=len(sample1)
    length2=len(sample2)

    blocks=0
    min_length=min(length1,length2)

#大块长度
    for i in range(0,min_length,block_size):
        if sample1[i:i+block_size] == sample2[i:i+block_size]:
            blocks+=1
        else:
            break

    #小字节长度
    input_try=b''
    length=blocks*block_size

#比较i和i+1次的结果
    for i in range(block_size):
        input_try+=b'w'
        now = encryption_oracle(input_try)[length:length+block_size]
        next = encryption_oracle(input_try+b'w')[length:length+block_size]
        if now == next :
            break

    res = block_size - len(input_try)
    return length+res


def ecb_decrypt(block_size):
  
    # common = lower_cases + upper_cases + space + numbers
    # to optimize brute-force approach
    common = list(range(ord('a'), ord('z'))) + list(range(ord('A'),
                                                          ord('Z'))) + [ord(' ')] + list(range(ord('0'), ord('9')))
    rare = [i for i in range(256) if i not in common]
    possibilities = bytes(common + rare)

    plaintext = b''  # holds the entire plaintext = sum of `found_block`'s
    check_length = block_size

    random_length = detect_random_length()
    print(f"Length of Random :{random_length}")
    check_begin = (random_length // block_size) * block_size
    res = random_length % block_size

    while True:
        # as more characters in the block are found, the number of A's to prepend decreases
        prepend = b'A' * (block_size - 1 - ((len(plaintext)+res) % block_size))
        actual = encryption_oracle(prepend)[check_begin:check_length+check_begin]

        found = False
        for byte in possibilities:
            value = bytes([byte])
            your_string = prepend + plaintext + value
            produced = encryption_oracle(your_string)[check_begin:check_begin+check_length]
            if actual == produced:
                plaintext += value
                found = True
                break

        if not found:
            print(f'Possible end of plaintext: No matches found.')
            print(f"Plaintext: \n{ plaintext.decode('ascii') }")
            return

        if (len(plaintext)+res) % block_size == 0:
            check_length += block_size


def main():
    # detect block size
    block_size = detect_block_size()
    print(f"Block Size is { block_size }")

    # detect the mode (should be ECB)
    repeated_plaintext = b"A" * 50
    cipher = encryption_oracle(repeated_plaintext)
    mode = detect_mode(cipher)
    print(f"Mode of encryption is { mode }")

    # decrypt the plaintext inside `encryption_oracle()`
    ecb_decrypt(block_size)


if __name__ == "__main__":
    main()
