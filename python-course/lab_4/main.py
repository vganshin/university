from admin_panel import AdminPanel
from client_panel import ClientPanel
from exchanger import Exchanger

if __name__ == '__main__':
    Exchanger.set_exchange_rate("£", "₽", 70)

    AdminPanel.add_new_client("pasha")

    AdminPanel.show_all_money()

    AdminPanel.open_bill("pasha", "£", 100)
    AdminPanel.open_bill("pasha", "₽", 100)

    AdminPanel.add_new_client("dron")
    AdminPanel.open_bill("dron", "₽", 100)

    pasha = ClientPanel("pasha")

    pasha.transfer("1000", "1002", 12)

    # pasha.transfer("1000", "1001", 88)
    #
    pasha.show_bills()
    #
    AdminPanel.show_unaccepted_transactions()
    AdminPanel.accept_transaction("100000")
    AdminPanel.show_unaccepted_transactions()

    pasha.show_bills()

    dron = ClientPanel("dron")

    pasha.transfer("1001", "1002", 100)

    dron.show_bills()

    dron.transfer("1002", "1000", 1000)

    # AdminPanel.accept_transaction("100002")

    pasha.show_bills()

    AdminPanel.show_all_money()

    AdminPanel.show_all_bills()

    pasha.show_history_of_transactions()

    AdminPanel.show_unaccepted_transactions()

    pasha.show_bill("1000")

    # ====

    # dron.show_bills()
    #
    # dron.transfer("1002", "1000", 1000)

