import random
import math


def is_prime(number):
    # sprawdzanie czy liczba jest pierwsza
    if number > 1:  # sprawdzam tylko jeśli jest większa od 1
        for i in range(2, number):
            if number % i == 0:  # jeśli ma jakiś dzielnik mniejszy od samej siebie, to funkcja się kończy i zwraca False
                return False
        else:  # jeśli pętla się skończy bez przerwania (nie ma żadnego dzielnika) tzn że liczba jest pierwsza i True
            return True
    else:
        return False


def generate_random_p():
    p = random.randint(1000, 10000)  # tu generuję randomowe inty od 1000 do 10000
    while not is_prime(p):
        p = random.randint(1000, 10000)  # dopóki nie wygeneruje liczby pierwszej to losuje dalej
    return p


def encode(text):
    for i in text:
        yield ord(i)


def mod_exp(base, exp, modulus):
    return pow(base, exp, modulus)  # działanie: base ^ exp % modulus


def generate_keys():  # generowanie kluczy
    p = generate_random_p()
    a = find_primitive(p)
    x = random.randint(1, p - 1)
    y = mod_exp(a, x, p)
    k = random.randint(1, p - 1)
    return {'public': (a, p, y),
            'private': x,
            'k_value': k}


def encrypt(key, message):
    encoded_msg = list(encode(message))
    pairs = []
    x = 1
    for item in encoded_msg:
        y = mod_exp(key['public'][0], key['k_value'], key['public'][1])
        z = item * (mod_exp(key['public'][2], key['k_value'], key['public'][1]))
        pairs.append((y, z))
        x += 1
    return pairs


def decrypt(key, message):
    x = key['private']
    p = key['public'][1]
    decoded_msg = ''
    for item in message:
        first = item[0]  # 28
        second = item[1]  # 9
        # m = (second * (pow(first, p-1-x)))%p
        m = (second * (first ** (p - 1 - x))) % p
        decoded_msg += str(chr(m))
    return decoded_msg


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


keys = generate_keys()

input_text = input('Enter text to encrypt: ')
encrypted_msg = encrypt(keys, input_text)
decrypted_msg = decrypt(keys, encrypted_msg)

for i in encrypted_msg:
    encrypted_msg = ''.join(str(i[0]) + str(i[1]))

print(f'Encrypted message: {encrypted_msg}')
print(f'Decrypted message: {decrypted_msg}')