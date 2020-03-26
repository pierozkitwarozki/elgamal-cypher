import random
import math


def is_prime(number): # funkcja sprawdzająca czy liczba jest pierwsza
    if number > 1: # sprawdzam tylko jeśli jest większa od 1, inaczej False
        for i in range(2, number):
            if number % i == 0: #jeśli ma jakiś dzielnik mniejszy od samej siebie,  to False
                return False
        else:
            return True #jeśli nie ma żadnego dzielnika to True
    else:
        return False


def generate_random_p():
    p = random.randint(1000, 10000) #randomowe inty, ważne żeby były duże, dlatego od 1000 do 10000
    while not is_prime(p):
        p = random.randint(1000, 10000) #dopoki nie wygeneruje l. pierwszej to generuje dalej
    return p


def encode(text):# zamienianie kazdego znaku w ciągu na inta z tablicy ASCII, zeby potem
    # mozna było wykonywać na nich operacje matematyczne
    for i in text:
        yield ord(i) # yield to taki jakby return tylko dla każdej iteracji w pętli, nie zatrzymuje pętli


def mod_exp(base, exp, modulus):
    return pow(base, exp, modulus) # działanie: base ^ exp % modulus


def generate_keys(): #generowanie kluczy, to wykonywanie tych funkcji po prostu
    # pod tymi linkami co Ci wyslalem masz opisane jaka liczba ma byc jaka
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


def encrypt(key, message): # metoda szyfrująca
    encoded_msg = list(encode(message)) # tu zamieniam słowa na ascii
    pairs = [] # tu bede zapisywał pary zaszyfrowane
    x = 1
    k = key['k_value']
    p = key['public'][1]
    for item in encoded_msg: # dla każdego znaku takie działanie
        k = random.randint(1, p - 1)
        y = mod_exp(key['public'][0], k, p)
        z = item * (mod_exp(key['public'][2], k, p))
        pairs.append((y, z))
        x += 1
    encrypted_msg_str = ''
    for i in pairs: # łączę wszystkie pary w ciag liczb żeby się nie wyświetlało jak lista, tylko jak string
        encrypted_msg_str += str(i[0]) + str(i[1])
    return pairs, encrypted_msg_str  # zwracam listę par i ciąg do wyświetlenia


def decrypt(key, message): # no i metoda deszyfrująca, też wg wzoru z pliku który Ci wysłałem link,
    # ten z Bobem i Alicia chyba XDDD
    x = key['private']
    p = key['public'][1]
    decoded_msg = ''
    for item in message:
        first = item[0]
        second = item[1]
        m = (second * (first ** (p - 1 - x))) % p
        decoded_msg += str(chr(m)) # zamieniam z powrotem na stringa
    return decoded_msg


keys = generate_keys()

# input_text = input('Enter text to encrypt: ') jak odkomentujesz, i zakomentujesz to niżej,
# # to można wprowadzać tekst z klawiatury
input_text = 'SzyFRRRRRrrrr!!!!$$$'
encrypted_msg, encrypted_msg_str = encrypt(keys, input_text)
decrypted_msg = decrypt(keys, encrypted_msg)

print(f'You entered message: {input_text}')
print(f'Encrypted message: {encrypted_msg_str}')
print(f'Decrypted message: {decrypted_msg}')