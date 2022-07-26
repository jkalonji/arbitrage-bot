# -*- coding: utf-8 -*-
"""
Created on Tue Jul 26 16:59:48 2022

@author: jerem
"""

import binascii
import xchainpy_thorchain
from xchainpy_thorchain.cosmos.models.StdTx import StdTx
import http3
import json
from xchainpy_client import interface
from xchainpy_crypto import crypto as xchainpy_crypto
#from xchainpy_thorchain import utils
from xchainpy_thorchain import crypto
from xchainpy_thorchain import client
from xchainpy_thorchain.cosmos.models.MsgCoin import MsgCoin
from xchainpy_thorchain.cosmos.models.MsgNativeTx import MsgNativeTx
from xchainpy_thorchain.cosmos.sdk_client import CosmosSDKClient
from xchainpy_thorchain.cosmos import message
#from xchainpy_thorchain.utils import DEFAULT_GAS_VALUE, asset_to_string, frombech32, getDenomWithChain, get_asset

import asyncio

from xchainpy_thorchain.cosmos.cosmosUtil import bech32_prefix 
import bech32
#from bech32 import decode

# ===================== Def classes ====================

class Client(interface.IXChainClient):

    derive_path = "m/44'/118'/0'/0/0"
    phrase = address = network = ''
    private_key = None

    def __init__(self, phrase: str, network: str = "testnet", client_url: str = None, explorer_url: str = None) -> None:
        """Constructor

        Client has to be initialised with network type and phrase.
        It will throw an error if an invalid phrase has been passed.

        :param phrase: phrase of wallet (mnemonic) will be set to the Class
        :param network: network of chain can either be `testnet` or `mainnet`
        :param client_url: client url can be added manually
        :param explorer_url: explorer url can be added manually
        :type phrase: string
        :type network: string
        :type client_url: string
        :type explorer_url: string
        :return: returns void (None)
        :rtype: None
        """
        self.network = network
        self.client_url = client_url or self.get_default_client_url()
        self.explorer_url = explorer_url or self.get_default_explorer_url()
        self.thor_client = self.get_new_thor_client()

        if phrase:
            self.set_phrase(phrase)

    async def purge_client(self) -> None:
        """Purge client

        :return: returns void (None)
        :rtype: None
        """
        self.phrase = self.address = ''
        self.private_key = None
        await self.thor_client.client.close()

    def set_network(self, network: str) -> None:
        """Set/update the current network.

        :param netowrk: network `mainnet` or `testnet`
        :type network: string
        :returns: Nothing (Void/None)
        :raises:
            Exception: "Network must be provided". -> Thrown if network has not been set before.
        """
        if not network:
            raise Exception('Network must be provided')
        else:
            self.network = network
            self.thor_client = self.get_new_thor_client()
            self.address = ''

    def set_phrase(self, phrase: str) -> str:
        if not self.phrase or self.phrase != phrase:
            if not xchainpy_crypto.validate_phrase(phrase):
                raise Exception("invalid phrase")

            self.phrase = phrase
            self.private_key = None
            self.address = ''

        return self.get_address()

    def get_network(self) -> str:
        """Get the current network.

        :returns: The current network. (`mainnet` or `testnet`)
        :rtype: string
        """
        return self.network

    def set_client_url(self, client_url: str) -> None:
        """Set/update the client URL.

        :param client_url: The client url to be set.
        :type client_url: string
        :returns: Nothing (None)
        :rtype: None
        """
        self.client_url = client_url
        self.thor_client = self.get_new_thor_client()

    def validate_address(self, address: str, prefix: str):
        """Validate the given address

        :param address: address
        :type address: str
        :param prefix: bnb or tbnb
        :type prefix: str
        :returns: True or False
        """
        return True if crypto.check_address(address, prefix) else False

    def get_default_client_url(self) -> object:
        """Get the client url.

        :returns: The client url (both node, rpc) for thorchain based on the network.
        :rtype: {NodeUrl} as a object
        """
        return {
            "testnet": {
                "node": 'https://testnet.thornode.thorchain.info',
                "rpc": 'https://testnet.rpc.thorchain.info',
            },
            "mainnet": {
                "node": 'https://thornode.thorchain.info',
                "rpc": 'https://rpc.thorchain.info',
            },
        }

    def get_default_explorer_url(self) -> str:
        """Get the explorer url.

        :returns: The explorer url (both mainnet and testnet) for thorchain.
        :rtype: string
        """
        return 'https://testnet.thorchain.net' if self.network == 'testnet' else 'https://thorchain.net'

    def get_explorer_tx_url(self , tx_id: str) -> str:
        """Get the explorer url for the given transaction id.
   
        :param tx_id: network
        :type tx_id: string
        :returns: The explorer url for the given transaction id.
        :rtype: string
        """
        return f'{self.get_default_explorer_url()}/txs/${tx_id}'

    def get_prefix(self, network: str = None) -> str:
        """Get address prefix based on the network.

        :param network: network
        :type network: string
        :returns: The address prefix based on the network.
        :rtype: string
        """
        if network:
            return 'tthor' if network == 'testnet' else 'thor'
        else:
            return 'tthor' if self.network == 'testnet' else 'thor'

    def get_chain_id(self) -> str:
        """Get the chain id.

        :returns: The chain id based on the network.
        :rtype: string
        """
        return 'thorchain'

    def get_new_thor_client(self):
        """Get new thorchain client.

        :returns: The new thorchain client.
        :rtype: CosmosSDKClient Class    
        """
        network = self.get_network()
        return CosmosSDKClient(server=self.client_url[network]["node"], prefix=self.get_prefix(), derive_path="m/44'/931'/0'/0/0", chain_id=self.get_chain_id())

    def get_private_key(self) -> bytes:
        """Get private key.

        :returns: The private key generated from the given phrase
        :rtype: bytes
        :raises: 
            Exception: {"Phrase not set"} -> Throws an error if phrase has not been set before
        """
        if not self.private_key:
            if not self.phrase:
                raise Exception('Phrase not set')

            self.private_key = self.thor_client.seed_to_privkey(self.phrase)

        return self.private_key

    def get_address(self) -> str:
        """Get the current address

        :returns: the current address
        :rtype: string
        :raises: 
            Exception: {"Address has to be set. Or set a phrase by calling `setPhrase` before to use an address of an imported key."}
                        -> Raises if phrase has not been set before. A phrase is needed to create a wallet and to derive an address from it.
        """
        if not self.address:
            self.address = self.thor_client.privkey_to_address(
                self.get_private_key())
            if not self.address:
                raise Exception(
                    "Address has to be set. Or set a phrase by calling `setPhrase` before to use an address of an imported key.")
        return self.address

    async def get_balance(self, address: str = None, assets = None) -> list:
        """
         Get the balance of a given address.

         :param address: address By default, it will return the balance of the current wallet. (optional)
         :param asset: asset If not set, it will return all assets available. (optional)
         :returns: The balance of the address.
         :rtype: list
        """
        if not address:
            address = self.get_address()
        response = await self.thor_client.get_balance(address)
        response = response["result"]

        balances = []
        for balance in response:
            asset = None
            if balance['denom']:
                asset = get_asset(balance['denom'])
            else:
                asset = {"chain" : "THOR", "symbol": "RUNE" , "ticker" : "RUNE"}
            amount = balance['amount']
            balances.append({"asset" : asset,"amount" : amount})
        if assets:
            return list(filter(lambda x : any(asset_to_string(x["asset"]) == asset_to_string(element) for element in assets) , balances))
        return balances

    async def get_transaction_data(self, tx_id: str) -> object:
        """Get the transaction details of a given transaction id

        if you want to give a hash that is for mainnet and the current self.net is 'testnet',
        you should call self.set_network('mainnet') (and vice versa) and then call this method.

        :param tx_id: The transaction id
        :type tx_id: str
        :returns: The transaction details of the given transaction id
        :rtype: object
        """
        try:
            tx_result = await self.thor_client.txs_hash_get(tx_id)
            if not tx_result:
                raise Exception("transaction not found")
            return tx_result
        except Exception as err:
            raise Exception(err)

    async def transfer(self, amount: int, recipient: str, asset = {"symbol": "rune"}, memo: str = "") -> dict:
        """Transfer balances with MsgSend

        :param amount: amount which you want to send
        :param recipient: the address of recipient to be send
        :param asset: asset need to be send
        :param memo: memo of the transaction
        :type amount: int
        :type recipient: string
        :type asset: string
        :type memo: string
        :returns: The transaction hash
        :rtype: object
        """
        if not asset:
            raise Exception('Asset must be provided')
        if not amount:
            raise Exception('Amount must be provided')
        if not recipient:
            raise Exception('Destination address must be provided')

        before_balance = await self.get_balance()
        if len(before_balance) == 0:
            raise Exception('No balance in this wallet')
        print('before_balance: ',before_balance)
        before_balance_amount = before_balance[0]['amount']
        fee = await self.get_fees()
        fee = float(base_amount(fee['average'], DECIMAL))
        print('before_balance_amount: ',before_balance_amount)
        if (amount + fee) > float(before_balance_amount):
            raise Exception(
                'input asset amout is higher than current (asset balance - transfer fee)')

        try:
            await self.thor_client.make_transaction(self.get_private_key(), bech32_decode('thor163d6u80etxenfsuttfzhw57ly36f0wj2q3utc0'), fee_denom=asset['symbol'].lower(), memo=memo)
            self.thor_client.add_transfer(recipient, amount, denom=asset['symbol'].lower())
            Msg = self.thor_client.get_pushable()
            return await self.thor_client.do_transfer(Msg)
        except Exception as err:
            raise Exception(err)

    async def get_fees(self) -> dict:
        """Get the current fees

        :returns: The fees with three rates
        :rtype: dict
        """
        fee = DEFAULT_GAS_VALUE

        return {
            
            "fast": fee,
            "fastest": fee,
            "average": fee,
        }

    async def build_deposit_tx(self , msg_native_tx : MsgNativeTx) -> StdTx :
        try:
            url = f'{self.client_url[self.get_network()]["node"]}/thorchain/deposit'
            client = http3.AsyncClient(timeout=10)
            data = {
            "coins" : msg_native_tx.coins,
            "memo" : msg_native_tx.memo,
            "base_req" : {
                "chain_id" : "thorchain",
                "from" : msg_native_tx.signer
            }  
            }
            response = await client.post(url=url, json=data)

            if response.status_code == 200:
                res = json.loads(response.content.decode('utf-8'))['value']
                unsigned_std_tx = StdTx(res['msg'] , res['fee'] ,[] ,'')

                return unsigned_std_tx
            else:
                raise Exception(response.text)

        except Exception as err:
            raise Exception(str(err))
        

    async def deposit(self, amount , memo , asset = {"chain" : "THOR", "symbol": "RUNE" , "ticker" : "RUNE"}):
        try:
            asset_balance = await self.get_balance(self.get_address(), [asset])
            if len(asset_balance) == 0 or float(asset_balance[0]['amount']) < (float(amount) + DEFAULT_GAS_VALUE):
                raise Exception("insufficient funds")

            signer = self.get_address()
            coins = [MsgCoin(getDenomWithChain(asset), amount).to_obj()]

            msg_native_tx = message.msg_native_tx_from_json(coins, memo, signer)
            
            unsigned_std_tx = await self.build_deposit_tx(msg_native_tx)
            fee = unsigned_std_tx.fee
            private_key = self.get_private_key()
            acc_address = frombech32(signer)
            # max gas
            fee['gas'] = '100000000'

            result = await self.thor_client.sign_and_broadcast(unsigned_std_tx, private_key, acc_address)
            if not result['logs']:
                raise Exception("failed to broadcast transaction")
            else:
                return result

        except Exception as err:
            raise Exception(str(err))




