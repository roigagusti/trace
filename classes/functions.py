
def balance(blockchain,user):
    balance = 0
    for block in blockchain:
        for transaction in block.transactions:
            if transaction['seller'] == user:
                balance += int(transaction['amount'])
            if transaction['buyer'] == user:
                balance -= int(transaction['amount'])
    return balance