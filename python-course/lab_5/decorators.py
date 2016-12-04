import csv

START_ENUMERATE = 2
PASSPORT_LENGTH = 6
NUMBER_OF_MONTHS = 12
MIN_VALID_YEAR = 1990
DAYS_IN_NON_LEAP_YEAR = (0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
DAYS_IN_LEAP_YEAR = (None, 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
MONTHS = [
    None,
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December"
]


class NameNotValid(Exception):
    pass


class PassportNumberNotValid(Exception):
    pass


class BirthdayNotValid(Exception):
    pass


def validate_string(max_length=1):
    def _validate_string(func):
        def wrapper(self, value):
            if type(value) is not str:
                raise NameNotValid("Name should be a string.")

            if len(value) > max_length:
                raise NameNotValid("Name should be less than {} symbols.".format(max_length))

            func(self, value)

        return wrapper

    return _validate_string


def validate_passport_number(func):
    def wrapper(self, value):
        if type(value) is not str:
            raise PassportNumberNotValid("Passport number should be a string.")

        if len(value) != PASSPORT_LENGTH:
            raise PassportNumberNotValid("Name should have {} symbols.".format(PASSPORT_LENGTH))

        if not 100000 <= int(value) <= 999999:
            raise PassportNumberNotValid("Passport number should be in range from 100000 to 999999.")

        func(self, value)

    return wrapper


def validate_birthday(func):
    def wrapper(self, value):
        if type(value) is not str:
            raise BirthdayNotValid("Birthday should be a string.")

        import re

        matched_date = re.match(r'^([0-9]{2})\.([0-9]{2})\.([0-9]{4})$', value)

        if not matched_date:
            raise BirthdayNotValid("Birthday should be in format DD.MM.YYYY.")

        day, month, year = matched_date.groups()
        day, month, year = int(day), int(month), int(year)

        days_in = DAYS_IN_NON_LEAP_YEAR
        if year % 4 == 0:
            days_in = DAYS_IN_LEAP_YEAR

        if year < MIN_VALID_YEAR:
            raise BirthdayNotValid("Year should be greater than {}".format(MIN_VALID_YEAR))

        if not 1 <= month <= NUMBER_OF_MONTHS:
            raise BirthdayNotValid("There are {} every year.".format(NUMBER_OF_MONTHS))

        if not 1 <= day <= days_in[month]:
            raise BirthdayNotValid("There are {} days in {} {}. Not {}."
                                   .format(days_in[month], MONTHS[month], year, day))

        from datetime import date
        today = date.today()

        if year > today.year \
                or year == today.year and month > today.month \
                or year == today.year and month == today.month and day > today.day:
            raise BirthdayNotValid("Can't register Person from future. Even if (s)he will be child of Marty McFly.")

        func(self, value)

    return wrapper


class Person:
    __name = None
    __passport_number = None
    __birthday = None

    def __init__(self, name, passport_number, birthday):
        self.name = name
        self.passport_number = passport_number
        self.birthday = birthday

    @property
    def name(self):
        return self.__name

    @name.setter
    @validate_string(max_length=20)
    def name(self, value):
        self.__name = value

    @property
    def passport_number(self):
        return self.__passport_number

    @passport_number.setter
    @validate_passport_number
    def passport_number(self, value):
        self.__passport_number = value

    @property
    def birthday(self):
        return self.__birthday

    @birthday.setter
    @validate_birthday
    def birthday(self, value):
        self.__birthday = value


table = csv.reader(open("persons.csv"))

next(table)

for i, data in enumerate(table, START_ENUMERATE):
    try:
        Person(*data)
    except NameNotValid as e:
        print('Error in line {}, NAME column: "{}"'.format(i, e))
    except PassportNumberNotValid as e:
        print('Error in line {}, PASSPORT_NUMBER column: "{}"'.format(i, e))
    except BirthdayNotValid as e:
        print('Error in line {}, BIRTHDAY column: "{}"'.format(i, e))
    except Exception:
        raise
