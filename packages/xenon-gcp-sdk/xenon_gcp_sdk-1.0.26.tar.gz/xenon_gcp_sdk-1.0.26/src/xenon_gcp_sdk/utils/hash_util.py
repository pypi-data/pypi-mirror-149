import hashlib


def string_fingerprint(s):
    hash_object = hashlib.sha256(s.encode('utf-8'))
    return hash_object.hexdigest()