# ============================================
# File "/home/jrm/.local/lib/python3.8/site-packages/xchainpy_thorchain/utils.py",
# line 38, in tobech32 words = bech32_towords(bytes(value))


DECIMAL = 8
DEFAULT_GAS_VALUE = 2000000


def base_amount(value: str and int, decimal: int = DECIMAL) -> str:
    if type(value) == int:
        return str(value / 10**decimal)
    else:
        return str(int(value) / 10**decimal)


def cnv_big_number(value: float and int and str, decimal: int = DECIMAL) -> str:
    if type(value) == float or type(value) == int:
        return str(round(float(value) * (10**decimal)))
    elif type(value) == str:
        return str(round(float(value) * (10**decimal)))


def getDenomWithChain(asset) -> str:
    return f'THOR.{asset["symbol"].upper()}'


def bech32_fromwords(words):
    res = bech32.convertbits(words, 5, 8, False)
    if res:
        return res


def bech32_towords(value_bytes):
    res = bech32.convertbits(value_bytes, 8, 5, False)
    if res:
        return res
    

def frombech32(address : str):
    (prefix, words) = bech32.bech32_decode(address)
    res = bech32_fromwords(words)
    return res


def tobech32(value):
    words = bech32_towords(bytes(value, 'utf-8'))
    enc = bech32.bech32_encode(bech32_prefix["accAddr"], words)
    return enc


