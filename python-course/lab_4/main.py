from datetime import datetime


class Bank:
    bills = []
    transactions = []

    @classmethod
    def open_bill(cls, client, currency, amount):
        bill = Bill(client, currency, amount)
        cls.bills.append(bill)

    @classmethod
    def create_transaction(cls, sender_bill, receiver_bill, amount):
        transaction = Transaction(sender_bill, receiver_bill, amount)
        cls.transactions.append(transaction)


class Client:
    def open_bill(self, currency, amount):
        Bank.open_bill(self, currency, amount)

    def transfer_money(self, owner_bill, receiver_bill, amount):
        pass


class Bill:
    next_id = 1000

    def __init__(self, client, currency, amount):
        self.id = str(Bill.next_id)
        Bill.next_id += 1
        self.client = client
        self.__currency = currency
        self.__amount = amount

    def recharge(self, amount):
        self.__amount += amount

    def withdraw(self, amount):
        if self.__amount < amount:
            raise Exception("You don't have enough money.")

        self.__amount -= amount

    @property
    def currency(self):
        return self.__currency

    @property
    def amount(self):
        return self.__amount


class Transaction:
    def __init__(self, sender_bill, receiver_bill, amount):
        self.sender_bill = sender_bill
        self.receiver_bill = receiver_bill
        self.amount = amount
        self.state = "init"
        self.creation_ts = datetime.now()
        self.last_modified = self.creation_ts

    def accept(self):
        self.state = "accepted"
        self.last_modified = datetime.now()

    def reject(self):
        self.state = "rejected"
        self.last_modified = datetime.now()

if __name__ == "__main__":
    print("Bank is open.")

    c1 = Client()
    c1.open_bill("RU", 1000)

    с2 = Client()
    с2.open_bill("RU", 0)

    c1.transfer_money("1000", "1001", 500)
