from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.exceptions import InvalidSignature
import os

# === 1. GENEROWANIE KLUCZY I ZAPIS DO PLIKÓW ===
def generate_keys():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()

    # Zapis klucza prywatnego
    with open("private_key.pem", "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ))

    # Zapis klucza publicznego
    with open("public_key.pem", "wb") as f:
        f.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))
    print("🔐 Klucze zapisane do plików.")

# === 2. PODPISYWANIE WIADOMOŚCI ===
def sign_message(message: bytes):
    with open("private_key.pem", "rb") as f:
        private_key = serialization.load_pem_private_key(f.read(), password=None)

    digest = hashes.Hash(hashes.SHA3_256())
    digest.update(message)
    hash_val = digest.finalize()

    signature = private_key.sign(
        hash_val,
        padding.PKCS1v15(),
        hashes.SHA3_256()
    )

    with open("signature.bin", "wb") as f:
        f.write(signature)
    print("✍️ Podpis zapisany do pliku signature.bin.")

# === 3. WERYFIKACJA PODPISU ===
def verify_signature(message: bytes):
    with open("public_key.pem", "rb") as f:
        public_key = serialization.load_pem_public_key(f.read())
    with open("signature.bin", "rb") as f:
        signature = f.read()

    digest = hashes.Hash(hashes.SHA3_256())
    digest.update(message)
    hash_val = digest.finalize()

    try:
        public_key.verify(
            signature,
            hash_val,
            padding.PKCS1v15(),
            hashes.SHA3_256()
        )
        print("✅ Podpis jest prawidłowy.")
    except InvalidSignature:
        print("❌ Podpis nieprawidłowy.")

# === 4. DEMO ===
if __name__ == "__main__":
    message = "To jest oryginalna wiadomość.".encode('utf-8')

    if not (os.path.exists("private_key.pem") and os.path.exists("public_key.pem")):
        generate_keys()

    sign_message(message)
    verify_signature(message)

    # Modyfikacja wiadomości do testu błędnego podpisu:
    modified = "To jest zmodyfikowana wiadomość.".encode('utf-8')
    print("\n🔍 Weryfikacja zmodyfikowanej wiadomości:")
    verify_signature(modified)
