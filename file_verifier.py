import os
import hashlib
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

def sha3_file(filepath):
    h = hashlib.sha3_256()
    with open(filepath, "rb") as f:
        h.update(f.read())
    return h.digest()

def list_all_files():
    files = []
    mapping = {}
    idx = 1

    # Pliki z folderu to_sign/
    for fname in sorted(os.listdir("to_sign")):
        path = os.path.join("to_sign", fname)
        if os.path.isfile(path):
            files.append(f"({idx}) {fname}")
            mapping[idx] = path
            idx += 1

    # Pliki z folderu fake/
    if os.path.isdir("fake"):
        for fname in sorted(os.listdir("fake")):
            path = os.path.join("fake", fname)
            if os.path.isfile(path):
                files.append(f"({idx}) {fname}  [FAKE]")
                mapping[idx] = path
                idx += 1

    return files, mapping

def main():
    print("Pliki dostępne do weryfikacji:")
    files, mapping = list_all_files()
    if not files:
        print("❌ Brak plików do weryfikacji.")
        return

    for line in files:
        print(line)

    try:
        idx = int(input("Wybierz numer pliku do weryfikacji: "))
        file_path = mapping[idx]
    except (ValueError, KeyError):
        print("❌ Nieprawidłowy numer.")
        return

    try:
        hash_val = sha3_file(file_path)

        with open("keys/public_key.pem", "rb") as f:
            public_key = serialization.load_pem_public_key(f.read())

        with open("keys/signature.bin", "rb") as f:
            signature = f.read()

        public_key.verify(
            signature,
            hash_val,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        print(f"✅ Plik '{file_path}' — podpis prawidłowy.")
    except FileNotFoundError as e:
        print(f"❌ Brakuje pliku: {e.filename}")
    except Exception:
        print(f"❌ Plik '{file_path}' — podpis nieprawidłowy.")

if __name__ == "__main__":
    main()
#156178