from client_service import ClientService
from bill_service import BillService
from transaction_service import TransactionService


class ClientPanel:
    def __init__(self, client_id):
        self.client = ClientService.get_client_by_client_id(client_id)

    def transfer(self, from_bill_id, to_bill_id, amount):
        from_bill = self.client.get_bill(from_bill_id)
        to_bill = BillService.get_bill_by_bill_id(to_bill_id)
        from_bill.transfer_money(to_bill, amount)

    def show_bills(self):
        self.print("{}, Ваши счета:".format(self.client.id))
        for bill in self.client.bills:
            self.print(" ", bill)
        self.print()

    def show_bill(self, bill_id):
        bill = next((bill for bill in self.client.bills if bill.id == bill_id), None)

        self.print("{}, Ваш {}".format(self.client.id, bill))

    def show_history_of_transactions(self):
        transactions = TransactionService.get_transactions_by_client_id(self.client.id)

        self.print("{}, Ваша история транзакци:".format(self.client.id))
        for transaction in transactions:
            self.print("", transaction)
        print()

    @classmethod
    def print(cls, *text):
        print("\033[94m", *text, "\033[0m")
