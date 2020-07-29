from configparser import ConfigParser
import os
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex


def add_to_16(text):
    if len(text.encode('utf-8')) % 16:
        add = 16 - (len(text.encode('utf-8')) % 16)
    else:
        add = 0
    text = text + ('\0' * add)
    return text.encode('utf-8')


def encrypt(text):
    key = 'your key'.encode('utf-8')
    mode = AES.MODE_CBC
    iv = b'qqqqqqqqqqqqqqqq'
    text = add_to_16(text)
    cryptos = AES.new(key, mode, iv)
    cipher_text = cryptos.encrypt(text)
    # 因为AES加密后的字符串不一定是ascii字符集的，输出保存可能存在问题，所以这里转为16进制字符串
    return b2a_hex(cipher_text)


def decrypt(text):
    key = 'your key'.encode('utf-8')
    iv = b'qqqqqqqqqqqqqqqq'
    mode = AES.MODE_CBC
    cryptos = AES.new(key, mode, iv)
    plain_text = cryptos.decrypt(a2b_hex(text))
    return bytes.decode(plain_text).rstrip('\0')


# os.getcwd()
def get_context():
    cfg = ConfigParser()
    cfg.read("config.ini")
    os.environ["WEB3_INFURA_PROJECT_ID"] = cfg.get("init", "WEB3_INFURA_PROJECT_ID")
    os.environ["WEB3_INFURA_API_SECRET"] = cfg.get("init", "WEB3_INFURA_API_SECRET")
    os.environ["WEB3_PROVIDER_URI"] = cfg.get("init", "WEB3_PROVIDER_URI")
    from web3.auto import w3
    my = w3.eth.account.from_key(decrypt(cfg.get("init", "PRIVATE_KEY")))
    return w3, my


def get_sol():
    cfg = ConfigParser()
    cfg.read("../contract/eth.sol")
    print(cfg.sections())

