"""
Copyright (c) 2022 Plugin Andrey (9keepa@gmail.com)
Licensed under the MIT License
"""
import logging
import hmac
import base64
import os
import hashlib


def log(name, filename=None):
    # создаём logger
    logger = logging.getLogger(name)
    logger.setLevel( logging.DEBUG )
    logger.propagate = False

    # создаём консольный handler и задаём уровень
    if filename:
        ch = logging.FileHandler(filename)
    else:
        ch = logging.StreamHandler()

    ch.setLevel(logging.DEBUG)

    # создаём formatter
    formatter = logging.Formatter('%(asctime)s : %(lineno)d : %(name)s : %(levelname)s : %(message)s')
    # %(lineno)d :
    # добавляем formatter в ch
    ch.setFormatter(formatter)

    # добавляем ch к logger
    logger.addHandler(ch)

    # logger.debug('debug message')
    # logger.info('info message')
    # logger.warn('warn message')
    # logger.error('error message')
    # logger.critical('critical message')
    return logger


def create_signature(secret: bytes,
                     message: bytes, algorithm: str = "sha512") -> bytes:
    sign = hmac.digest(secret, message, digest=algorithm)
    return base64.b64encode(sign)


def listdir_fullpath(d):
    return [os.path.join(d, f) for f in os.listdir(d)]


def hash_(string):
    return hashlib.sha1(string.encode()).hexdigest()
