# Fishcake Box

## Requirements

1. Python 3
2. pytezos [pip install pytezos]

These scripts have been tested on **Ubuntu 20.10**

## Contracts

There are 2 contracts :

1. Fishcake Token : This is a FA2 contract that uses a modified version of the [FA2 smartpy template](https://smartpy.io/ide?template=FA2.py)
2. Fishcake Box : This contract enables users to redeem a fixed amount of `Fishcake Tokens`

### Setup SmartPy CLI

```sh
sh <(curl -s https://smartpy.io/cli/install.sh)
```

### Test Contracts

```sh
# test fishcake contract
~/smartpy-cli/SmartPy.sh test contracts/fishcake.py contracts/test-tmp

# test fishcake box contract
~/smartpy-cli/SmartPy.sh test contracts/fishcakeBox.py contracts/test-tmp
```

### Deploy Contracts

`contract/deploy.py` script will deploy and setup the contracts, edit this script to make changes to the default settings:

```py
default_rpc = "delphinet"  # rpc address or pytezos network name
default_pk = ""  # your tezos account private keys
default_supply = 100000  # total Fishcake Token supply
default_redeem_amt = 100  # constant redeem amount for the Fishcake Box
default_fsck_box_fund = 10000  # initial tokens funded to Fishcake Box
```

Once you have edited the constants you can run the script from the root of the repository:

```sh
python3 contract/deploy.py
```

It will deploy the contracts and perform the necessary txs after which it will display the contract addresses:

```sh
[!] Details :

-- Fishcake Token Address : KT1....
-- Fishcake Box Address : KT1....
```
