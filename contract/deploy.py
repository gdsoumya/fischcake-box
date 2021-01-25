import os
from os.path import expanduser

from pytezos import Contract, pytezos
from pytezos.michelson.micheline import michelson_to_micheline

# constants
default_rpc = "delphinet"  # rpc address or pytezos network name
default_pk = ""  # your tezos account private keys
default_supply = 100000  # total Fishcake Token supply
default_redeem_amt = 100  # constant redeem amount for the Fishcake Box
default_fsck_box_fund = 10000  # initial tokens funded to Fishcake Box


pytezos = pytezos.using(shell=default_rpc, key=default_pk)
pub_key_hash = pytezos.key.public_key_hash()  # tezos address


def compile_contract(file: str, class_call: str) -> str:
    """
    Compile SmartPy contract in the file using the specified class call
    """
    print(f"Compiling {file}.py ....")
    exit_code = os.system(
        f"~/smartpy-cli/SmartPy.sh compile contract/contracts/{file}.py \"{class_call}\" contract/build")
    if exit_code != 0:
        raise Exception(f"Failed to compile Contract : {file}.py")


def deploy(file: str) -> None:
    """
    Deploy the compiled contract in the file
    """
    print(f"Deploying {file}.py ....")
    contract = Contract.from_file(f"contract/build/{file}_compiled.tz")
    contract_storage = {}

    with open(expanduser(f"contract/build/{file}_storage_init.tz")) as f:
        contract_storage = f.read().replace('\n', '')

    opg = pytezos.origination(
        contract.script(storage=contract.storage.decode(contract_storage))).autofill().sign().inject(_async=False)
    return opg['contents'][0]['metadata']['operation_result']['originated_contracts'][0]


def setup(token_addr: str, box_addr: str) -> None:
    """
    Setup the contracts, perform initial mint of FSCK tokens and 
    fund the fishcake box contract
    """
    print(f"\nSetting up Contracts....")
    tokenContract = pytezos.contract(token_addr)
    print(f"-- Performing Initial Mint to Admin : {pub_key_hash}")
    tokenContract.initialMint(None).inject(_async=False)
    print("-- Funding Fishcake Box Contract")
    tokenContract.transfer([{"from_": pub_key_hash, "txs": [
                           {"to_": box_addr, "token_id": 0, "amount": default_fsck_box_fund}]}]).inject(_async=False)


def init():
    """
    Main function that compiles, deploys and configures the contracts
    """
    try:
        compile_contract(
            "fishcake", f"Fishcake(sp.address('{pub_key_hash}'),{default_supply})")
        fishcake_addr = deploy("fishcake")
        print("\n")
        compile_contract(
            "fishcakeBox", f"FishcakeBox({default_redeem_amt}, sp.address('{fishcake_addr}'))")
        fishcake_box_addr = deploy("fishcakeBox")
        setup(fishcake_addr, fishcake_box_addr)
        print("\n\n[!] Details :\n")
        print(f"-- Fishcake Token Address : {fishcake_addr}")
        print(f"-- Fishcake Box Address : {fishcake_box_addr}")
    except Exception as e:
        print("Failed to originate Contracts : ", e)


if __name__ == '__main__':
    init()
