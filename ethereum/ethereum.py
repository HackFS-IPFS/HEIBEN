from Crypto.Util.number import *
from web3 import exceptions
from utils import utils
import json

"""
    本类基本没有做异常处理...
    尤其是设计到和合约交互的部分，可能会由于gas limit等问题导致交互不成功，可根据返回的tx_receipt来查询trans具体状态
    前三个函数暂时用不到，主要使用和合约交互的后面几个函数就可以了
"""
class Ethereum:
    def __init__(self):
        # 获取w3, my
        self.w3, self.my = utils.get_context()
        self.w3.eth.defaultAccount = self.my.address
        self.contract_instance = None

    # 签发包含msg的trans到区块链
    def send_to_ether(self, msg):
        signed_trans = self.my.sign_transaction(dict(
            nonce=self.w3.eth.getTransactionCount(self.my.address) + getRandomInteger(10),
            gasPrice=self.w3.eth.gasPrice,
            gas=100000,
            to='0x5DF9B87991262F6BA471F09758CDE1c0FC1De734',
            value=0,
            data=bytes(msg.encode()),
        ))
        transhash = self.w3.eth.sendRawTransaction(signed_trans.rawTransaction)
        return transhash

    # 通过交易哈希获取交易中包含的消息
    def get_from_ether(self, transhash):
        trans = self.w3.eth.getTransaction(transhash)
        # data信息需要单独处理，可能会有多种情况
        data = trans.get('input')
        return data
        # data_in_int = int(data, 16)
        # return long_to_bytes(data_in_int).decode('utf-8')

    def deploy_contract(self):
        sol_name = "hackfs"
        # sol should like this
        compiled_sol = utils.get_compiled_contract()
        bytecode = compiled_sol['contracts']["eth.sol"][sol_name]['evm']['bytecode']['object']
        abi = json.loads(compiled_sol['contracts']["eth.sol"][sol_name]['metadata'])['output']['abi']
        contract = self.w3.eth.contract(abi=abi, bytecode=bytecode)
        transaction = {
            'gasPrice': self.w3.eth.gasPrice,
            'chainId': self.w3.eth.chainId,
            'nonce': self.w3.eth.getTransactionCount(self.my.address)
        }
        contract_data = contract.constructor().buildTransaction(transaction)
        transaction = self.my.signTransaction(contract_data)
        tx_hash = self.w3.eth.sendRawTransaction(transaction.rawTransaction)

        tx_receipt = self.w3.eth.waitForTransactionReceipt(tx_hash)
        self.contract_instance = self.w3.eth.contract(
            address=tx_receipt.contractAddress,
            abi=abi
        )
        # return self.contract_instance

    # 必须在和合约交互之前调用
    def get_contract_instance(self, contractAddress):
        contract_instance = self.w3.eth.contract(
            address=contractAddress,
            abi=json.loads(utils.get_compiled_contract()['contracts']["eth.sol"]["hackfs"]['metadata'])['output']['abi']
        )
        self.contract_instance = contract_instance

    # 接下来的函数和合约函数一一对应，文档可以参考石墨
    def getHash(self, uuid):
        try:
            data = self.contract_instance.functions.getHash(uuid).call()
        except exceptions.BadFunctionCallOutput:
            return "no such uuid"
        return data

    """
        下列函数的运行时间不稳定，最好使用异步或者回调来确保前台响应效率...
    """

    def newHash(self, value):
        cool_function = self.contract_instance.functions.newHash(value)
        trans = cool_function.buildTransaction(
            {'nonce': self.w3.eth.getTransactionCount(self.my.address), 'gas': 1000000, "from": self.my.address,
             'gasPrice': self.w3.eth.gasPrice})
        signed = self.my.signTransaction(trans)
        tx_hash = self.w3.eth.sendRawTransaction(signed.rawTransaction)
        tx_receipt = self.w3.eth.waitForTransactionReceipt(tx_hash)
        # 返回值只是为了确认成功
        return tx_receipt

    def updateHash(self, oldHashValue, newHashValue):
        cool_function = self.contract_instance.functions.updateHash(oldHashValue, newHashValue)
        trans = cool_function.buildTransaction(
            {'nonce': self.w3.eth.getTransactionCount(self.my.address), 'gas': 1000000, "from": self.my.address,
             'gasPrice': self.w3.eth.gasPrice})
        signed = self.my.signTransaction(trans)
        tx_hash = self.w3.eth.sendRawTransaction(signed.rawTransaction)
        tx_receipt = self.w3.eth.waitForTransactionReceipt(tx_hash)
        return tx_receipt

    def newRelation(self, uuid, hashValue):
        cool_function = self.contract_instance.functions.newRelation(uuid, hashValue)
        trans = cool_function.buildTransaction(
            {'nonce': self.w3.eth.getTransactionCount(self.my.address), 'gas': 1000000, "from": self.my.address,
             'gasPrice': self.w3.eth.gasPrice})
        signed = self.my.signTransaction(trans)
        tx_hash = self.w3.eth.sendRawTransaction(signed.rawTransaction)
        tx_receipt = self.w3.eth.waitForTransactionReceipt(tx_hash)

        return tx_receipt

    # 备用
    def call_what_you_want(self, name):
        contract_func = self.contract_instance.functions[name]
        twentyone = contract_func("params").call()  # 是否有参数取决于合约，有参数提交的需要创建真实trans
        return twentyone


"""
下面是部分测试用例
"""

# 实例化对象
# ethereum = Ethereum()
# # 初始化合约对象
# ethereum.get_contract_instance("0x8d592ad6DA67C3FdDe95a3cD8c33441F29C39836")

# 合约存入新哈希
# print(ethereum.newHash("0x8d592ad6DA67C3FdDe95a3cD8c33441F29C39836"))
# 建立新关系
# print(ethereum.newRelation("123", "0x8d592ad6DA67C3FdDe95a3cD8c33441F29C39836"))
# 打印0x8d592ad6DA67C3FdDe95a3cD8c33441F29C39836
# 例子
ethereum = Ethereum()
ethereum.get_contract_instance("0x8d592ad6DA67C3FdDe95a3cD8c33441F29C39836")
ethereum.newHash("IPFSAddressExample")
ethereum.newRelation("oneExample", "IPFSAddressExample")
print(ethereum.getHash("oneExample"))
