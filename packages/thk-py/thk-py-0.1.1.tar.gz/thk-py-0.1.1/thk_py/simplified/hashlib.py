# -*- coding: utf-8 -*-
import hashlib


def _hash_method(instance, raw: str) -> str:
    instance.update(raw.encode('utf-8'))
    return instance.hexdigest()


def hash_md5(raw: str) -> str:
    return _hash_method(hashlib.md5(), raw)


def hash_sha1(raw: str) -> str:
    return _hash_method(hashlib.sha1(), raw)


def hash_sha256(raw: str) -> str:
    return _hash_method(hashlib.sha256(), raw)


def hash_sha384(raw: str) -> str:
    return _hash_method(hashlib.sha384(), raw)


def hash_sha512(raw: str) -> str:
    return _hash_method(hashlib.sha512(), raw)
