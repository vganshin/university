from datetime import datetime
from exchanger import Exchanger


class Transaction:
    next_id = 100000

    def __init__(self, sender_bill, receiver_bill, amount):
        self.id = str(Transaction.next_id)
        Transaction.next_id += 1
        self.sender_bill = sender_bill
        self.receiver_bill = receiver_bill
        self.amount = amount
        self.state = "init"
        self.sender_bill.block_money_by_transaction(amount, self.id)

        self.creation_ts = datetime.now()
        self.last_modified = self.creation_ts

        if self.sender_bill.currency == self.receiver_bill.currency:
            self.accept()

    def accept(self):
        amount = self.calculate_exchange()
        self.receiver_bill.recharge(amount)
        self.state = "accepted"
        self.last_modified = datetime.now()

    def reject(self):
        self.sender_bill.recharge(self.amount)
        self.state = "rejected"
        self.last_modified = datetime.now()

    def calculate_exchange(self):
        return Exchanger.calculate_exchange(self.sender_bill.currency, self.receiver_bill.currency, self.amount)

    def __str__(self):
        s = "Транзакция №{}: с №{} на №{}, {:.2f}{}".format(
            self.id,
            self.sender_bill.id,
            self.receiver_bill.id,
            self.amount,
            self.sender_bill.currency
        )

        if self.sender_bill.currency != self.receiver_bill.currency:
            s += " ({:.2f}{})".format(
                self.calculate_exchange(),
                self.receiver_bill.currency
            )

        return s
