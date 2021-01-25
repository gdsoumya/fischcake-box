# Fishcake Box

## Setup

This section guides you how to setup your env to run the scripts in this repository

[*] These scripts have been tested on **Ubuntu 20.10**

### Requirements

1. Python 3.8
2. virtualenv

### Clone Repo

```sh
git clone https://github.com/gdsoumya/fischcake-box

cd fischcake-box
```

### Create Virtual Env

```sh
virtualenv env

source env/bin/activate
```

### Install Requirements

```sh
pip install -r requirements
```

## Contracts

There are 2 contracts :

1. Fishcake Token : This is a FA2 contract that uses a modified version of the [FA2 smartpy template](https://smartpy.io/ide?template=FA2.py)
2. Fishcake Box : This contract enables users to redeem a fixed amount of `Fishcake Tokens`

### Setup SmartPy CLI [REQUIRED]

```sh
sh <(curl -s https://smartpy.io/cli/install.sh)
```

### Test Contracts

```sh
# test fishcake contract
~/smartpy-cli/SmartPy.sh test contract/contracts/fishcake.py contract/test-tmp

# test fishcake box contract
~/smartpy-cli/SmartPy.sh test contract/contracts/fishcakeBox.py contract/test-tmp
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

## CLI

The CLI uses these default values :

```
default_rpc = "delphinet"  # rpc address or pytezos network name
default_fsck_box_addr = "KT18mmFJu1vKN91ko8MmnvSW8kf8CstM7H4g"
default_fsck_token_addr = "KT1NdiBZcHJ6KxqTjkCztWXJw9VCZAxLzJUM"
```

The above can be configured by passing the required setting :

```sh
python cli/cli.py --help

Usage: cli.py [OPTIONS] COMMAND [ARGS]...

  CLI group

Options:
  --rpc <rpc-address>             rpc node to use
  --fishcake-box <contract-addr>  fishcake box contract address
  --fishcake-token <contract-addr>
                                  fishcake token contract address
  --help                          Show this message and exit.

Commands:
  has-redeemed    Check if user has redeemed tokens from Fishcake Box or not...
  token-balance   Check how many Fishcake Tokens user has ADDRESS is the...
  total-redeemed  Check the total redeemed tokens from Fishcake Box
```

The CLI util has 3 commands:

1. `total-redeemed` : This shows the total tokens redeemed from fishcake box contract
2. `has-redeemed` : This command takes the user address as an argument and shows whether the user has redeemed the token from fishcake box
3. `token-balance` : This command takes the user address as an argument and shows their fishcake token balance
