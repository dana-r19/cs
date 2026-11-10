"""Shared code for Laboratory Work No. 1 (Caesar cipher, Romanian alphabet).

Letter codes come ONLY from the position in ALPHABET (Table 2 of the lab
description). ord()/ASCII/Unicode code points are never used for the shift.
"""
import unicodedata

# Table 2: A=0, Ă=1, Â=2, ... , Z=30  (n = 31)
ALPHABET = ["A", "Ă", "Â", "B", "C", "D", "E", "F", "G", "H", "I", "Î",
            "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "Ș", "T",
            "Ț", "U", "V", "W", "X", "Y", "Z"]
LOWERCASE = ["a", "ă", "â", "b", "c", "d", "e", "f", "g", "h", "i", "î",
             "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "ș", "t",
             "ț", "u", "v", "w", "x", "y", "z"]
N = len(ALPHABET)  # 31

# s/t with CEDILLA (ş ţ) are treated as s/t with COMMA BELOW (ș ț)
CEDILLA_FIX = {"Ş": "Ș", "ş": "ș", "Ţ": "Ț", "ţ": "ț"}

# lowercase -> uppercase, built from the two parallel lists
TO_UPPER = dict(zip(LOWERCASE, ALPHABET))
# letter -> code (0..30)
CODE = {letter: i for i, letter in enumerate(ALPHABET)}

MIN_KEYWORD_LEN = 7


def clean_char(ch):
    """Return the uppercase Romanian letter for ch, or None if invalid."""
    ch = CEDILLA_FIX.get(ch, ch)
    if ch in CODE:
        return ch
    return TO_UPPER.get(ch)


def prepare_text(raw):
    """Uppercase the text and drop spaces.

    Returns (text, bad_char). bad_char is the first rejected character,
    or None when everything is valid.
    """
    # Combine Romanian diacritics into the same form used by ALPHABET.
    raw = unicodedata.normalize("NFC", raw)
    result = []
    for ch in raw:
        if ch == " ":
            continue
        letter = clean_char(ch)
        if letter is None:
            return None, ch
        result.append(letter)
    return "".join(result), None


def build_permuted_alphabet(keyword):
    """Keyword letters (first occurrences only) + remaining letters in order."""
    order = []
    # Keep each keyword letter once, preserving its first appearance.
    for letter in keyword:
        if letter not in order:
            order.append(letter)
    for letter in ALPHABET:
        if letter not in order:
            order.append(letter)
    return order


def encrypt(text, k, alphabet=ALPHABET):
    """c = (x + k) mod n, x = position in `alphabet`."""
    n = len(alphabet)
    # Shift alphabet positions rather than Unicode character codes.
    pos = {letter: i for i, letter in enumerate(alphabet)}
    return "".join(alphabet[(pos[ch] + k) % n] for ch in text)


def decrypt(text, k, alphabet=ALPHABET):
    """m = (y - k) mod n; the extra '+ n' keeps the value non-negative in
    languages whose % can return negatives."""
    n = len(alphabet)
    # Subtract the key to reverse encryption, wrapping around the alphabet.
    pos = {letter: i for i, letter in enumerate(alphabet)}
    return "".join(alphabet[((pos[ch] - k) % n + n) % n] for ch in text)



def ask_operation():
    """Prompt until the user selects encryption or decryption."""
    while True:
        choice = input("Operation - (E)ncrypt or (D)ecrypt: ").strip().lower()
        if choice in ("e", "encrypt", "encryption"):
            return "E"
        if choice in ("d", "decrypt", "decryption"):
            return "D"
        print("  Invalid choice. Type E for encryption or D for decryption.")


def ask_key():
    """Prompt for a valid Caesar shift key."""
    while True:
        raw = input(f"Key k (integer from 1 to {N - 1}): ").strip()
        try:
            k = int(raw)
        except ValueError:
            print(f"  Invalid key '{raw}': the key must be an integer "
                  f"between 1 and {N - 1}.")
            continue
        if 1 <= k <= N - 1:
            return k
        print(f"  Invalid key {k}: allowed values are 1 to {N - 1}.")


def ask_text(prompt):
    """Read and prepare non-empty text containing Romanian letters."""
    while True:
        text, bad = prepare_text(input(prompt))
        if bad is not None:
            print(f"  Invalid character '{bad}'. Only letters of the Romanian "
                  f"alphabet (and spaces) are allowed.")
            continue
        if not text:
            print("  The text is empty. Enter at least one letter.")
            continue
        return text


def ask_keyword():
    """Read an uppercase Romanian keyword of the required minimum length."""
    while True:
        raw = input(f"Keyword k2 (Romanian letters only, at least "
                    f"{MIN_KEYWORD_LEN} characters): ").strip()
        raw = unicodedata.normalize("NFC", raw)
        letters, bad = [], None
        for ch in raw:
            letter = clean_char(ch)
            if letter is None:
                bad = ch
                break
            letters.append(letter)
        if bad is not None:
            print(f"  Invalid character '{bad}' in the keyword. Only letters "
                  f"of the Romanian alphabet are allowed (no spaces).")
            continue
        if len(letters) < MIN_KEYWORD_LEN:
            print(f"  Keyword too short ({len(letters)} characters): it must "
                  f"have at least {MIN_KEYWORD_LEN} characters.")
            continue
        return "".join(letters)
