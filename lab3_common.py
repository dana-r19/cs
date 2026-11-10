"""Shared helpers for Laboratory Work No. 3 (polyalphabetic ciphers).

Romanian alphabet, n = 31, codes 0..30 taken ONLY from the position in
ALPHABET (A=0, Ă=1, Â=2, ... , Z=30).
"""
import unicodedata

ALPHABET = ["A", "Ă", "Â", "B", "C", "D", "E", "F", "G", "H", "I", "Î",
            "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "Ș", "T",
            "Ț", "U", "V", "W", "X", "Y", "Z"]
LOWERCASE = ["a", "ă", "â", "b", "c", "d", "e", "f", "g", "h", "i", "î",
             "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "ș", "t",
             "ț", "u", "v", "w", "x", "y", "z"]
N = len(ALPHABET)  # 31

# s/t with cedilla (ş ţ) are accepted as s/t with comma below (ș ț)
CEDILLA_FIX = {"Ş": "Ș", "ş": "ș", "Ţ": "Ț", "ţ": "ț"}
TO_UPPER = dict(zip(LOWERCASE, ALPHABET))
CODE = {letter: i for i, letter in enumerate(ALPHABET)}

MIN_KEY_LEN = 7
ALLOWED_HINT = ("letters A-Z, a-z (and the Romanian letters Ă Â Î Ș Ț / "
                "ă â î ș ț)")


def clean_char(ch):
    """Uppercase Romanian letter for ch, or None if ch is not a letter."""
    ch = CEDILLA_FIX.get(ch, ch)
    if ch in CODE:
        return ch
    return TO_UPPER.get(ch)


def prepare_text(raw, drop_spaces=True):
    """Uppercase the text, drop spaces. Returns (text, bad_char)."""
    raw = unicodedata.normalize("NFC", raw)
    out = []
    for ch in raw:
        if ch == " " and drop_spaces:
            continue
        letter = clean_char(ch)
        if letter is None:
            return None, ch
        out.append(letter)
    return "".join(out), None


# user input 
def ask_operation():
    while True:
        c = input("Operation - (E)ncrypt or (D)ecrypt: ").strip().lower()
        if c in ("e", "encrypt", "encryption"):
            return "E"
        if c in ("d", "decrypt", "decryption"):
            return "D"
        print("  Invalid choice. Type E for encryption or D for decryption.")


def ask_key(prompt=None):
    prompt = prompt or f"Key (at least {MIN_KEY_LEN} letters): "
    while True:
        key, bad = prepare_text(input(prompt).strip(), drop_spaces=False)
        if bad is not None:
            shown = "space" if bad == " " else f"'{bad}'"
            print(f"  Invalid character {shown} in the key. Allowed: "
                  f"{ALLOWED_HINT}; no spaces.")
            continue
        if len(key) < MIN_KEY_LEN:
            print(f"  Key too short ({len(key)} letters): it must have at "
                  f"least {MIN_KEY_LEN} letters.")
            continue
        return key


def ask_text(prompt):
    while True:
        text, bad = prepare_text(input(prompt))
        if bad is not None:
            print(f"  Invalid character '{bad}'. Allowed: {ALLOWED_HINT}; "
                  f"spaces are ignored.")
            continue
        if not text:
            print("  The text is empty. Enter at least one letter.")
            continue
        return text
