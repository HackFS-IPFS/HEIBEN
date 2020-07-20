from solc import compile_source
from web3 import Web3, HTTPProvider
import json
from config import config
from sha3 import keccak_256
import random

class Instance:
	def __init__(self, name, code):
		self.address = "快来部署合约吧"
		self.compiled = compile_source(code)
		self.interface = self.compiled['<stdin>:' + name]
		self.w3 = Web3(HTTPProvider(config["infura"])) 
		self.contract = self.w3.eth.contract(abi = self.interface["abi"], bytecode = self.interface["bin"])

		self.slogan = "👈 这边是源码哦~"
		self.acct = self.w3.eth.account.privateKeyToAccount(config["private"])
		self.w3.eth.defaultAccount = self.acct


	def getAddress(self):
		return self.address

	def deploy(self, num):
		if self.address[:2] == "0x":
			return "你已经有合约了 (▼⊿▼)"
		construct_txn = self.contract.constructor(self.randomStr()).buildTransaction({
			'from': self.acct.address,
			'value': 0,
			'nonce': self.w3.eth.getTransactionCount(self.acct.address, 'pending'),
			'gas': 1000000,
			'gasPrice': self.w3.toWei('30', 'gwei')})

		signed = self.acct.signTransaction(construct_txn)
		txn_hash = self.w3.eth.sendRawTransaction(signed.rawTransaction)
		txn_receipt = self.w3.eth.waitForTransactionReceipt(txn_hash)
		self.address = txn_receipt["contractAddress"]
		self.challenge = self.w3.eth.contract(address = self.address, abi = self.interface["abi"])
		print("The {}th contract deploied, address: {}.".format(num, self.address))

		return "部署成功！"


	def initChallenge(self):
		# 调用 view 或者 pure 函数时需要重新搞一个 web3 出来，很迷
		provider = Web3.HTTPProvider("https://ropsten.infura.io/v3/cea814e8a71845b997e2501bffe94ad1")
		w3 = Web3(provider)

		return w3.eth.contract(address = self.address, abi = self.interface['abi'])


	def nextHash(self):
		challenge = self.initChallenge()
		construct_txn = challenge.functions.nextHash(self.randomStr()).buildTransaction({
			'from': self.acct.address,
			'value': 0,
			'nonce': self.w3.eth.getTransactionCount(self.acct.address, 'pending'),
			'gas': 1000000,
			'gasPrice': self.w3.toWei('30', 'gwei')})
		signed = self.acct.signTransaction(construct_txn)
		tx_hash = self.w3.eth.sendRawTransaction(signed.rawTransaction)
		# tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
		return "更新成功~"


	def check(self):
		challenge = self.initChallenge()
		res = challenge.functions.getFlag().call()
		return res


	def randomStr(self):
		random_str = ''
		base_str = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789'
		length = len(base_str) - 1
		for i in range(6):
			random_str += base_str[random.randint(0, length)]
		return random_str

	def updateSlogan(self):
		try:
			challenge = self.initChallenge()
			newSlogan = str(challenge.functions.getSlogan().call())
			if self.isVaild(newSlogan):
				self.slogan = newSlogan
				return False
			else:
				return True 
		except Exception as e:
			pass
		

	def isVaild(self, slogan):
		if "\{\}.[]\\|" in slogan:
			return False
		else:
			return True