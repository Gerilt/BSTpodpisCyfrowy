
# 📄 Podpis cyfrowy RSA + SHA3

## 📌 Opis
Ten projekt demonstruje, jak za pomocą **RSA** oraz skrótu **SHA3-256**:
- Generować parę kluczy (prywatny/publiczny).
- Tworzyć **podpis cyfrowy** wiadomości.
- Weryfikować podpis cyfrowy.
- Zabezpieczać autentyczność przesyłanych danych.

## 🛠️ Wymagania

Zainstaluj bibliotekę `cryptography`:
```bash
pip install cryptography
```

## 📂 Struktura plików

| Plik                | Opis                                 |
|---------------------|--------------------------------------|
| `main.py`           | Główny program podpisujący i weryfikujący wiadomości |
| `private_key.pem`   | Klucz prywatny (generowany automatycznie) |
| `public_key.pem`    | Klucz publiczny (generowany automatycznie) |
| `signature.bin`     | Plik z podpisem cyfrowym wiadomości |
| `README.md`         | Dokumentacja projektu |

## ▶️ Jak uruchomić?

1. Uruchom program:
```bash
python main.py
```

2. Program wykona:
- Generację kluczy (jeśli ich nie ma).
- Podpisanie wiadomości `"To jest oryginalna wiadomość."`.
- Weryfikację podpisu.
- Test niepoprawnej wiadomości.

## ✅ Przykład działania

```
🔐 Klucze zapisane do plików.
✍️ Podpis zapisany do pliku signature.bin.
✅ Podpis jest prawidłowy.

🔍 Weryfikacja zmodyfikowanej wiadomości:
❌ Podpis nieprawidłowy.
```

## 🔒 Uwaga

**Nie udostępniaj `private_key.pem`** – ten plik powinien być bezpiecznie przechowywany.
