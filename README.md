# Fishcake Box

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
