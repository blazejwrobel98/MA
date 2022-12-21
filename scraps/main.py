import random

from passlib.hash import md5_crypt


# create password generator for brute force
def password_generator(length):
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()_+"
    gen_password = ""
    for x in range(length):
        gen_password += random.choice(chars)
    return gen_password


# hash to crack
hash = "$1$D1lp$Go1x/jVF2eY8F8aJfJB4W."

# loop and verify hash vs. password
l = 0
while True:
    for i in range(1, 20):
        password = password_generator(i)
        if l % 1000 == 0:
            print(l)
        if md5_crypt.verify(password, hash):
            print("Password found: " + password)
            break
        l += 1
