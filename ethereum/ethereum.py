from Crypto.Util.number import *
import os

# 设置provider为测试链
os.environ["WEB3_PROVIDER_URI"] = "https://ropsten.infura.io/v3/0993fb0fcd0b4017a1512244688eca6c"

from web3.auto import w3


# w3.eth.defaultAddress = "0x62ECE298dE844EF5636233A6c871CF7ebe4Ea069"

# from eth_account.messages import encode_defunct

# 用私钥key签发包含msg的trans到区块链，后期地址可能会填成合约地址
def send_to_ether(msg, key):
    my = w3.eth.account.from_key(private_key=key)
    signed_trans = my.sign_transaction(dict(
        nonce=w3.eth.getTransactionCount("0x62ECE298dE844EF5636233A6c871CF7ebe4Ea069"),
        gasPrice=w3.eth.gasPrice,
        gas=100000,
        to='0x5DF9B87991262F6BA471F09758CDE1c0FC1De734',
        value=0,
        data=bytes(msg.encode()),
    ))
    transhash = w3.eth.sendRawTransaction(signed_trans.rawTransaction)
    return transhash


# 通过交易哈希获取交易中包含的消息
def get_from_ether(transhash):
    trans = w3.eth.getTransaction(transhash)
    data = trans.get['input']
    data_in_int = int(data, 16)
    return long_to_bytes(data_in_int.decode('utf-8'))

# print(send_to_ether("我爱张华", "你的key").hex())

# message = encode_defunct(text=msg)
