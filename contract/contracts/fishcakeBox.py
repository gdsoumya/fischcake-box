import smartpy as sp

FA2 = sp.import_script_from_url(
    "file:./contract/contracts/fishcake.py", name="Fishcake")


class FishcakeBox(sp.Contract):
    def __init__(self, amount, tokenAddr):
        self.init(users=sp.big_map(tkey=sp.TAddress, tvalue=sp.TBool),
                  redeemAmt=amount, tokensDistributed=0, fischake=tokenAddr)
        self.transfer = FA2.Batch_transfer(FA2.getFishcakeConfig())

    @sp.entry_point
    def redeem(self):
        sp.verify(~self.data.users.contains(sp.sender))
        self.data.users[sp.sender] = True
        self.data.tokensDistributed += self.data.redeemAmt
        contract = sp.contract(self.transfer.get_type(
        ), self.data.fischake, entry_point="transfer").open_some()
        payload = [self.transfer.item(from_=sp.self_address, txs=[sp.record(to_=sp.sender,
                                                                            amount=self.data.redeemAmt,
                                                                            token_id=0)])]
        sp.transfer(payload, sp.mutez(0), contract)

    @sp.view(sp.TBool)
    def hasRedeemed(self, address):
        sp.if self.data.users.contains(address):
            sp.result(True)
        sp.else:
            sp.result(False)


class TestConsumer(sp.Contract):
    def __init__(self, address):
        self.init(contract=address, redeemed=False)

    @sp.entry_point
    def callback(self, params):
        sp.set_type(params, sp.TBool)
        self.data.redeemed = params

    @sp.entry_point
    def checkRedeem(self, address):
        sp.set_type(address, sp.TAddress)
        contract = sp.contract(sp.TPair(sp.TAddress, sp.TContract(
            sp.TBool)), self.data.contract, entry_point="hasRedeemed").open_some()
        payload = sp.pair(address, sp.contract(
            sp.TBool, sp.self_address, entry_point="callback").open_some())
        sp.transfer(payload, sp.mutez(0), contract)


@sp.add_test(name="FishcakeBox")
def test():
    scenario = sp.test_scenario()
    scenario.h1("Fischcake Box")
    scenario.table_of_contents()
    admin = sp.test_account("Administrator")
    alice = sp.test_account("Alice")
    bob = sp.test_account("Bob")
    jack = sp.test_account("Jack")
    scenario.h2("Accounts")
    scenario.show([admin, alice, bob, jack])
    scenario.h2("Initializing Fishcake Token")
    c1 = FA2.Fishcake(admin.address, 10000)
    scenario += c1
    scenario.h2("Initial Minting")
    scenario.p("The administrator mints the initial tokens")
    scenario += c1.initialMint().run(sender=admin)
    scenario.h2("Initializing Fishcake Box")
    c2 = FishcakeBox(amount=1000, tokenAddr=c1.address)
    scenario += c2
    scenario.h2("Sending Tokens to Fishcake Box")
    scenario += c1.transfer(
        [
            c1.batch_transfer.item(from_=admin.address,
                                   txs=[
                                       sp.record(to_=c2.address,
                                                 amount=3000,
                                                 token_id=0)
                                   ])
        ]).run(sender=admin)
    scenario.verify(
        c1.data.ledger[c1.ledger_key.make(admin.address, 0)].balance
        == 7000)
    scenario.verify(
        c1.data.ledger[c1.ledger_key.make(c2.address, 0)].balance
        == 3000)
    scenario.h2("Redeem Tokens from Fishcake Box")
    scenario.h3("Successful Redeem")
    scenario += c2.redeem().run(sender=alice)
    scenario += c2.redeem().run(sender=bob)
    scenario.verify(
        c1.data.ledger[c1.ledger_key.make(alice.address, 0)].balance
        == 1000)
    scenario.verify(
        c1.data.ledger[c1.ledger_key.make(bob.address, 0)].balance
        == 1000)
    scenario.verify(
        c1.data.ledger[c1.ledger_key.make(c2.address, 0)].balance
        == 1000)
    scenario.h3("Unsuccessful Redeem")
    scenario.p("User has already redeemed")
    scenario += c2.redeem().run(sender=alice, valid=False)
    scenario += c2.redeem().run(sender=bob, valid=False)
    scenario.p("Insufficient Balance of Fishcake Box")
    scenario += c2.redeem().run(sender=jack)
    # smartpy currently cannot handle recursive errors hence this test case has been commented
    # scenario += c2.redeem().run(sender=admin, valid=False)
    scenario.h2("Calling View")
    consumer = TestConsumer(c2.address)
    scenario += consumer
    scenario += consumer.checkRedeem(alice.address)
    scenario.verify(
        consumer.data.redeemed == True)
    scenario += consumer.checkRedeem(bob.address)
    scenario.verify(
        consumer.data.redeemed == True)
    scenario += consumer.checkRedeem(jack.address)
    scenario.verify(
        consumer.data.redeemed == True)
    scenario += consumer.checkRedeem(admin.address)
    scenario.verify(
        consumer.data.redeemed == False)
