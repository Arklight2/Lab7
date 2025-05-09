# firm/utils.py
import hashlib

def custom_hash(data, algorithm="sha256"):
    """
    Преобразует строку data в хеш фиксированной длины с использованием алгоритма MD5 или SHA256.
    """
    if algorithm.lower() == 'md5':
        h = hashlib.md5()
    elif algorithm.lower() == 'sha256':
        h = hashlib.sha256()
    else:
        raise ValueError("Unsupported algorithm")
    h.update(data.encode('utf-8'))
    return h.hexdigest()
