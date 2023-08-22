import hashlib
import os
import json

# CLASSES
class Block:
    def __init__(self, index, previous_hash, timestamp, transactions, data, nonce=0, hash=''):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.transactions = transactions
        self.data = data
        self.nonce = nonce
        self.hash = self.calculate_hash()
        if hash != '':
            if self.hash != hash:
                raise ValueError("Invalid hash")

    def calculate_hash(self):
        data = f"{self.index}{self.previous_hash}{self.timestamp}{self.data}{self.nonce}"
        return hashlib.sha256(data.encode('utf-8')).hexdigest()

    def mine_block(self, difficulty):
        target = "0" * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
        print("Block mined: " + self.hash)

class Transaction:
    def __init__(self, sender, recipient, amount, timestamp):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.timestamp = timestamp
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        data = f"{self.sender}{self.recipient}{self.amount}{self.timestamp}"
        return hashlib.sha256(data.encode('utf-8')).hexdigest()

# FUNCTIONS
def initBlockchain():
    if os.path.exists('blockchain.json'):
        # If the blockchain file exists, load the blockchain
        with open('blockchain.json') as json_file:
            serialized_blocks = json.load(json_file)
            blockchain = [Block(**block) for block in serialized_blocks]
    else:
        # If not, create the blockchain with the genesis block
        genesis = Block(0, "0", 0, [], "Genesis Block")
        genesis.mine_block(1)
        blockchain = [genesis]
    transactions = []
    return blockchain, transactions


