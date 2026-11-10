"""Task 3.2 - Vigenere cipher, Romanian alphabet (n = 31)."""
from lab3_common import ALPHABET, N, ask_operation, ask_key, ask_text


def _codes(text, alphabet):
    pos = {letter: i for i, letter in enumerate(alphabet)}
    return [pos[ch] for ch in text]


def vigenere_encrypt(text, key, alphabet=ALPHABET):
    """c_i = (m_i + k_i) mod n, key repeated cyclically."""
    n = len(alphabet)
    m, k = _codes(text, alphabet), _codes(key, alphabet)
    return "".join(alphabet[(m[i] + k[i % len(k)]) % n]
                   for i in range(len(m)))


def vigenere_decrypt(text, key, alphabet=ALPHABET):
    """m_i = (c_i - k_i) mod n  (+ n keeps the value non-negative)."""
    n = len(alphabet)
    c, k = _codes(text, alphabet), _codes(key, alphabet)
    return "".join(alphabet[((c[i] - k[i % len(k)]) % n + n) % n]
                   for i in range(len(c)))


def main():
    print(f"Vigenere cipher - Romanian alphabet (n = {N})")
    print("Alphabet:", " ".join(f"{l}={i}" for i, l in enumerate(ALPHABET)))
    op = ask_operation()
    key = ask_key()
    if op == "E":
        text = ask_text("Message: ")
        print("Prepared text :", text)
        print("Key (upper)   :", key)
        print("Ciphertext    :", vigenere_encrypt(text, key))
    else:
        text = ask_text("Ciphertext: ")
        print("Prepared text :", text)
        print("Key (upper)   :", key)
        print("Decrypted text:", vigenere_decrypt(text, key))


if __name__ == "__main__":
    main()
