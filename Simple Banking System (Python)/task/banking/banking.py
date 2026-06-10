import random
import string
import sys

import database

class Account:

    def __init__(self):
        self.card_num = self.generate_card_number()
        self.card_pin = self.generate_pin()
        self.balance = 0

    def generate_card_number(self):
        while True:
            card_num = '400000' + ''.join(random.choices(string.digits, k=10))

            if self.verify_card_num(card_num):
                return card_num

    # static method is a utility/helper function that does not use self
    # (instance or class data)
    # Only work with input or return values
    @staticmethod
    def generate_pin():
        card_pin = f"{random.randint(0, 9999):04}"
        return card_pin

    @staticmethod
    def verify_card_num(card):
        digits = [int(d) for d in card if d.isdigit()]
        # Reverse the list to start from the rightmost digit
        digits = digits[::-1]
        checksum = 0

        for i, digit in enumerate(digits):
            # Double every second digit (odd indices in a 0-indexed reversed list)
            if i % 2 == 1:
                doubled = digit * 2
                # If doubled value > 9, subtract 9
                checksum += doubled if doubled <= 9 else doubled - 9
            else:
                checksum += digit

        return checksum % 10 == 0
    

class Bank:
    def __init__(self):
        self.account = None  # currently selected account
        self.pin = None

    @staticmethod
    def print_main_menu():
        print("1. Create an account\n"
              "2. Log into account\n"
              "0. Exit")

    @staticmethod
    def create_account():
        act = Account()

        database.insert_account(
            act.card_num,
            act.card_pin
        )

        print("\nYour card has been created"
              "\nYour card number:\n" +
              act.card_num + "\nYour card PIN:\n" +
              act.card_pin + "\n")

    # @staticmethod
    def balance_menu(self):
        while True:
            print("1. Balance\n"
                  "2. Add income\n"
                  "3. Do transfer\n"
                  "4. Close account\n"
                  "5. Log out\n"
                  "0. Exit"
                  )

            match int(input()):
                case 1:
                    print(self.account)
                    print(f"\nBalance: {database.get_balance(self.account)} \n")
                case 2:
                    print("\nEnter income:")
                    income = int(input())
                    database.add_money(income, self.account)
                    print("\nIncome was added!\n")

                case 3:
                    # Accounts - 4000004729772883 1505, 4000009132293740 4519
                    self.transfer_money()

                case 4:
                   database.delete_account(self.account)
                   print("The account has been closed!\n")
                   break
                case 5:
                    print("\nYou have successfully logged out!\n")
                    break
                case 0:
                    print("\nBye!")
                    sys.exit(0)

    def transfer_money(self):
        valid_account = Account()
        current_account = self.account

        print("Transfer\nEnter card number")
        to_account = input()

        if not valid_account.verify_card_num(to_account):
            print("Probably you made a mistake in the card number. Please try again!\n")
        elif not database.get_card_number(to_account):
            print("Such a card does not exist.\n")
        else:
            print("Enter how much money you want to transfer:")
            transfer_amount = int(input())

            if transfer_amount > database.get_balance(current_account):
                print("Not enough money!")
            else:
                database.transfer_balance(current_account, to_account, transfer_amount)
                print("Success!")

    def login(self):
        # Prompt to enter account info
        print("\nEnter your card number:")
        enter_card_num = input()
        print("Enter your PIN:")
        enter_pin = input()

        account = database.find_account(enter_card_num, enter_pin)

        if account:
            self.account = enter_card_num
            self.pin = enter_pin

            print("\nYou have successfully logged in!\n")
            self.balance_menu()
        else:
            print("\nWrong card number or PIN!\n")

    def run(self):
        while True:
            self.print_main_menu()
            choice = int(input())

            match choice:
                case 1:
                    self.create_account()
                case 2:
                    self.login()
                case 0:
                    print("\nBye!")
                    break

def main():
    database.create_table() # initialize table
    bank = Bank()
    bank.run()

if __name__ == "__main__":
    main()
