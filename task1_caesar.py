"""Task 1.1 - Caesar cipher over the Romanian alphabet (n = 31)."""
from romanian_caesar import (ALPHABET, N, ask_operation, ask_key, ask_text,
                             encrypt, decrypt)


def main():
    print("Caesar cipher - Romanian alphabet (n = %d)" % N)
    print("Alphabet:", " ".join(ALPHABET))
    # Get the requested operation and shift amount.
    op = ask_operation()
    k = ask_key()   
    if op == "E":
        # ask_text validates and prepares the message before encryption.
        text = ask_text("Message: ")
        print("Prepared text :", text)
        print("Ciphertext    :", encrypt(text, k))
    else:
        # Prepare the ciphertext, then reverse the shift.
        text = ask_text("Ciphertext: ")
        print("Prepared text :", text)
        print("Decrypted text:", decrypt(text, k))


# Run the program only when this file is executed directly.
if __name__ == "__main__":
    main()
