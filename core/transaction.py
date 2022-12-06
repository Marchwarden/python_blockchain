import time as _time
from dataclasses import dataclass
import binascii
import collections

from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA

from .supportedCoins import coinList, networkList


@dataclass
class Transaction:
    # pylint: disable=too-many-instance-attributes
    # Eight is reasonable in this case.

    sender: any  # TODO: Change
    recipient: str
    value: float
    coin_type: str  # Need to implement control and security protocols to check b4 compiled into blocks.
    network: str
    time: float = _time.time()
    # add cointype, blockgroup, ether chain information, other arbitrary info

    # TODO: what is the identity property?
    def to_dict(self) -> collections.OrderedDict:
        if self.sender == "Genesis":
            identity = "Genesis"
        else:
            identity = self.sender.identity

        return collections.OrderedDict(
            {
                "sender": identity,
                "recipient": self.recipient,
                "value": self.value,
                "time": self.time,
                "coinType": self.coin_type,
                "network": self.network,
            }
        )

    def display_transaction(self, transaction):
        dict = transaction.to_dict()
        print("sender: " + dict["sender"])
        print("-----")
        print("recipient: " + dict["recipient"])
        print("-----")
        print("coinType: " + dict["coinType"])
        print("-----")
        print("value: " + str(dict["value"]))
        print("-----")
        print("network: " + dict["network"])
        print("-----")
        print("time: " + str(dict["time"]))
        print("-----")
        print("--------------")

    # TODO: this should not work
    def sign_transaction(self) -> str:
        private_key = self.sender._private_key
        signer = pkcs1_15.new(private_key)
        hash = SHA.new(str(self.to_dict()).encode("utf8"))  # change var name

        return binascii.hexlify(signer.sign(hash)).decode("ascii")

    # basic idea of system to check if the transaction is possible before initial creation by user.
    # prevents customers from sending money into the void by accident.
    def check_valid(self, proposed, verified):
        self.proposed = proposed
        self.verified = verified

        if self.proposed in self.verified:
            return True
        return False
