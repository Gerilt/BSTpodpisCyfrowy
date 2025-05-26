import os
import hashlib
import random
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding

def choose_rng_file():
    files = [f for f in os.listdir("binary") if f.endswith(('.bin', '.dat', '.exe'))]
    if not files:
        print("Brak plików binarnych w folderze 'binary'.")
        exit()
    print("Wybierz plik binarny jako RNG:")
    for i, f in enumerate(files):
        print(f"{i+1}. {f}")
    idx = int(input("Numer: ")) - 1
    return os.path.join("binary", files[idx])

def choose_file_to_sign():
    files = [f for f in os.listdir("to_sign") if os.path.isfile(os.path.join("to_sign", f))]
    if not files:
        print("Brak plików do podpisania w folderze 'to_sign'.")
        exit()
    print("Wybierz plik do podpisania:")
    for i, f in enumerate(files):
        print(f"{i+1}. {f}")
    idx = int(input("Numer: ")) - 1
    return os.path.join("to_sign", files[idx])

def get_seed_from_file(filepath):
    with open(filepath, "rb") as f:
        data = f.read()
    return int.from_bytes(hashlib.sha256(data).digest(), 'big')

def generate_rsa_key_from_seed(seed):
    random.seed(seed)
    return rsa.generate_private_key(public_exponent=65537, key_size=2048)

def sha3_file(filepath):
    h = hashlib.sha3_256()
    with open(filepath, "rb") as f:
        h.update(f.read())
    return h.digest()

def save_public_key_and_signature(public_key, signature):
    os.makedirs("keys", exist_ok=True)
    with open("keys/public_key.pem", "wb") as f:
        f.write(public_key.public_bytes(
            serialization.Encoding.PEM,
            serialization.PublicFormat.SubjectPublicKeyInfo
        ))
    with open("keys/signature.bin", "wb") as f:
        f.write(signature)

def main():
    rng_file = choose_rng_file()
    file_to_sign = choose_file_to_sign()

    seed = get_seed_from_file(rng_file)
    private_key = generate_rsa_key_from_seed(seed)
    public_key = private_key.public_key()

    hash_val = sha3_file(file_to_sign)

    signature = private_key.sign(
        hash_val,
        padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
        hashes.SHA256()
    )

    save_public_key_and_signature(public_key, signature)
    print(f"✅ Plik '{file_to_sign}' został podpisany.")
    print(f"📁 Podpis i klucz publiczny zapisane w folderze 'keys/'.")

if __name__ == "__main__":
    main()
#156178