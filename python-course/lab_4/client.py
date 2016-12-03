from bill_service import BillService


class Client:
    def __init__(self, client_id):
        self.id = client_id
        self.bills = []

    def open_bill(self, currency, amount):
        bill = BillService.create_bill(self, currency, amount)
        self.bills.append(bill)

        return bill.id

    def get_bill(self, bill_id):
        for bill in self.bills:
            if bill.id == bill_id:
                return bill

        raise Exception("Bill not found.")


