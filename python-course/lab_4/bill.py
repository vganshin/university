from transaction_service import TransactionService


class Bill:
    next_id = 1000

    def __init__(self, client, currency, amount):
        self.id = str(Bill.next_id)
        Bill.next_id += 1
        self.client = client
        self.currency = currency
        self.amount = amount
        self.blocks = {}

    def recharge(self, amount):
        self.amount += amount

    def withdraw(self, amount):
        if self.amount < amount:
            raise Exception("Don't have enough money.")

        self.amount -= amount

    def block_money_by_transaction(self, amount, transaction_id):
        self.blocks[transaction_id] = amount
        self.withdraw(amount)

    @property
    def amount_with_blocks(self):
        return self.amount + sum(self.blocks.values())

    def transfer_money(self, receiver_bill, amount):
        if receiver_bill == self.id:
            raise Exception("Owner & receiver bills should not be equal.")

        if receiver_bill is None:
            raise Exception("Receiver bill is NOT exists.")

        return TransactionService.create_transaction(self, receiver_bill, amount)

    def __str__(self):
        s = "Счёт №{}: {:.2f}{}".format(self.id, self.amount, self.currency)
        if self.blocks:
            s += " (+{:.2f}{} заблокировано)".format(sum(self.blocks.values()), self.currency)
        return s