def sort_dict(item: dict):
    return {k: sort_dict(v) if isinstance(v, dict) else v for k, v in sorted(item.items())}    


def get_asset(denom : str):
    if denom == 'rune':
        return  {"chain" : "THOR", "symbol": "RUNE" , "ticker" : "RUNE"}
    else:
        
        return  {"chain" : "THOR", "symbol": denom.upper() , "ticker" : denom.split('-')[0]}


def asset_to_string(asset):
    return f'{asset["chain"]}.{asset["symbol"]}'


# NameError: name 'bech32_decode' is not defined

from typing import Iterable, List, Optional, Tuple, Union
CHARSET = "qpzry9x8gf2tvdw0s3jn54khce6mua7l"

def bech32_polymod(values: Iterable[int]) -> int:
    """Internal function that computes the Bech32 checksum."""
    generator = [0x3b6a57b2, 0x26508e6d, 0x1ea119fa, 0x3d4233dd, 0x2a1462b3]
    chk = 1
    for value in values:
        top = chk >> 25
        chk = (chk & 0x1ffffff) << 5 ^ value
        for i in range(5):
            chk ^= generator[i] if ((top >> i) & 1) else 0
    return chk


def bech32_hrp_expand(hrp: str) -> List[int]:
    """Expand the HRP into values for checksum computation."""
    return [ord(x) >> 5 for x in hrp] + [0] + [ord(x) & 31 for x in hrp]


