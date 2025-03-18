from hashlib import sha256
import time


class Transaction:
    def __init__(self, from_addr, to_addr, amount):
        self.from_addr = from_addr
        self.to_addr = to_addr
        self.amount = amount


class Block:
    def __init__(self, timestamp, transactions, prior_hash=''):
        self.timestamp = timestamp
        self.transactions = transactions
        self.prior_hash = prior_hash
        self.nonce = 0
        self.hash = self.create_hash()

    def create_hash(self):
        block_string = (str(self.prior_hash) + str(self.timestamp) + str(self.transactions) + str(self.nonce)).encode(
        )
        return sha256(block_string).hexdigest()

    def mine_block(self, difficulty):
        target = '0' * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.create_hash()
        print(f'Block mined! Nonce: {self.nonce}, Hash: {self.hash}')


class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 2
        self.pending_transactions = []
        self.mining_reward = 10

    def create_genesis_block(self):
        return Block(time.time(), [], "0")

    def get_last_block(self):
        return self.chain[-1]

    def mine_pending_transactions(self, mining_reward_address):
        block = Block(time.time(), self.pending_transactions,
                      self.get_last_block().hash)
        block.mine_block(self.difficulty)
        self.chain.append(block)
        self.pending_transactions = [Transaction(
            None, mining_reward_address, self.mining_reward)]

    def create_transaction(self, transaction):
        self.pending_transactions.append(transaction)

    def get_balance_of_address(self, address):
        balance = 0

        for block in self.chain:
            for transaction in block.transactions:
                if transaction.from_addr == address:
                    balance -= transaction.amount
                if transaction.to_addr == address:
                    balance += transaction.amount
        return balance

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != current_block.create_hash():
                return False
            if current_block.prior_hash != previous_block.hash():
                return False
        return True


# phuong thuc tao va quan ly chuoi khoi (blockchain)
class ErnestoBlockChain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 4

    def create_genesis_block(self):
        return Block(0, '12/23/1899', 'TriveraTech.com', '3')

    def get_last_block(self):
        return self.chain[-1]

    def add_block(self, new_block):
        new_block.prior_hash = self.get_last_block().hash
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)

    def is_bc_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != current_block.create_hash():
                return False

            if current_block.prior_hash != previous_block.hash:
                return False
        return True


ernesto_coin = Blockchain()

ernesto_coin.create_transaction(Transaction('address1', 'address2', 75))
ernesto_coin.create_transaction(Transaction('address2', 'address1', 25))

print('Starting mining process...')
ernesto_coin.mine_pending_transactions('miner_address')
print(
    f'\nBalance of miner\'s wallet: {ernesto_coin.get_balance_of_address("miner_address")}')
print("Mining again to receive the reward...")
ernesto_coin.mine_pending_transactions('miner_address')
print(
    f'\nBalance of miner\'s wallet after second mining: {ernesto_coin.get_balance_of_address("miner_address")}')
