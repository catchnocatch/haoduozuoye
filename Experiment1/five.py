# import binascii
# from collections import Counter

# # Hex encoded string
# hex_string = "1934693d2c28353d272b63293f242c3d6324703425213420227e69212565273a202d2b653a273a3a632a3e37693d2a2b373e2c6e21293f213a212e65372026393065393c692f2f297026212b6328393e25272c2b2372282027653d3b25222a2a3e21692125652326283c3069703b3d6e2a3670372721362238723d21632831392c6e2b2c3d72212f33352972233b30317026266e2f2a3f39692f3765243a2c6e303131203a60630d35722a2f2d652333306e372a703a202330203c34656e64163f3f2c392b202237656e2e3c7034252134202272203d633138373b2b6d6b7e75690c3631703b2f6e372d35723a26262020722c2f37367026212b63233c3d3e2b3169703b276e2c2b357224212e203e26692f2f29703a203d633624333b3d6332393e256e21207036283c28203e372d606d6b7013272a633c3f27693a2b2c3e39693a2b242472203d632b3f2669272e353f203d2f2d3171"
# # Convert hex string to bytes
# cipher_bytes = binascii.unhexlify(hex_string)


# best_decryption = ""
# key = None

# for i in range(256):
#     decrypted = bytes(b ^ i for b in cipher_bytes)
#     try:
#         decrypted_text = decrypted.decode('ascii')
#     except UnicodeDecodeError:
#         continue

#     score = english_score(decrypted_text)
#     if score > best_score:
#         best_score = score
#         best_decryption = decrypted_text
#         key = i

# print(f"Key: {chr(key)}")
# print(f"Decrypted message: {best_decryption}")
