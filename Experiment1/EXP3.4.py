# -*- coding:utf-8 -*-
CHARACTER_FREQ = {
    'a': 0.0651738, 'b': 0.0124248, 'c': 0.0217339, 'd': 0.0349835,
    'e': 0.1041442, 'f': 0.0197881, 'g': 0.0158610, 'h': 0.0492888,
    'i': 0.0558094, 'j': 0.0009033, 'k': 0.0050529, 'l': 0.0331490,
    'm': 0.0202124, 'n': 0.0564513, 'o': 0.0596302, 'p': 0.0137645,
    'q': 0.0008606, 'r': 0.0497563, 's': 0.0515760, 't': 0.0729357,
    'u': 0.0225134, 'v': 0.0082903, 'w': 0.0171272, 'x': 0.0013692,
    'y': 0.0145984, 'z': 0.0007836, ' ': 0.1918182
}

def get_score(text):

    return sum(CHARACTER_FREQ.get(ch.lower(), 0) for ch in text)

def single_byte_xor(key, text):

    return ''.join(chr(key ^ byte) for byte in text)

def find_best_candidate(text):

    best_result = {'key': 0, 'plaintext': '', 'score': 0}
    for key in range(256):
        plaintext = single_byte_xor(key, text)
        score = get_score(plaintext)
        if score > best_result['score']:
            best_result = {'key': key, 'plaintext': plaintext, 'score': score}
    return best_result

if __name__ == '__main__':
    file_path = 'challenge4.txt'
    candidates = []
    
    with open(file_path, 'r') as f:
        hex_lines = f.readlines()
    
    for line in hex_lines:
        line = line.strip()
        string = bytes.fromhex(line)  # Decode hex string
        candidates.append(find_best_candidate(string))

    best_candidate = max(candidates, key=lambda c: c['score'])
    print(best_candidate['plaintext'])  # Print the plaintext with the highest score