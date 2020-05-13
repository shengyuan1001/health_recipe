import hashlib


def make_password(pwd_str):
    return hashlib.md5(('@&$blog' + pwd_str + 'blog$&@').encode()).hexdigest()
