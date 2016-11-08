from datetime import datetime


class ClientNotFoundException(Exception):
    pass


class ClientAlreadyExists(Exception):
    pass


class Bank:
    clients = []
    transactions = []

    @classmethod
    def _get_client_or_none(cls, client_id):
        for client in cls.clients:
            if client.client_id == client_id:
                return client

    @classmethod
    def add_new_client(cls, client_id):
        if Bank._get_client_or_none(client_id):
            raise ClientAlreadyExists

        client = Client(client_id)
        cls.clients.append(client)

    @classmethod
    def get_clients(cls):
        return cls.clients

    @classmethod
    def get_client(cls, client_id):
        client = Bank._get_client_or_none(client_id)

        if not client:
            raise ClientNotFoundException

        return client

    @classmethod
    def create_transaction(cls, sender_bill, receiver_bill, amount):
        transaction = Transaction(sender_bill, receiver_bill, amount)
        cls.transactions.append(transaction)

    @classmethod
    def convert(cls, from_currency, to_currency, amount):
        return amount


class Client:
    def __init__(self, client_id):
        self.client_id = client_id
        self.bills = []

    def open_bill(self, currency, amount):
        bill = Bill(self, currency, amount)
        self.bills.append(bill)

    def get_bill(self, bill_id):
        for bill in self.bills:
            if bill.id == bill_id:
                return bill

        raise Exception("Bill not found.")


class Bill:
    next_id = 1000

    def __init__(self, client, currency, amount):
        self.id = str(Bill.next_id)
        Bill.next_id += 1
        self.client = client
        self.__currency = currency
        self.__amount = amount
        self.__blocked = 0

    def recharge(self, amount):
        self.__amount += amount

    def withdraw(self, amount):
        if self.__amount < amount:
            raise Exception("You don't have enough money.")

        self.__amount -= amount

    def transfer_money(self, receiver_bill_id, amount):
        if receiver_bill_id == self.id:
            raise Exception("Owner & receiver bills should not be equal.")

        if not Bank.is_bill_exists(receiver_bill_id):
            raise Exception("Receiver bill is NOT exists.")
        
        self.block_money(amount)
        transaction = Transaction(self.id, receiver_bill_id, amount)
        return transaction.id

    def block_money(self, amount):
        self.__blocked += amount

    @property
    def currency(self):
        return self.__currency

    @property
    def amount(self):
        return self.__amount - self.__blocked


class Transaction:
    next_id = 100000

    def __init__(self, sender_bill_id, receiver_bill_id, amount):
        self.id = Transaction.next_id
        Transaction.next_id += 1
        self.sender_bill = Bank.get_bill(sender_bill_id)
        self.receiver_bill = Bank.get_bill(receiver_bill_id)
        self.amount = amount
        self.state = "init"
        self.creation_ts = datetime.now()
        self.last_modified = self.creation_ts

    def accept(self):
        # todo: зачислить деньги получателю
        self.state = "accepted"
        self.last_modified = datetime.now()

    def reject(self):
        # todo: вернуть деньги отправителю
        self.state = "rejected"
        self.last_modified = datetime.now()


class AdminPanel:
    @staticmethod
    def add_new_client(client_id):
        Bank.add_new_client(client_id)

    @staticmethod
    def open_bill(client_id, currency, money=0):
        client = Bank.get_client(client_id)

        client.open_bill(currency, money)

    @staticmethod
    def show_bills(client_id):
        client = Bank.get_client(client_id)

        print("Bills of " + client)
        for bill in client.bills:
            print(bill)

    @staticmethod
    def show_all_money():
        pass

    @staticmethod
    def show_unaccepted_transactions():
        pass

    @staticmethod
    def accept_transaction(transaction_id):
        pass

    @staticmethod
    def reject_transaction(transaction_id):
        pass


class ClientPanel:
    def transfer(self, sender_bill, receiver_bill, amount):
        pass

    def show_money(self, bill):
        pass

    def show_history_of_transactions(self):
        pass


if __name__ == "__main__":
    print("Bank is open.")
