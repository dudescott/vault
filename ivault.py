from Crypto.Cipher import AES
import sqlite3 as sql
# import clipboard
import os

BLOCK_SIZE = 16  # Bytes


def pad(s):
    return s + str((BLOCK_SIZE - len(s) %
                    BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE))


def unpad(s):
    return s[:-ord(s[len(s) - 1:])]


def encrypt(file, key):
    with open(file, 'rb') as f:
        msg = f.read()

    cipher = AES.new(key, AES.MODE_CBC)
    msg = cipher.encrypt(
        bytearray(pad(str(msg, encoding='utf-8')), encoding='utf-8'))

    with open(file + '.txt', "wb") as f:
        f.write(cipher.iv)
        f.write(msg)


def decrypt(file, key):
    with open(file, 'rb') as f:
        iv = f.read(16)
        msg = f.read()

    cipher = AES.new(key, AES.MODE_CBC, iv)
    msg = unpad(cipher.decrypt(msg))

    with open(file[:-4], "wb") as f:
        f.write(msg)


def get_key(path):
    with open(path, 'rb') as f:
        return f.read()


def retrieve(c, site):
    c.execute('select * from pwm where site == ?', (site,))
    cred = c.fetchall()
    if cred != []:
        clipboard.copy(cred[0][2])


def get_sites(c):
    c.execute('select site from pwm')
    sites = c.fetchall()
    print([site[0] for site in sites])


if __name__ == '__main__':
    option = ''
    while option.lower() != 'q':
        option = input("[E]ncrypt/[D]ecrypt/[R]etrieve/[Q]uit: ")
        if option.lower() in 'ed':
            db = input("enter db: ")
            key = input("enter key: ")
            key = get_key(key)
            if option.lower() == 'e':
                encrypt(db, key)
            elif option.lower() == 'd':
                decrypt(db, key)
        elif option.lower() == 'r':
            if os.path.exists('pwm.db'):
                conn = sql.connect('pwm.db')
                c = conn.cursor()
                site = input('Input site: ')
                if site.lower() == 'l':
                    get_sites(c)
                else:
                    retrieve(c, site)
