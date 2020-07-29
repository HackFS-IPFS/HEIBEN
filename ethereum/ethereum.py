from Crypto.Util.number import *

from utils import utils
from solc import compile_standard
import json
import pprint


class Ethereum:
    def __init__(self):
        # 获取w3, my
        self.w3, self.my = utils.get_context()
        self.w3.eth.defaultAccount = self.my.address
        self.contract_instances = {}

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

    # 获取合约$name，需要在deploy_contract之后调用，否则返回None
    def get_contract_by_name(self, name):
        return self.contract_instances.get(name)

    # 获取所有合约
    def get_all_contract(self):
        return self.contract_instances

    """
    source = contract Greeter {
                string public greeting;
    
                function Greeter() {
                    greeting = 'Hello';
                }
    
                function setGreeting(string _greeting) public {
                    greeting = _greeting;
                }
    
                function greet() constant returns (string) {
                    return greeting;
                }
            }
        #sol should like this
        sol = {
            "name": "Greeter.sol",
            "body": source
        }
    """

    def deploy_contract(self, sol, sol_name):
        sol_name = "Greeter"

        source = """contract Greeter {
                        string public greeting;

                        function Greeter() {
                            greeting = 'Hello';
                        }

                        function setGreeting(string _greeting) public {
                            greeting = _greeting;
                        }

                        function greet() constant returns (string) {
                            return greeting;
                        }
                    }
                """
        # sol should like this
        sol = {
            "name": "Greeter.sol",
            "body": source
        }
        compiled_sol = compile_standard({
            "language": "Solidity",
            "sources": {
                sol.get("name"): {
                    "content": sol.get("body")
                }
            },
            "settings": {
                "outputSelection": {
                    "*": {
                        "*": ["metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                    }
                }
            }
        })
        bytecode = compiled_sol['contracts'][sol.get("name")][sol_name]['evm']['bytecode']['object']
        abi = json.loads(compiled_sol['contracts'][sol.get("name")][sol_name]['metadata'])['output']['abi']
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
        self.contract_instances[sol_name] = self.w3.eth.contract(
            address=tx_receipt.contractAddress,
            abi=abi
        )
        # return self.contract_instance


# print(send_to_ether("我爱张华", "你的key").hex())

ethereum = Ethereum()
ins = ethereum.deploy_contract(1, 2)
print(ethereum.contract_instance)

# print(ins.functions.greet().call())
# print(ethereum.get_from_ether("0x1f2c6bf11571f5609004e7fb316879261e4ace728e88923fb23d8ec31be1bff8"))
