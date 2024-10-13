import string
import re
from operator import itemgetter, attrgetter
import base64

def compute_letter_frequency(text):
    frequency = {
        'a': .08167, 'b': .01492, 'c': .02782, 'd': .04253,
        'e': .12702, 'f': .02228, 'g': .02015, 'h': .06094,
        'i': .06094, 'j': .00153, 'k': .00772, 'l': .04025,
        'm': .02406, 'n': .06749, 'o': .07507, 'p': .01929,
        'q': .00095, 'r': .05987, 's': .06327, 't': .09056,
        'u': .02758, 'v': .00978, 'w': .02360, 'x': .00150,
        'y': .01974, 'z': .00074, ' ': .15000
    }
    return sum([frequency.get(chr(i), 0) for i in text.lower()])

def xor_with_single_char(data, char):
    result = b''
    for byte in data:
        result += bytes([byte ^ char])
    return result

def find_best_single_char_xor(data):
    results = []
    for char in range(256):
        decrypted = xor_with_single_char(data, char)
        score = compute_letter_frequency(decrypted)
        results.append({
            'character': char,
            'decrypted': decrypted,
            'score': score
        })
    best_result = sorted(results, key=lambda x: x['score'], reverse=True)[0]
    return best_result

def xor_with_repeating_key(ciphertext, key):
    plaintext = b''
    key_length = len(key)
    for i in range(len(ciphertext)):
        plaintext += bytes([ciphertext[i] ^ key[i % key_length]])
    return plaintext

def calculate_hamming_distance(a, b):
    distance = 0
    for byte1, byte2 in zip(a, b):
        xor_result = byte1 ^ byte2
        distance += bin(xor_result).count('1')
    return distance

def estimate_key_length(ciphertext):
    results = []
    for key_length in range(2, 41):
        blocks = [ciphertext[i:i + key_length] for i in range(0, len(ciphertext), key_length)]
        distances = []
        for i in range(len(blocks) - 1):
            distance = calculate_hamming_distance(blocks[i], blocks[i + 1]) / key_length
            distances.append(distance)
        average_distance = sum(distances) / len(distances)
        results.append({
            'key_length': key_length,
            'average_distance': average_distance
        })
    best_key_length = sorted(results, key=lambda x: x['average_distance'])[0]
    return best_key_length

def break_repeating_key_xor(ciphertext):
    estimated_key_length = estimate_key_length(ciphertext)['key_length']
    print(estimated_key_length)
    key = b''
    decrypted_message = b''
    blocks = [ciphertext[i:i + estimated_key_length] for i in range(0, len(ciphertext), estimated_key_length)]
    for i in range(estimated_key_length):
        combined_bytes = b''
        for block in blocks:
            if i < len(block):
                combined_bytes += bytes([block[i]])
        best_result = find_best_single_char_xor(combined_bytes)
        key += bytes([best_result['character']])
    for block in blocks:
        decrypted_message += xor_with_repeating_key(block, key)
    return decrypted_message, key

if __name__ == '__main__':
    with open('set6.txt') as file:
        encoded_ciphertext = file.read()
        ciphertext = base64.b64decode(encoded_ciphertext)
    message, key = break_repeating_key_xor(ciphertext)
    print("message:", bytes.decode(message), "\nkey:", bytes.decode(key))
