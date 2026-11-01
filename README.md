# 🔐 CipherVault – Educational Encryption & Decryption Toolkit

An educational encryption and decryption application built for the **DecodeLabs Cybersecurity Internship – Project 2**. CipherVault demonstrates fundamental cryptographic concepts through interactive tools and lessons.

> ⚠️ **Security Disclaimer:** The Caesar and Vigenère ciphers implemented here are **classical ciphers suitable only for educational purposes**. They provide no security against modern cryptanalysis. Never use them to protect sensitive information.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| **Caesar Cipher** | Shift-based monoalphabetic substitution with customizable shift |
| **Vigenère Cipher** | Keyword-based polyalphabetic substitution |
| **Encrypt / Decrypt Workspace** | Full-featured I/O with algorithm selection and key input |
| **Verification** | Round-trip verification (encrypt → decrypt → compare) |
| **Brute Force Lab** | Try all 25 Caesar shifts — educational demonstration |
| **Frequency Analysis** | Character distribution stats and bar chart |
| **File Encryption** | Upload, encrypt/decrypt, and download `.txt` files |
| **Operation History** | Session-based log (no plaintext/keys stored) |
| **Learn Cryptography** | Interactive lessons on encryption fundamentals |
| **Input Validation** | Graceful handling of empty inputs, invalid keys, bad files |

---

## 🛠️ Technologies

- **Python 3.10+**
- **Streamlit** — interactive web UI
- **Standard Library** — `collections`, `datetime`, `unittest`
- No external APIs or network dependencies

---

## 📂 Project Structure

```
CipherVault/
│
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── README.md               # This file
├── PROJECT_STATUS.md        # Task tracking
├── PROJECT_NOTES.md         # Architecture decisions
│
├── algorithms/
│   ├── __init__.py
│   ├── caesar.py           # Caesar cipher (encrypt, decrypt, brute force)
│   ├── vigenere.py          # Vigenère cipher (encrypt, decrypt)
│   └── analysis.py          # Character frequency analysis
│
├── utils/
│   ├── __init__.py
│   ├── validators.py        # Input validation
│   ├── file_handler.py      # File I/O helpers
│   └── history.py           # Operation history manager
│
└── tests/
    ├── test_caesar.py       # Caesar cipher tests (17 tests)
    ├── test_vigenere.py      # Vigenère cipher tests (10 tests)
    └── test_validation.py    # Input validation tests (15 tests)
```

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.10 or higher
- pip (Python package manager)

### Steps (Windows Command Prompt)

```cmd
cd C:\Users\HP\Desktop\Hustle\Decodelabs-Internship\Project#02

pip install -r requirements.txt

python -m streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`.

---

## 📖 Usage

### Encrypting Text (Caesar)
1. Navigate to **🔒 Encrypt / Decrypt**
2. Select **Caesar Cipher**
3. Set the **Shift Value** (e.g., 3)
4. Enter your message in the input area
5. Click **🔒 Encrypt**
6. View and copy the ciphertext

### Decrypting Text (Vigenère)
1. Navigate to **🔒 Encrypt / Decrypt**
2. Select **Vigenère Cipher**
3. Enter the **Keyword** used during encryption
4. Paste the ciphertext
5. Click **🔓 Decrypt**

### Example

| Operation | Algorithm | Key | Input | Output |
|-----------|-----------|-----|-------|--------|
| Encrypt | Caesar | Shift 3 | `HELLO WORLD` | `KHOOR ZRUOG` |
| Decrypt | Caesar | Shift 3 | `KHOOR ZRUOG` | `HELLO WORLD` |
| Encrypt | Vigenère | `KEY` | `HELLO` | `RIJVS` |
| Decrypt | Vigenère | `KEY` | `RIJVS` | `HELLO` |

---

## 🧪 Running Tests

```cmd
python -m unittest discover -s tests -v
```

All 42 tests should pass, covering:
- Caesar encryption/decryption (shifts 0, 3, 26, negative, > 26)
- Case preservation and punctuation handling
- Vigenère encryption/decryption with keyword validation
- Round-trip verification for both algorithms
- Input validation (empty, invalid, edge cases)

---

## ⚠️ Security Disclaimer

This project is built for **educational purposes only** as part of the DecodeLabs Cybersecurity Internship.

- Caesar and Vigenère ciphers are **historically significant** but **cryptographically broken**
- The Caesar cipher has only 25 possible keys — trivially brute-forced
- The Vigenère cipher is vulnerable to the Kasiski examination and frequency analysis
- **Never use classical ciphers to protect sensitive information**
- Modern encryption (AES, RSA, ChaCha20) should be used for real security needs

---

## 📜 License

Educational project — DecodeLabs Cybersecurity Internship, Project 2.
