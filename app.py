from flask import Flask, request, jsonify, render_template, redirect, url_for
from classes.blockchain import Block, Transaction, initBlockchain
from classes.functions import balance
import time
import json



app = Flask(__name__)



# BLOCKCHAIN INITIALIZATION
blockchain, transactions = initBlockchain()


# PRODCUTION ROUTES
@app.route('/')
def index():
    return render_template('add_transaction.html')

@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    # Create transaction
    buyer = request.form['buyer']
    seller = request.form['seller']
    sku = request.form['sku']
    amount = request.form['amount']
    skuPerformance = request.form['skuPerformance']
    skuImpact = request.form['skuImpact']
    timestamp = int(time.time())
    transaction = Transaction(buyer, seller, sku, amount, skuPerformance, skuImpact, timestamp)
    transactions.append(transaction)

    # Each 5 transactions, create a new block
    if len(transactions) % 2 == 0:
        index = len(blockchain)
        previous_hash = blockchain[-1].hash
        timestamp = int(time.time())
        trans = [transaction.__dict__ for transaction in transactions]
        description = ",".join([transaction.hash for transaction in transactions])
        new_block = Block(index, previous_hash, timestamp, description, trans)
        new_block.mine_block(1)
        blockchain.append(new_block)
        transactions.clear()

        # Save the blockchain
        serialized_blocks = [block.__dict__ for block in blockchain]
        with open('blockchain.json', 'w') as json_file:
            json.dump(serialized_blocks, json_file, indent=4)
    return redirect(url_for('index'))


@app.route('/get_chain', methods=['GET'])
def get_chain():
    serialized_blocks = [block.__dict__ for block in blockchain]
    return jsonify(serialized_blocks)


@app.route('/balance/<user>')
def get_balance(user):
    value = balance(blockchain,user)
    return jsonify(value)

@app.route('/product-life/<sku>')
def get_productLife(sku):
    history = []
    # Get all transactions with the same sku and return their properties and how many times they have been used, paid, etc.
    for block in blockchain:
        for transaction in block.transactions:
            if transaction['sku'] == sku:
                history.append(transaction)
    return render_template('product_life.html', sku=sku, history=history)
                



if __name__ == '__main__':
    app.run(debug=True)
    