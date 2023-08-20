from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
import time
import hashlib

app = Flask(__name__)

# Set up MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['blockchain_db']
blocks_collection = db['blocks']

class Block:
    def __init__(self, index, previous_hash, timestamp, data, nonce=0):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        data = f"{self.index}{self.previous_hash}{self.timestamp}{self.data}{self.nonce}"
        return hashlib.sha256(data.encode()).hexdigest()

    def mine_block(self, difficulty):
        target = "0" * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
        print("Block mined: " + self.hash)

# Create the blockchain
genesis = Block(0, "0", 0, "Genesis Block")
genesis.mine_block(1)
blockchain = [genesis]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    index = len(blockchain)
    previous_hash = blockchain[-1].hash
    timestamp = int(time.time())
    data = request.form['name']
    new_block = Block(index, previous_hash, timestamp, data)
    new_block.mine_block(1)
    blockchain.append(new_block)    
    return jsonify({"message": "Transaction added"})

@app.route('/get_chain', methods=['GET'])
def get_chain():
    serialized_blocks = [block.__dict__ for block in blockchain]
    return jsonify(serialized_blocks)

if __name__ == '__main__':
    app.run(debug=True)

    