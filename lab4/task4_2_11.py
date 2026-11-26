"""Lab 4, task 2.11 - from L16 and R16 to the encrypted DES block.

After round 16 DES swaps the halves (R16 L16) and applies the final
permutation IP^-1 (FP). The result, written in hexadecimal, is the
encrypted 64-bit block.

Input: L16 and R16 typed by the user, or generated randomly.
In random mode a random key and message block are encrypted with the full
DES, and the program checks that its answer equals the real ciphertext.
"""
import random
from des_core import (FP, des_encrypt_block, permute, bits_to_str,
                      bits_to_hex, bits_to_int, int_to_bits, hex_to_bits)


def print_table(title, table, cols):
    print(title)
    for i in range(0, len(table), cols):
        print("  " + " ".join(f"{v:2d}" for v in table[i:i + cols]))


def ask_mode():
    while True:
        c = input("Input data - (U)ser or (R)andom: ").strip().lower()
        if c in ("u", "user"):
            return "U"
        if c in ("r", "random"):
            return "R"
        print("  Invalid choice. Type U to enter the data or R for random.")


def ask_half(name):
    """32 bits, as 32 binary digits or as 8 hexadecimal digits."""
    while True:
        raw = input(f"{name} (32 bits as binary, or 8 hex digits): ")
        text = raw.replace(" ", "").upper()
        if len(text) == 32 and set(text) <= {"0", "1"}:
            return [int(c) for c in text]
        if len(text) == 8:
            try:
                return hex_to_bits(text, 32)
            except ValueError:
                pass
        if set(text) <= {"0", "1"} and text:
            print(f"  Invalid {name}: {len(text)} bits entered, 32 required "
                  f"(or exactly 8 hex digits).")
        else:
            print(f"  Invalid {name}: use only 0/1 (32 digits) or "
                  f"hexadecimal digits 0-9, A-F (8 digits).")


def random_case():
    key = [random.randint(0, 1) for _ in range(64)]
    block = [random.randint(0, 1) for _ in range(64)]
    l16, r16, cipher = des_encrypt_block(block, key)
    print("Random key        :", bits_to_hex(key))
    print("Random message    :", bits_to_hex(block), "(one 64-bit block)")
    return l16, r16, cipher


def main():
    print("DES - task 2.11: encrypted block from L16 and R16")
    mode = ask_mode()
    expected = None
    if mode == "U":
        l16 = ask_half("L16")
        r16 = ask_half("R16")
    else:
        l16, r16, expected = random_case()

    print()
    print("L16 =", bits_to_str(l16, 8), " =", bits_to_hex(l16))
    print("R16 =", bits_to_str(r16, 8), " =", bits_to_hex(r16))

    print()
    print("Step 1. After round 16 the halves are swapped: preoutput = R16 L16")
    pre = r16 + l16
    print("R16 L16 =", bits_to_str(pre, 8))

    print()
    print("Step 2. Final permutation IP^-1 (output bit j = preoutput bit FP[j])")
    print_table("FP table:", FP, 8)

    print()
    print("Bit-by-bit result (output position <- preoutput position : bit):")
    for row in range(8):
        cells = []
        for col in range(8):
            j = row * 8 + col
            cells.append(f"{j + 1:2d}<-{FP[j]:2d}:{pre[FP[j] - 1]}")
        print("  " + "  ".join(cells))

    cipher = permute(pre, FP)
    print()
    print("Step 3. Encrypted block")
    print("Binary :", bits_to_str(cipher, 8))
    print("Hex    :", bits_to_hex(cipher))
    if expected is not None:
        ok = expected == cipher
        print("Check  : full DES encryption of the message gives",
              bits_to_hex(expected), "->", "MATCH" if ok else "MISMATCH")


if __name__ == "__main__":
    main()
