from dataclasses import dataclass, field
import time
from NimlothBlockClass import NimlothBlock

@dataclass 
class Blockchain:
    unconfirmed_transactions: list = field(default_factory=list)
    chain: list = field(default_factory=list)
    difficulty: int = 2

    def __post_init__(self):
        self.create_genesis_block()

    # TODO: hash is not a property of block 
    def create_genesis_block(self) -> None:
        genesis_block = NimlothBlock(0, [], time.time(), "0")
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)

    def proof_of_work(self, block: NimlothBlock) -> str:
        block.nonce = 0
        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0'*Blockchain.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()
        return computed_hash
    
    # TODO: type proof parameter 
    # TODO: hash is not a property of block 
    def add_block(self, block: NimlothBlock, proof) -> bool:
        previous_hash = self.last_block.hash
        if previous_hash != block.previous_hash:
            return False
        if not self.is_valid_proof(block, proof):
            return False
        block.hash = proof
        self.chain.append(block)
        return True

    # TODO: type block_hash parameter 
    def is_valid_proof(self, block: NimlothBlock, block_hash) -> bool:
        return (block_hash.startswith('0'*Blockchain.difficulty) and 
                block_hash == block.compute_hash())
    
    # TODO: type transaction parameter 
    def add_new_transaction(self, transaction) -> None:
        self.unconfirmed_transactions.append(transaction)
