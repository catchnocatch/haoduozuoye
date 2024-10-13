import binascii
from collections import Counter

# Hex encoded string
hex_string = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"
# Convert hex string to bytes
cipher_bytes = binascii.unhexlify(hex_string)

# Frequency analysis for English language
def english_score(text):
    freq = Counter(text.lower())
    # Common letters in English (space, e, t, a, o, i, n, s, h, r)
    common_letters = 'etaoinshrdlcumwfgypbvkjxqz'
    score = sum(freq.get(char, 0) for char in common_letters)
    return score

# Brute-force decryption
best_score = -1
best_decryption = ""
key = None

for i in range(256):
    decrypted = bytes(b ^ i for b in cipher_bytes)
    try:
        decrypted_text = decrypted.decode('ascii')
    except UnicodeDecodeError:
        continue

    score = english_score(decrypted_text)
    if score > best_score:
        best_score = score
        best_decryption = decrypted_text
        key = i

print(f"Key: {chr(key)}")
print(f"Decrypted message: {best_decryption}")
