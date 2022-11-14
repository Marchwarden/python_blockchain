import time as _time
from dataclasses import dataclass
import binascii
import collections

from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA

@dataclass
class Transaction:
    sender: str
    recipient: str 
    value: float 
    time: float = _time.time() 
#add cointype, blockgroup, ether chain information, other arbitrary info
    # TODO: what is the identity property?
    def to_dict(self) -> collections.OrderedDict:
        if self.sender == "Genesis":
            identity = "Genesis"
        else:
            identity = self.sender.identity
        
        return collections.OrderedDict({
            'sender': identity,
            'recipient': self.recipient,
            'value': self.value,
            'time': self.time })
    def display_transaction(transactions):
        for transaction in transactions:
            dict = transaction.to_dict()
            print ("sender: " + dict['sender'])
            print ('-----')
            print ("recipient: " + dict['recipient'])
            print ('-----')
            print ("value: " + str(dict['value'])) 
            print ('-----') 
            print ("time: " + str(dict['time'])) 
            print ('-----')   
            print ('--------------')
            
    
    def sign_transaction(self) -> str:
        private_key = self.sender._private_key
        signer = pkcs1_15.new(private_key)
        h = SHA.new(str(self.to_dict()).encode('utf8')) # change var name
        
        return binascii.hexlify(signer.sign(h)).decode('ascii') 
    