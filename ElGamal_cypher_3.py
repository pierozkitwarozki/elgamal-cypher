import random
import math


def is_prime(number):
    if number > 1:
        for i in range(2, number):
            if number % i == 0:
                return False
        else:
            return True
    else:
        return False


def generate_random_p():
    p = random.randint(1000, 10000)
    while not is_prime(p):
        p = random.randint(1000, 10000)
    return p


def encode(text):
    for i in text:
        yield ord(i)


def mod_exp(base, exp, modulus):
    return pow(base, exp, modulus)


def generate_keys():
    p = generate_random_p()
    a = find_primitive(p)
    x = random.randint(1, p - 1)
    y = mod_exp(a, x, p)
    k = random.randint(1, p - 1)
    return {'public': (a, p, y),
            'private': x,
            'k_value': k}


def find_prime_factors(s, n):
    while n % 2 == 0:
        s.add(2)
        n = n // 2
    for i in range(3, int(math.sqrt(n)), 2):
        while n % i == 0:
            s.add(i)
            n = n // i
    if n > 2:
        s.add(n)


def find_primitive(n):
    s = set()
    if not is_prime(n):
        return -1
    phi = n - 1
    find_prime_factors(s, phi)
    for r in range(2, phi + 1):
        flag = False
        for it in s:
            if mod_exp(r, phi // it, n) == 1:
                flag = True
                break
        if not flag:
            return r
    return -1


def encrypt(key, message):
    encoded_msg = list(encode(message))
    pairs = []
    x = 1
    for item in encoded_msg:
        y = mod_exp(key['public'][0], key['k_value'], key['public'][1])
        z = item * (mod_exp(key['public'][2], key['k_value'], key['public'][1]))
        pairs.append((y, z))
        x += 1
    encrypted_msg_str = ''
    for i in pairs:
        encrypted_msg_str += str(i[0]) + str(i[1])
    return pairs, encrypted_msg_str


def decrypt(key, message):
    x = key['private']
    p = key['public'][1]
    decoded_msg = ''
    for item in message:
        first = item[0]
        second = item[1]
        m = (second * (first ** (p - 1 - x))) % p
        decoded_msg += str(chr(m))
    return decoded_msg


keys = generate_keys()

# input_text = input('Enter text to encrypt: ')
input_text = 'SzYfRRR'
encrypted_msg, encrypted_msg_str = encrypt(keys, input_text)
decrypted_msg = decrypt(keys, encrypted_msg)

print(f'You entered message: {input_text}')
print(f'Encrypted message: {encrypted_msg_str}')
print(f'Decrypted message: {decrypted_msg}')
