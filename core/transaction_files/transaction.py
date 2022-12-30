import time as _time
from dataclasses import dataclass
import binascii
import collections
import json
from ..wallet_files.user import User
from ..wallet_files.wallet import Wallet
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA, SHA256


@dataclass
class TransactionData:
    def __init__(self):
        recipient: str
        coin: str
        value: str
@dataclass
class TransactionInput:
    output_index: int
    transaction_hash:str
    public_key: bytes
    signature: bytes
    

@dataclass
class Transaction:
    sender: Wallet   # this is now the wallet address(could possibly change to wallet object)
    recipient: str
    value: float
    coin_type: str  # Need to implement control and security protocols to check b4 compiled into blocks.
    time: float = _time.time()
    signature = None
    # add cointype, blockgroup, ether chain information, other arbitrary info

    # TODO: what is the identity property?
    def to_dict(self) -> collections.OrderedDict:
        if self.sender == "Genesis":
            identity = "Genesis"
        else:
            identity = self.sender.address

        return collections.OrderedDict(
            {
                "sender": str(identity),
                "recipient": str(self.recipient),
                "value": str(self.value),
                "time": str(self.time),
                "coinType": self.coin_type,
            }
        )
    
    def to_bytes(self):
        transaction_byte_data = self.to_dict
        return json.dumps(transaction_byte_data, indent=2).encode('utf-8')
        
    def display_transaction(self, transactions):
        for transaction in transactions:
            dict = transaction.to_dict()
            print("sender: " + dict["sender"])
            print("-----")
            print("recipient: " + dict["recipient"])
            print("-----")
            print("value: " + str(dict["value"]))
            print("-----")
            print("time: " + str(dict["time"]))
            print("-----")
            print("--------------")

    # # TODO: this is an old transaction signing
    #TODO fix sign transaction to represent addreses rather than public keys
    def sign_transaction(self, privatekey) -> str:
        transaction_data = self.to_bytes
        signer = pkcs1_15.new(privatekey)
        hash = SHA256.new(transaction_data)  # change var name
        signature = signer.sign(hash)
        self.signature = binascii.hexlify(signature).decode("utf-8")
