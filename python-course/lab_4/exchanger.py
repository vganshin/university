class Exchanger:
    exchange_rates = {}

    @classmethod
    def calculate_exchange(cls, from_currency, to_currency, amount):
        if from_currency == to_currency:
            return amount

        exchange_rate = cls.exchange_rates.get(from_currency, {}).get(to_currency)

        if exchange_rate is None:
            raise Exception("Can't calculate exchange from {} to {}.".format(from_currency, to_currency))

        return amount * exchange_rate

    @classmethod
    def set_exchange_rate(cls, from_currency, to_currency, exchange_rate):
        if not cls.exchange_rates.get(from_currency):
            cls.exchange_rates[from_currency] = {}

        cls.exchange_rates[from_currency][to_currency] = exchange_rate

        if not cls.exchange_rates.get(to_currency):
            cls.exchange_rates[to_currency] = {}

        cls.exchange_rates[to_currency][from_currency] = 1.0 / exchange_rate

