# ECC-Messaging-Scheme-Package
A system that encrypts and decrypts data packets with the elliptic curve cryptography (ECC) for others
to utilize and download.

## Where to download:
### typescript/javascript
https://www.npmjs.com/package/ecc-messaging-scheme-package

### Python
https://pypi.org/project/ecc-messaging-scheme-package/


## Classes
We have one main class, ECCM class, which combines our ECC class and our Encrypt/Decrypt, and
curve initialization(initializePublicEnv) functions.

The ECC Class:
-  Responsible for generating/loading private key
-  Get current users public key from cookies or create a new one and save
-  Gets shared key using diffie hellman when given another users public key
-  Clear cookies containing private key for current instance.

Encrypt/Decrypt:
-  Given a key and text it encrypts/decrypts text using AES

initializePublicEnv function:
-  Inizalites a point and an ecc curve: secp256k1


## Examples:
```
#Key exchange
C = initialize_public_env()
a_ecc_instance = ECC_Instance(C,'a')
a_ecc_instance.get_public_key()

b_ecc_instance = ECC_Instance(C,'b')
b_ecc_instance.get_public_key()

a_ecc_instance.generate_shared_key(b_ecc_instance.get_public_key())
b_ecc_instance.generate_shared_key(a_ecc_instance.get_public_key())

assert(a_ecc_instance.get_shared_key() == b_ecc_instance.get_shared_key())
#Share messages
key_b = a_ecc_instance.get_shared_key().x.to_bytes(24, byteorder='big')
plaintext = "test 12312 "
ciphertext,nonce = encrypt(key_b,plaintext)

plaintext_out = decrypt(key_b,ciphertext,nonce)

assert(plaintext==plaintext_out)
```

# Disclaimer
Use at Your Own Risk.
