import os
from io import BufferedReader
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import scrypt


_AUTH_TAG_BYTE_LEN = 16
_IV_BYTE_LEN = 12
_KEY_BYTE_LEN = 32

def _read_variables_file(environment = None):
    filename = f'{environment}.variables' if environment else 'variables'
    return open(f'.ev/{filename}', 'rb')

# returns a secret from a string using scrypt
def _get_secret(password):
    return scrypt(password, 'EV_SECRET_SALT', key_len=_KEY_BYTE_LEN, N=2**14, r=8, p=1)

# Decrypt file using AES-256-GCM
def _decrypt_file(content: BufferedReader, password: str = None, secret: bytes = None):
    content_bytes = content.read()
    # get the IV
    iv = content_bytes[:_IV_BYTE_LEN]
    # get the encrypted data, which comes after the IV and before the auth tag
    encrypted_data = content_bytes[_IV_BYTE_LEN:-_AUTH_TAG_BYTE_LEN]
    # get the auth tag
    auth_tag = content_bytes[-_AUTH_TAG_BYTE_LEN:]
    # decrypt
    cipher = AES.new(secret or _get_secret(password), AES.MODE_GCM, iv)
    try:
        decrypted_content = cipher.decrypt_and_verify(encrypted_data, auth_tag)
    except ValueError:
        raise Exception('Invalid secret')
    return decrypted_content.decode('utf-8')

def _parse_variables_file(content: str):
    return {
        line.split('=')[0]: line.split('=')[1].strip() 
        for line in content.split('\n') if line
    }

def _import_dict_to_env(dictionary: dict):
    for key, value in dictionary.items():
        os.environ[key] = value

def load_environment(environment: str = None, secret: str = None):
    variables_file = _read_variables_file(environment)
    secret_file = f'.ev/{environment}.secret' if environment else '.ev/secret'
    if secret:
        variables_content = _decrypt_file(variables_file, password=secret)
    elif os.path.isfile(secret_file):
        with open(secret_file, 'rb') as f:
            secret_content = f.read()
            variables_content = _decrypt_file(variables_file, secret=secret_content)
    elif os.getenv('EV_SECRET'):
        variables_content = _decrypt_file(variables_file, password=os.getenv('EV_SECRET'))
    else:
        raise Exception('No secret provided')
    variables = _parse_variables_file(variables_content)
    _import_dict_to_env(variables)