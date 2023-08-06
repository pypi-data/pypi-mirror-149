# Dojo-py

A very incomplete interface to your Samourai Dojo REST API. 

- All requests are proxied through SOCKS to your Dojo's Tor hidden service URL 
- Authenticated calls to the Dojo make use of the `Authorization` HTTP header with the `Bearer` scheme.

## Get Started
### Install from pip
```python
pip install dojo-py
```

### Setup
```python
## Import the package
from pydojo import pyDojo

## Set two variables for onion address and API key.
## Both can be obtained from your Dojo Maintenance Tool
## or your pairing QR code
onion = 'mytorv3onionaddress.onion'
apikey = 'mydojoapikey'
pd = pyDojo(onion, apikey)
```

### Status
```python
## Get Dojo Status
## NOTE: this call requires use of the Admin Key instead 
## of the API Key
pd.get_status()
```
### Fees
```python
## Get current miner fee rates as per your Dojo
pd.get_fees()
```
### Block header
```python
## Get information about a certain block header
blockhash = '0000000000000000000a0c3d6bbc0168932613d550cb7875459b6d37ae088211'
pd.get_block_header(blockhash)
```

### Add extended public key to your Dojo
```python
## Add a new extended public key to your Dojo
## You must tell the Dojo how to derive addresses
## if it is a Segwit enabled public key. `bip49` or `bip84`
## You also need to supply a method of import. Valid values 
## are `new` and `restore`.

xpub = 'ypub...'
method = 'restore'
segwit = 'bip49'

pd.add_xpub(xpub=xpub, type=method, segwit=segwit)
```

### XPUB Info
```python
## Get transactions for a given extended public key tracked
## by your Dojo
xpub = 'xpub...'
pd.get_xpub(payload)
```

### Transactions
```python
## Get transactions for a given extended public key or loose address
payload = ('bc1q...', '1Gef...', 'xpub...', 'ypub...', 'zpub...')
pd.get_transactions(payload)
```

### Transaction
```python
## Get transactions info for a txid
transaction = '6d2c2187169c7e85191edeea9d1db732abdefd14c7f1788d999e14b3096f8476'
pd.get_transaction(transaction)
```

### PushTx
```python
## Push a signed transaction to the network using your Dojo node
tx_hex = 'long_hex_string'
pd.push_transaction(tx_hex)
```

### Wallet info
```python
## Request details about a collection of HD accounts and/or 
## loose addresses and/or pubkeys (derived in 3 formats P2PKH, 
## P2WPKH/P2SH, P2WPKH Bech32) including a list of unspent 
## transaction outputs.
payload = ('bc1q...', '1Gef...', 'xpub...', 'ypub...', 'zpub...')
pd.get_wallet(payload)
```