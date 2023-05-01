import pandas as pd
from blockcypher import get_address_full

#Get BTC Transaction from blockcypher

def scrap_btc_transaction(file_address, file_transaction):
    """
    :Function: Get the transaction from the btc address
    :param file_address: file where the btc address is stored
    :type file_address: str
    :param file_transaction: file where the transaction will be stored
    :type file_address: str
    :return: None
    """
    with open(file_transaction, 'w') as f:
        df = pd.read_csv(file_address, header=None, names=['add'])
        for address in df['add']:
            try:
                transactions = get_address_full(address)
                for transaction in transactions['txs']:
                    for add in transaction['addresses']:
                        if add != address:
                            f.write("%s,%s,%s\n" % (address, add, transaction['total']))
            except:
                print('error', address)

file_address = '' #file where the btc address is stored
file_transaction = '' #file where the transaction will be stored

# uncomment to run
# scrap_btc_transaction(file_address, file_transaction)