def bech32_verify_checksum(hrp: str, data: Iterable[int]) -> bool:
    """Verify a checksum given HRP and converted data characters."""
    return bech32_polymod(bech32_hrp_expand(hrp) + list(data)) == 1


def bech32_create_checksum(hrp: str, data: Iterable[int]) -> List[int]:
    """Compute the checksum values given HRP and data."""
    values = bech32_hrp_expand(hrp) + list(data)
    polymod = bech32_polymod(values + [0, 0, 0, 0, 0, 0]) ^ 1
    return [(polymod >> 5 * (5 - i)) & 31 for i in range(6)]


def bech32_encode(hrp: str, data: Iterable[int]) -> str:
    """Compute a Bech32 string given HRP and data values."""
    combined = list(data) + bech32_create_checksum(hrp, data)
    return hrp + "1" + "".join([CHARSET[d] for d in combined])


def bech32_decode(bech: str) -> Union[Tuple[None, None], Tuple[str, List[int]]]:
    """Validate a Bech32 string, and determine HRP and data."""
    if (any(ord(x) < 33 or ord(x) > 126 for x in bech)) or (
        bech.lower() != bech and bech.upper() != bech
    ):
        return (None, None)
    bech = bech.lower()
    pos = bech.rfind("1")
    if pos < 1 or pos > 83 or pos + 7 > len(bech):  # or len(bech) > 90:
        return (None, None)
    if not all(x in CHARSET for x in bech[pos + 1 :]):
        return (None, None)
    hrp = bech[:pos]
    data = [CHARSET.find(x) for x in bech[pos + 1 :]]
    if not bech32_verify_checksum(hrp, data):
        return (None, None)
    return (hrp, data[:-6])


def convertbits(data: Iterable[int], frombits: int, tobits: int, pad: bool = True) -> Optional[List[int]]:
    """General power-of-2 base conversion."""
    acc = 0
    bits = 0
    ret = []
    maxv = (1 << tobits) - 1
    max_acc = (1 << (frombits + tobits - 1)) - 1
    for value in data:
        if value < 0 or (value >> frombits):
            return None
        acc = ((acc << frombits) | value) & max_acc
        bits += frombits
        while bits >= tobits:
            bits -= tobits
            ret.append((acc >> bits) & maxv)
    if pad:
        if bits:
            ret.append((acc << (tobits - bits)) & maxv)
    elif bits >= frombits or ((acc << (tobits - bits)) & maxv):
        return None
    return ret


def decode(hrp: str, addr: str) -> Union[Tuple[None, None], Tuple[int, List[int]]]:
    """Decode a segwit address."""
    hrpgot, data = bech32_decode(addr)
    if hrpgot != hrp:
        return (None, None)
    assert data is not None
    decoded = convertbits(data[1:], 5, 8, False)
    if decoded is None or len(decoded) < 2 or len(decoded) > 40:
        return (None, None)
    if data[0] > 16:
        return (None, None)
    if data[0] == 0 and len(decoded) != 20 and len(decoded) != 32:
        return (None, None)
    return (data[0], decoded)


def encode(hrp: str, witver: int, witprog: Iterable[int]) -> Optional[str]:
    """Encode a segwit address."""
    five_bit_witprog = convertbits(witprog, 8, 5)
    if five_bit_witprog is None:
        return None
    ret = bech32_encode(hrp, [witver] + five_bit_witprog)
    if decode(hrp, ret) == (None, None):
        return None
    return ret
# ==================== Main ======================


async def main():
    #thorClient = IThorchainClient()
    #client = IXChainClient()
    phrase = 'rule morning slim debris main lumber retire air remind satisfy panic ball'
    thorClient = Client(phrase)
    thorClient.set_network('mainnet')
    memo = 'SWAP:THOR.ETH.ETH.ETH:0xC3b35c81BD9a316F6c8fD9edc12c044e24A65CA5:1'
    print('adresse du client: ', thorClient.get_address())

    
    #f1 = loop.create_task(thorClient.get_balance())
    #print(f1)
    f2 = loop.create_task(thorClient.transfer(1, 'thor163d6u80etxenfsuttfzhw57ly36f0wj2q3utc0', {"symbol":"THOR.ETH.ETH"}, memo))
    print(f2)
    await asyncio.wait([f2])


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
#asyncio.run(main())
