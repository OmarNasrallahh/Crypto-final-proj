# Crypto Toolkit

A comprehensive cryptography toolkit built for educational purposes that demonstrates modern encryption, decryption, encoding, decoding, and hashing techniques.

---

## Overview

This project was developed as part of a Cryptography course project. The toolkit provides implementations of several important cryptographic algorithms and encoding methods through an easy-to-use application.

The project demonstrates both symmetric and asymmetric cryptography concepts, along with hashing and data encoding techniques.

---

## Features

### Symmetric Encryption

* AES Encryption & Decryption
* DES Encryption & Decryption
* Triple DES (3DES) Encryption & Decryption

### Asymmetric Encryption

* RSA Key Generation
* RSA Encryption & Decryption

### Encoding & Decoding

* Base64 Encoding / Decoding
* Hex Encoding / Decoding
* URL Encoding / Decoding

### Hashing

* SHA-256 Hashing
* SHA-512 Hashing
* Salted SHA-256 Hashing

---

## Algorithms Used

### AES (Advanced Encryption Standard)

AES is a secure symmetric encryption algorithm widely used worldwide.

* Block Size: 128-bit
* Key Sizes: 128 / 192 / 256-bit
* Secure and industry standard

### DES (Data Encryption Standard)

DES is a legacy symmetric cipher included for educational comparison.

* Block Size: 64-bit
* Key Size: 56-bit
* Considered insecure today

### 3DES (Triple DES)

An improved version of DES that applies encryption three times.

* Key Size: 112 / 168-bit
* More secure than DES

### RSA

RSA is a public-key cryptosystem used for secure communication.

* 2048-bit key generation
* Public & Private key encryption system

### SHA-256 / SHA-512

Secure hashing algorithms used for integrity verification and password hashing.

---

## Project Structure

```bash
Crypto Project/
│
├── index.html
├── style.css
├── script.js
├── assets/
├── screenshots/
└── README.md
```

---

## Technologies Used

* HTML5
* CSS3
* JavaScript
* CryptoJS
* JSEncrypt

---

## Installation

Clone the repository:

```bash
git clone https://github.com/your-username/crypto-toolkit.git
cd crypto-toolkit
```

Open the project:

```bash
Open index.html in your browser
```

Or run using VS Code Live Server.

---

## Usage Examples

### AES Encryption

Input:

```text
Hello, Cryptography!
```

Key:

```text
mysecretkey123
```

Output:

```text
U2FsdGVkX1+...
```

---

### RSA Encryption

Input:

```text
Secret Message
```

Output:

```text
Encrypted Base64 Ciphertext
```

---

### SHA-256 Hash

Input:

```text
password123
```

Output:

```text
ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f
```

---

## Learning Objectives

This project helps students understand:

* Symmetric vs Asymmetric encryption
* Public & Private key cryptography
* Secure hashing techniques
* Encoding vs Encryption
* Modern cryptographic standards

---

## Screenshots

Add screenshots here.

```md
![AES Encryption](screenshots/aes.png)
```

---

## Future Improvements

* Add file encryption support
* Add drag & drop interface
* Improve UI/UX design
* Add more hashing algorithms
* Add password strength analysis

---

## Team Members

* Mahmoud Mostafa Foad
* Omar Nasrallah Saad
* Omar Ramy
* Mamdouh Mohamed
* Mohamed Ibrahim Aboyoussef

---

## Course Information

* Course: Cryptography


---

## License

This project is for educational and academic purposes.
