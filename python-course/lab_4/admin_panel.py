from client_service import ClientService
from transaction_service import TransactionService
from bill_service import BillService


class AdminPanel:
    @classmethod
    def add_new_client(cls, client_id):
        ClientService.create_client(client_id)

    @classmethod
    def open_bill(cls, client_id, currency, money=0):
        client = ClientService.get_client_by_client_id(client_id)

        client.open_bill(currency, money)

    @classmethod
    def show_bills_of_client(cls, client_id):
        client = ClientService.get_client_by_client_id(client_id)

        cls.print("Счета пользователя" + client)
        for bill in client.bills:
            cls.print(bill)
        cls.print()

    @classmethod
    def show_all_bills(cls, ):
        bills = BillService.get_bills()

        cls.print("Все счета в банке:")
        for bill in bills:
            cls.print("", bill)
        cls.print()

    @classmethod
    def show_all_money(cls):
        bills = BillService.get_bills()
        money = {}

        if not bills:
            cls.print("В банке еще нет ни одного счёта. :(\n")
            return

        for bill in bills:
            if not money.get(bill.currency):
                money[bill.currency] = 0
            money[bill.currency] += bill.amount

        cls.print("Все деньги в банке:")
        for currency, amount in money.items():
            cls.print("  {:.2f}{}".format(amount, currency))
        cls.print()

    @classmethod
    def show_unaccepted_transactions(cls, ):
        transactions = TransactionService.get_transactions()
        unaccepted_transactions = [transaction for transaction in transactions if transaction.state == "init"]

        if unaccepted_transactions:
            cls.print("Приостановленные транзакции:")
            for transaction in unaccepted_transactions:
                cls.print(" ", transaction)
        else:
            cls.print("Приостановленных транзакций нет.")

        cls.print()

    @classmethod
    def accept_transaction(cls, transaction_id):
        transaction = TransactionService.get_transaction_by_transaction_id(transaction_id)

        transaction.accept()

    @classmethod
    def reject_transaction(cls, transaction_id):
        transaction = TransactionService.get_transaction_by_transaction_id(transaction_id)

        transaction.reject()

    @classmethod
    def print(cls, *text):
        print("\033[91m", *text, "\033[0m")
