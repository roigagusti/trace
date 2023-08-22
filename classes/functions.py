
def balance(blockchain,user):
    balance = 0
    for block in blockchain:
        for transaction in block.transactions:
            if transaction['recipient'] == user:
                balance += int(transaction['amount'])
            if transaction['sender'] == user:
                balance -= int(transaction['amount'])
    return balance