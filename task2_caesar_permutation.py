"""Task 1.2 - Caesar cipher with two keys (shift + keyword permutation)."""
from romanian_caesar import (ALPHABET, N, ask_operation, ask_key, ask_keyword,
                             ask_text, build_permuted_alphabet, encrypt,
                             decrypt)


def main():
    print("Caesar cipher with permutation - Romanian alphabet (n = %d)" % N)
    op = ask_operation()
    k1 = ask_key()
    k2 = ask_keyword()
    # Put unique keyword letters first, followed by the remaining alphabet.
    perm = build_permuted_alphabet(k2)
    print("Keyword (upper):", k2)
    print("Plain alphabet   :", " ".join(ALPHABET))
    print("Permuted alphabet:", " ".join(perm))
    if op == "E":
        # Shift letters by k1 positions in the permuted alphabet.
        text = ask_text("Message: ")
        print("Prepared text :", text)
        print("Ciphertext    :", encrypt(text, k1, perm))
    else:
        # Reverse the same shift to recover the prepared message.
        text = ask_text("Ciphertext: ")
        print("Prepared text :", text)
        print("Decrypted text:", decrypt(text, k1, perm))


# Run the program only when this file is executed directly.
if __name__ == "__main__":
    main()
