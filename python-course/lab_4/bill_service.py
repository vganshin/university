from bill import Bill


class BillService:
    bills = []

    @classmethod
    def create_bill(cls, client_id, currency, amount):
        bill = Bill(client_id, currency, amount)
        cls.bills.append(bill)
        return bill

    @classmethod
    def get_bills(cls):
        return cls.bills

    @classmethod
    def get_bill_by_bill_id(cls, bill_id):
        for bill in cls.bills:
            if bill.id == bill_id:
                return bill

    @classmethod
    def get_bill_by_client_id(cls, client_id):
        return [bill for bill in cls.bills if bill.client_id == client_id]