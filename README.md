# 🔐 System podpisu cyfrowego RSA

Projekt realizuje podpis cyfrowy RSA na podstawie wybranego pliku binarnego jako źródła entropii (RNG). Dzięki temu nie trzeba przechowywać klucza prywatnego — można go deterministycznie odtworzyć.

## 📁 Struktura folderów

```
BSTpodpisCyfrowy/
├── binary/           # Pliki binarne (np. aes.bin) używane jako RNG do RSA
├── fake/             # Fałszywe pliki do testowania weryfikacji (oznaczane [FAKE])
├── keys/             # Wygenerowany podpis (signature.bin) i klucz publiczny
├── to_sign/          # Pliki, które można podpisać
├── file_signer.py    # Program do podpisywania
├── file_verifier.py  # Program do weryfikacji podpisu
```

## 🛠️ Wymagania

Python 3.8+  
Zainstaluj wymagane biblioteki:

```bash
pip install cryptography
```

## ✍️ Podpisywanie pliku (`file_signer.py`)

1. Uruchom:
   ```bash
   python file_signer.py
   ```
2. Wybierz plik binarny z `binary/`, który posłuży jako RNG.
3. Wybierz plik do podpisania z folderu `to_sign/`.

➡️ Program:
- Obliczy SHA3-256 pliku,
- Wygeneruje deterministyczny klucz RSA z pliku binarnego,
- Podpisze hash,
- Zapisze `keys/signature.bin` i `keys/public_key.pem`.

## ✅ Weryfikacja podpisu (`file_verifier.py`)

1. Uruchom:
   ```bash
   python file_verifier.py
   ```
2. Z listy wybierz plik:
   - z `to_sign/` – oryginał,
   - z `fake/` – fałszywy plik (oznaczony `[FAKE]`).

➡️ Program:
- Obliczy hash wybranego pliku,
- Wczyta podpis i klucz z `keys/`,
- Sprawdzi poprawność podpisu.

## 🔄 Przykład działania

```
Pliki dostępne do weryfikacji:
(1) dokument.pdf
(2) dokument.pdf  [FAKE]
Wybierz numer pliku do weryfikacji: 1
✅ Plik 'to_sign/dokument.pdf' — podpis prawidłowy.
```

## ℹ️ Uwagi

- Prywatny klucz RSA nie jest zapisywany — można go odtworzyć używając tego samego pliku binarnego z `binary/`.
- Fałszywe pliki w `fake/` służą do testów odporności systemu.



156178