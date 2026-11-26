"""Checks des_core against known DES test vectors."""
import random
from des_core import *

# Classic worked example (Grabbe, "The DES Algorithm Illustrated")
key = hex_to_bits("133457799BBCDFF1", 64)
pt = hex_to_bits("0123456789ABCDEF", 64)
k_plus, cd, keys = key_schedule(key)
assert bits_to_str(k_plus) == ("1111000 0110011 0010101 0101111 "
                               "0101010 1011001 1001111 0001111"
                               ).replace(" ", "")
assert bits_to_str(keys[0]) == "000110110000001011101111111111000111000001110010"
assert bits_to_str(keys[15]) == "110010110011110110001011000011100001011111110101"
l16, r16, ct = des_encrypt_block(pt, key)
assert bits_to_hex(l16) == "43423234" and bits_to_hex(r16) == "0A4CD995"
assert bits_to_hex(ct) == "85E813540F0AB405"

# FIPS known answers
for k, p, c in [("0101010101010101", "8000000000000000", "95F8A5E5DD31D900"),
                ("0123456789ABCDEF", "1111111111111111", "17668DFC7292532D"),
                ("133457799BBCDFF1", "0123456789ABCDEF", "85E813540F0AB405")]:
    out = des_encrypt_block(hex_to_bits(p, 64), hex_to_bits(k, 64))[2]
    assert bits_to_hex(out) == c, (k, p, bits_to_hex(out))

for _ in range(500):
    k = [random.randint(0, 1) for _ in range(64)]
    p = [random.randint(0, 1) for _ in range(64)]
    c = des_encrypt_block(p, k)[2]
    assert des_decrypt_block(c, k) == p
print("DES tests OK")

try:   # optional cross-check with an independent library
    from Crypto.Cipher import DES
    for _ in range(200):
        kb, pb = random.randbytes(8), random.randbytes(8)
        mine = bits_to_int(des_encrypt_block(int_to_bits(int.from_bytes(pb, "big"), 64),
                                             int_to_bits(int.from_bytes(kb, "big"), 64))[2])
        assert mine.to_bytes(8, "big") == DES.new(kb, DES.MODE_ECB).encrypt(pb)
    print("cross-check with pycryptodome OK")
except ImportError:
    pass
