from transaction import Transaction


class TransactionService:
    transactions = []

    @classmethod
    def create_transaction(cls, sender_bill, receiver_bill, amount):
        transaction = Transaction(sender_bill, receiver_bill, amount)
        cls.transactions.append(transaction)
        return transaction

    @classmethod
    def get_transactions(cls):
        return cls.transactions

    @classmethod
    def get_transaction_by_transaction_id(cls, transaction_id):
        for transaction in cls.transactions:
            if transaction.id == transaction_id:
                return transaction

    @classmethod
    def get_transactions_by_client_id(cls, client_id):
        return [transaction for transaction in cls.transactions
                if client_id in [transaction.sender_bill.client.id, transaction.receiver_bill.client.id]]
