import os
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


def derive_key(shared_secret):
    # Transforme la clé ECDH brute en une clé AES-256 sécurisée grâce à HKDF.
    hkdf = HKDF(algorithm=hashes.SHA256(),
        length=32,          # clé AES-256
        salt=None,
        info=b'chat-app')
    return hkdf.derive(shared_secret)

def encrypt_message(key, plaintext, aad=None):
    # Chiffre le message en AES-GCM en générant un IV et un tag d’authentification.
    iv = os.urandom(12)
    cipher = Cipher(algorithms.AES(key), modes.GCM(iv))
    encryptor = cipher.encryptor()

    if aad:
        encryptor.authenticate_additional_data(aad) 
        
    ciphertext = encryptor.update(plaintext.encode()) + encryptor.finalize()
    return iv, ciphertext, encryptor.tag

def decrypt_message(key, iv, ciphertext, tag):
    # Déchiffre le message AES-GCM en utilisant la même clé, l’IV et le tag.
    cipher = Cipher(algorithms.AES(key), modes.GCM(iv, tag))
    decryptor = cipher.decryptor()
    return decryptor.update(ciphertext) + decryptor.finalize()
