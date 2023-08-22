from flask import Flask, request, jsonify, render_template
import time
import hashlib
import json
import os

app = Flask(__name__)


# CLASSES & FUNCTIONS
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


# BLOCKCHAIN INITIALIZATION
if os.path.exists('blockchain.json'):
    # If the blockchain file exists, load the blockchain
    with open('blockchain.json') as json_file:
        serialized_blocks = json.load(json_file)
        blockchain = [Block(**block) for block in serialized_blocks]
else:
    # Create the blockchain
    genesis = Block(0, "0", 0, [], "Genesis Block")
    genesis.mine_block(1)
    blockchain = [genesis]
transactions = []


# PRODCUTION ROUTES
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    sender = request.form['sender']
    recipient = request.form['recipient']
    amount = request.form['amount']
    timestamp = int(time.time())
    transaction = Transaction(sender, recipient, amount, timestamp)
    transactions.append(transaction)

    if len(transactions) % 2 == 0:
        index = len(blockchain)
        previous_hash = blockchain[-1].hash
        timestamp = int(time.time())
        trans = [transaction.__dict__ for transaction in transactions]
        data = ",".join([transaction.hash for transaction in transactions])
        new_block = Block(index, previous_hash, timestamp, trans, data)
        new_block.mine_block(1)
        blockchain.append(new_block)
        transactions.clear()

        # Save the blockchain
        serialized_blocks = [block.__dict__ for block in blockchain]
        with open('blockchain.json', 'w') as json_file:
            json.dump(serialized_blocks, json_file, indent=4)
          
    return jsonify({"message": "Transaction added"})


@app.route('/get_chain', methods=['GET'])
def get_chain():
    serialized_blocks = [block.__dict__ for block in blockchain]
    return jsonify(serialized_blocks)



if __name__ == '__main__':
    app.run(debug=True)
    