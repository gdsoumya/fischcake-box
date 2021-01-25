import click
from pytezos import pytezos

# constants
default_rpc = "delphinet"  # rpc address or pytezos network name
default_fsck_box_addr = "KT18mmFJu1vKN91ko8MmnvSW8kf8CstM7H4g"
default_fsck_token_addr = "KT1NdiBZcHJ6KxqTjkCztWXJw9VCZAxLzJUM"
fishcake_box_addr = ""
fishcake_token_addr = ""

pytezos = pytezos.using(shell=default_rpc)


@click.group()
@click.option('--rpc', metavar="<rpc-address>", default=default_rpc, help='rpc node to use')
@click.option('--fishcake-box', metavar="<contract-addr>", default=default_fsck_box_addr, help='fishcake box contract address')
@click.option('--fishcake-token', metavar="<contract-addr>", default=default_fsck_token_addr, help='fishcake token contract address')
def cli(rpc, fishcake_box, fishcake_token):
    """
    CLI group
    """
    global pytezos, fishcake_box_addr, fishcake_token_addr
    pytezos = pytezos.using(shell=rpc)
    fishcake_box_addr = fishcake_box
    fishcake_token_addr = fishcake_token


@cli.command()
def total_redeemed():
    """
    Check the total redeemed tokens from Fishcake Box
    """
    global pytezos, fishcake_box_addr
    try:
        fsck = pytezos.contract(fishcake_box_addr)
        tokensDistributed = fsck.storage()["tokensDistributed"]
        click.echo(f"\n[✓] Total Tokens Distributed : {tokensDistributed}\n")
    except Exception as e:
        click.echo(f"\n[!] Encountered Error : {str(e)}\n", err=True)


@cli.command()
@click.argument("address")
def has_redeemed(address):
    """
    Check if user has redeemed tokens from Fishcake Box or not

    ADDRESS is the address of the user 
    """
    global pytezos, fishcake_box_addr
    try:
        fsck = pytezos.contract(fishcake_box_addr)
        fsck.big_map_get(f"users/{address}")
        click.echo(f"\n[✓] User {address} has redeemed the tokens\n")
    except Exception as e:
        if "not found" in str(e).lower():
            click.echo(f"\n[✓] User {address} has not redeemed the tokens\n")
        else:
            click.echo(f"\n[!] Encountered Error : {str(e)}\n", err=True)


@cli.command()
@click.argument("address")
def token_balance(address):
    """
    Check how many Fishcake Tokens user has

    ADDRESS is the address of the user
    """
    global pytezos, fishcake_token_addr
    try:
        fsck = pytezos.contract(fishcake_token_addr)
        balance = fsck.big_map_get(f"ledger/{address}")
        click.echo(f"\n[✓] User {address} Balance : {balance} FSCK\n")
    except Exception as e:
        if "not found" in str(e).lower():
            click.echo(f"\n[✓] User {address} Balance : 0 FSCK\n")
        else:
            click.echo(f"\n[!] Encountered Error : {str(e)}\n", err=True)


if __name__ == "__main__":
    cli()
