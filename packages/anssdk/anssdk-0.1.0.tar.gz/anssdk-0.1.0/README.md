# PY-ANS-SDK
A python sdk to resolve .algo names and perform name operations on ANS .algo names.

## Documentation


Install Package

**`pip`**
```
pip3 install anssdk
```

## Import
```
import anssdk.resolver as resolver
```

## Setup

```
algod_client = "" # set up your algodV2 client
algod_indexer = "" # set up your algod indexer

#indexer is not required if the intention is to only resolve .algo names, but it is required to view the names owned by an algorand wallet address
#indexer and client must point to mainnet

resolver_obj = resolver.ans_resolver(client)
(OR)
resolver_obj = resolver.ans_resolver(client, indexer)
```


## Resolve .algo name
Resolve .algo name to get the address of the owner.
```
name = "ans.algo"

name_info = resolver_obj.resolve_name(name)

if(name_info["found"] is True):
    print(name_info["address"])
else:
    print('Name not registered')    
```

## Get names owned by an address
This method gets all the names owned by an Algorand address in reverse chronological order of registration.
```
address="" # provide an algorand wallet address here

# optional parameters
socials=True # return socials along with domain owner information
metadata=True # return metadata along with domain owner information
limit=1 # limit the number of domains to be retrieved 

names = resolver_obj.get_names_owned_by_address(address, socials, metadata, limit)

# Returns an array of names owned by the address
# Names appear in a reverse chronological order (names[0] returns recently purchased name)

if(len(names) > 0):
    for domain in names:
        print(domain['name'])
        # domain['socials'] and domain['metadata'] can be retrieved as well
else:
    print('No names registered by given address')        
```

## Register a new name

Import 
```
import anssdk.transactions as transactions
```
Setup
```
algod_client = "" #setup your algodv2 client
sdk = transactions.Transactions(algod_client)
```
Prepare name registration transactions
```
name_to_register = "" #.algo name to register
address = "" # owner's algorand wallet address
period = 0 # duration of registration

try:

    name_registration_txns = sdk.prepare_name_registration_transactions(name_to_register, address, period)

    # Returns a tuple of size two
    # name_registration_txns[0] includes the array of transactions
    # name_registration_txns[1] has the logic sig

    if(len(name_registration_txns[0]) == 2):

        # Lsig account previous opted in (name expired)
        # Sign both transactions
        # Send all to network

    elif(len(name_registration_txns[0]) == 4):

        # name_registration_txns[2] must be signed by the sdk
        # Sign name_registration_txns index 0,1,3
        # Submit transactions as a group

        signed_group_txns = []

        txns = [
            signed_group_txns[0],
            signed_group_txns[1],
            signed_group_txns[2], # must be signed by the sdk
            signed_group_txns[3]
        ]

        # send to network

except:
    pass
```

## Update Name (Set name properties)
This method returns transactions to set the social media handles of a domain name

```
try:

    name = "" #.algo name
    address = "" # owner's algorand address

    edited_handles = {
        'discord': '',
        'github': ''
    }

    update_name_property_txns = sdk.prepare_update_name_property_transactions(name, address, edited_handles)

    # Returns an array of transactions
    # Sign each and send to network

except:
    pass
```

## Renew Name
Retrieve transactions to renew a name. The ANS registry currently supports renewal only by the owner hence the transactions will fail if the input address is not the current owner of the name.

```
try:

    name = "" # .algo name
    owner = "" # owner address
    period = 0 # period for renewal

    name_renewal_txns =  sdk.prepare_name_renewal_transactions(name, owner, period)

    # Returns an array of transactions 
    # Sign each and send to network

except:
    pass
```

## Initiate transfer
This method returns a transaction to initiate name transfer. The owner is required to set the price for transfer and the recipient's algorand account address.

```
try:
    
    name = "" # .algo name to initiate transfer
    owner = "" # current owner
    new_owner = "" # new owner's address
    price = 0 # price at which the seller is willing to sell the name

    name_transfer_transaction = sdk.prepare_initiate_name_transfer_transaction(name, owner, new_owner, price)

    # Returns a transaction to be signed by `owner` 
    # Sign and send to network

except:
    pass
```

## Accept transfer
Retrieve the transactions to complete the transfer by providing the current owner's address, the transfer recipient's address, and the price set by the owner
```
try:
    
    name = "" # .algo name to accept transfer
    owner = "" # current owner
    new_owner = "" # new owner's address
    price = 0 # price set in the previous transaction

    accept_name_transfer_txns = sdk.prepare_accept_name_transfer_transactions(name, new_owner, owner, price)

    # Returns an array of transactions to be signed by `newOwner`
    # Sign each and send to network

except:
    pass
```




