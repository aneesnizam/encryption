ENCRYPTION AND DECRYPTION TOOL

This application is a comprehensive encryption and decryption tool that allows users to secure their messages using various classical cryptographic algorithms.

Features
Vernam Cipher

Rail Fence Cipher

Caesar Cipher

Columnar Transposition Cipher

Vigenère Cipher

Atbash Cipher

Playfair Cipher

The app provides an intuitive interface for users to encode and decode their messages securely.

Algorithms
Vernam Cipher
A symmetric cipher that uses a one-time pad. The encryption and decryption are performed by XORing the text with the key.

Rail Fence Cipher
A transposition cipher that arranges text in a zigzag pattern and reads it row by row.

Caesar Cipher
A substitution cipher that shifts each character by a fixed number of positions in the alphabet.

Columnar Transposition Cipher
A transposition cipher that rearranges the plaintext into a grid and reads it column by column.

Vigenère Cipher
A polyalphabetic substitution cipher using a keyword to determine the shifts for each letter.

Atbash Cipher
A substitution cipher where each letter is replaced with its reverse counterpart in the alphabet.

Playfair Cipher
A digraph substitution cipher that encrypts pairs of letters using a 5x5 key square.

Installation

Step 1: Clone the Repository
git clone https://github.com/aneesnizam/encryption.git
cd encryption-app

Step 2: Create and Activate Virtual Environment

For Windows (PowerShell):
python -m venv encenv
encenv\Scripts\activate

For macOS/Linux:
python -m venv encenv
source encenv/bin/activate

Step 3: Install Dependencies
pip install -r requirements.txt

Step 4: Run the Application
python manage.py runserver
