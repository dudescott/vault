from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import random
import pyperclip

def encrypt(file, key):
    with open(file, 'rb') as f:
        msg = f.read()

    cipher = AES.new(key, AES.MODE_CBC)
    msg = cipher.encrypt(pad(msg, AES.block_size))

    with open(file + '.vsa', "wb") as f:
        f.write(cipher.iv)
        f.write(msg)


def decrypt(file, key):
    with open(file, 'rb') as f:
        iv = f.read(16)
        msg = f.read()

    cipher = AES.new(key, AES.MODE_CBC, iv)
    msg = unpad(cipher.decrypt(msg), AES.block_size)

    with open(file[:-4], "wb") as f:
        f.write(msg)


def get_key(path):
    with open(path, 'rb') as f:
        return f.read()

def gen_password():
    DIGITS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] 
    LOCASE_CHARACTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
                        'i', 'j', 'k', 'm', 'n', 'o', 'p', 'q',
                        'r', 's', 't', 'u', 'v', 'w', 'x', 'y',
                        'z']
    UPCASE_CHARACTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
                        'I', 'J', 'K', 'M', 'N', 'O', 'p', 'Q',
                        'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y',
                        'Z']
    SYMBOLS = ['@', '#', '$', '%', '=', ':', '?', '.', '/', '|', '~', '>',
            '*', '(', ')', '<']
    COMBINED_LIST = DIGITS + UPCASE_CHARACTERS + LOCASE_CHARACTERS + SYMBOLS
    
    rand_digit = random.choice(DIGITS)
    rand_upper = random.choice(UPCASE_CHARACTERS)
    rand_lower = random.choice(LOCASE_CHARACTERS)
    rand_symbol = random.choice(SYMBOLS)

    password = [rand_digit , rand_upper , rand_lower ,rand_symbol]
    
    for _ in range(18 - 4):
        password.append(random.choice(COMBINED_LIST))
        random.shuffle(password)

    password_str = ""
    for char in password:
            password_str += char
    pyperclip.copy(password_str)
    return password_str

def vault(option, file, key):
    if key != '':
        key = get_key(key)
    if option.lower() == 'e':
        encrypt(file, key)
    elif option.lower() == 'd':
        decrypt(file, key)
    elif option.lower() == 'p':
      return gen_password()