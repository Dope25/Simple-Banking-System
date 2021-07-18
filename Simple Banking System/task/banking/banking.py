import sqlite3
from random import randint

connection = sqlite3.connect('card.s3db')
cursor = connection.cursor()


def create_table_card():
    #  automatic ID generation thanks to INTEGER PRIMARY KEY
    cursor.execute('CREATE TABLE IF NOT EXISTS card ('
                   'id INTEGER PRIMARY KEY,'
                   'number TEXT,'
                   'pin TEXT,'
                   'balance INTEGER DEFAULT 0)')
    connection.commit()


def insert_card(card, pin):
    cursor.execute(f"INSERT INTO card (number, pin) VALUES ('{card}', '{pin}')")
    connection.commit()


def retrieve_pin(card):
    cursor.execute(f"SELECT pin FROM card WHERE number = {card}")
    return cursor.fetchone()


def verify_pin(card, pin):
    cursor.execute(f"SELECT pin == {pin} FROM card WHERE number = {card}")
    try:
        result, = cursor.fetchone()
        if result == 0:
            return False
        else:
            return True
    except TypeError:
        return False


def retrieve_balance(card):
    cursor.execute(f"SELECT balance FROM card WHERE number = {card}")
    result, = cursor.fetchone()
    return result


def card_exists(card):
    cursor.execute(f"SELECT number FROM card WHERE number = {card}")
    try:
        result, = cursor.fetchone()
        if result == card:
            return True
        else:
            return False
    except TypeError:
        return False


def close_connection(conn):
    connection.commit()
    conn.close()


def truncate_card():
    cursor.execute("DELETE FROM card")
    connection.commit()


def add_income(card, amount):
    cursor.execute(f"UPDATE card SET balance = balance + {amount} WHERE number = {card}")
    connection.commit()
    print("Income was added!")


def transfer_money(card, amount, destination_card):
    cursor.execute(f"UPDATE card SET balance = balance - {amount} WHERE number = {card}")
    cursor.execute(f"UPDATE card SET balance = balance + {amount} WHERE number = {destination_card}")
    connection.commit()


def close_account(card):
    cursor.execute(f"DELETE FROM card WHERE number = {card}")
    connection.commit()


# noinspection PyPep8Naming
class BankSystem:

    def __init__(self):
        self.cards = {}
        create_table_card()

    def create_account(self):
        while True:
            card = '400000' + str(randint(000000000, 999999999))
            card += self.luhn(card)
            PIN = str(randint(0000, 9999))
            if len(card) != 16 or len(PIN) != 4:
                continue
            if not card_exists(card):
                self.cards[card] = {"PIN": PIN, "Balance": 0}
                insert_card(card, PIN)
                break
        print("Your card has been created.")
        print(f"Your card number:\n{card}")
        print(f"Your card PIN:\n{PIN}\n")

    @staticmethod
    def luhn(card: str):
        summary = 0
        count = 0
        array = [int(x) for x in card]
        for x in array:
            if count % 2 == 0:
                array[count] = x * 2
            if array[count] > 9:
                array[count] -= 9
            summary += array[count]
            count += 1
        if summary % 10 == 0:
            return str(summary)
        else:
            return str(10 - summary % 10)

    def login(self):
        card: str = input("\nEnter your card number:\n")
        PIN: str = input("\nEnter your PIN:\n")
        try:
            if verify_pin(card, PIN):
                print("You have successfully logged in!\n")
                self.account(card)
            else:
                print("Wrong card number or PIN\n")
        except KeyError:
            print("Wrong card number or PIN\n")

    @staticmethod
    def account(card: str):
        while True:
            choice = input('\n1. Balance'
                           '\n2. Add income'
                           '\n3. Do transfer'
                           '\n4. Close account'
                           '\n5. Log out'
                           '\n0. Exit\n')
            if choice == "1":
                print(f"\nBalance: {retrieve_balance(card)}\n")
            elif choice == "2":
                amount = int(input("\nHow much?"))
                add_income(card, amount)
            elif choice == "3":
                print("\nTransfer")
                destination_card = input("Enter card number:\n")
                luhn_check_card = destination_card[:-1]
                if destination_card != luhn_check_card + BankSystem.luhn(luhn_check_card):
                    print("Probably you made a mistake in the card number. Please try again!")
                    continue
                if not card_exists(destination_card):
                    print("Such a card does not exist.")
                    continue
                if card == destination_card:
                    print("You can't transfer money to the same account!")
                    continue
                # if
                else:
                    amount = int(input("Enter how much money you want to transfer:\n"))
                    if amount > retrieve_balance(card):
                        print("Not enough money!")
                        continue
                    else:
                        transfer_money(card, amount, destination_card)
                        print("Success!")
            elif choice == "4":
                print("The account has been closed!")
                close_account(card)
                # return False
                break
            elif choice == "5":
                print("You have successfully logged out!")
                return
            elif choice == "0":
                print("Bye!")
                close_connection(connection)
                exit()
            else:
                print("Unknown option.\n")

    def menu(self):
        while True:
            choice: str = input("1. Create an account\n2. Log into account\n0. Exit\n")
            if choice == "1":
                self.create_account()
            elif choice == "2":
                self.login()
            elif choice == "0":
                print("Bye!")
                close_connection(connection)
                exit()
            else:
                print("Unknown option.")


# debug to run without BankSystem
# test_card = '4000008077150105'
# fail_card = '4000008061927251'
# test_pin = '3741'
# destination_card = '4000008061927252'
# BankSystem.account(test_card)
BankSystem().menu()

