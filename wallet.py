import subprocess
import json
from constants import *
from dotenv import load_dotenv
import os
from web3 import Web3
from bit import *
from eth_account import Account

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))


load_dotenv()

mnemonic = os.getenv('mnemonic')

my_mnemonic = 'brother south surround harbor canal hurdle engine stick thing old sword sail noble ankle wisdom'


def derive_wallets(coin=BTC, mnemonic=my_mnemonic, depth=3):
    command = f'./derive -g --mnemonic='{mnemonic}' --coin='{coin}' --numderive'{depth}' --format=json'
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, err = p.communicate()
    p_status = p.wait()
    return json.loads(output)
    
coins = {'eth':derive_wallets(mnemonic=my_mnemonic,coin=ETH,numderive=3),'btc-test': derive_wallets(mnemonicmnem=my_mnemonic,coin=BTCTEST,numderive=3)}

eth_privatekey = coins['eth'][0]['privkey']
btc_privatekey = coins['btc-test'][0]['privkey']



def priv_key_to_account (coin, priv_key):
    if coin == ETH:
        return Account.privateKeyToAccount(priv_key)
    if coin == BTCTEST:
        return PrivateKeyTestnet(priv_key)

    
eth_account = priv_key_to_account(ETH,eth_pk)

btc_account = priv_key_to_account(BTCTEST,btc_pk)

def create_tx(coin,account,recipient,amount):
    if coin ==ETH:
        gasEstimate = w3.eth.estimateGas(
            {"from": account.address, "to": recipient, "value": amount}
        )
        return {
            "to": recipient,
            "from": account.address,
            "value": amount,
            "gasPrice": w3.eth.gasPrice,
            "gas": gasEstimate,
            "nonce": w3.eth.getTransactionCount(account.address)
        }
        
    if coin == BTCTEST:
        return PrivateKeyTestnet.prepare_transaction(account.address, [(recipient, amount, BTC)])  

def send_tx (coin, account, recipient, amount):
    if coin =='ETH':
        trxns_eth = create_tx(coin,account, recipient, amount)
        sign_trxns_eth = account.sign_transaction(trxns_eth)
        result = w3.eth.sendRawTransaction(sign_trxns_eth.rawTransaction)
        print(result.hex())
        return result.hex()
    else:
        trxns_btctest= create_tx(coin,account,recipient,amount)
        sign_trxns_btctest = account.sign_transaction(trxns_btctest)
        from bit.network import NetworkAPI
        NetworkAPI.broadcast_tx_testnet(sign_trxns_btctest)       
        return tx_hex