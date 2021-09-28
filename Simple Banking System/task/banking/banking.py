# Write your code here
import random
import sqlite3

print("1. Create an account")
print("2. Log into account")
print("0. Exit")

# initialize database

conn = sqlite3.connect("card.s3db")
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS card ( id integer, number text, pin text, balance integer default 0 );")
conn.commit()

user_input = int(input())

all_cards = {}
_id = 0
while user_input != 0:

    if user_input == 1:
        random_number = random.randint(0, 999999999)
        random_number = str(random_number)
        random_number = random_number.rjust(9, "0")
        random_number = "400000" + random_number
        control_sum = 0
        counter = 1
        for cha in random_number:
            cha = int(cha)
            if counter % 2 != 0:
                cha = cha * 2
            if cha > 9:
                cha = cha - 9
            control_sum = control_sum + cha
            counter = counter + 1

        if control_sum % 10 != 0:
            control_sum = str(control_sum)
            added_number = 10 - int(control_sum[1])
        else:
            added_number = 0
        card_number = random_number + str(added_number)

        random_pin = random.randint(0, 9999)
        random_pin = str(random_pin)
        random_pin = random_pin.rjust(4, "0")

        all_cards[card_number] = random_pin
        cur.execute("INSERT INTO card VALUES (" + str(_id) + ", '" + card_number + "', '" + random_pin + "', 0 );")
        conn.commit()
        _id = _id + 1
        print("Your card has been created")
        print("Your card number:")
        print(card_number)
        print("Your card PIN:")
        print(random_pin)

    if user_input == 2:
        entered_card_number = input("Please enter your card number: ")
        entered_pin = input("Please enter your pin: ")

        if entered_card_number in all_cards:
            if entered_pin == all_cards[entered_card_number]:
                print("You have successfully logged in!")

                print("1. Balance")
                print("2. Add income")
                print("3. Do transfer")
                print("4. Close account")
                print("5. Log out")
                print("0. Exit")

                logged_in_user_input = int(input())
                balance = 0
                while logged_in_user_input != 5:
                    if logged_in_user_input == 1:
                        cur.execute("SELECT balance FROM card WHERE number = '" + entered_card_number + "';")
                        conn.commit()
                        balance = cur.fetchone()[0]
                        print("Balance: " + str(balance))
                    elif logged_in_user_input == 2:
                        balance = balance + int(input("Enter income: "))
                        cur.execute("UPDATE card SET balance = " + str(balance) + " WHERE number = '" + entered_card_number + "';")
                        conn.commit()
                        print("Income was added!")
                    elif logged_in_user_input == 3:
                        transfer_card = input("Enter card number: ")

                        # check if card is valid for Luhn split last number
                        check_digit_of_card = transfer_card[-1]
                        card_number_front = transfer_card[0:-1]
                        i = 1
                        control_sum_card = 0
                        for num in card_number_front:
                            num = int(num)
                            if i % 2 != 0:
                                num = num * 2
                            if num > 9:
                                num = num - 9
                            control_sum_card = control_sum_card + num
                            i = i + 1

                        if control_sum_card % 10 != 0:
                            control_sum_card = str(control_sum_card)
                            added_number = 10 - int(control_sum_card[1])
                        else:
                            added_number = 0
                        if added_number == int(check_digit_of_card):
                            print("Valid Card Luhn!")
                            cur.execute("SELECT * FROM card WHERE number = '" + transfer_card + "';")
                            conn.commit()

                            if cur.fetchone() is not None:
                                print("Card found in DB!")
                                if transfer_card == entered_card_number:
                                    print("You can't transfer money to the same account!")
                                else:
                                    transfer_amount = input("Enter how much money you want to transfer:")
                                    if int(transfer_amount) > int(balance):
                                        print("Not enough money!")
                                    else:
                                        new_balance = 0
                                        cur.execute("SELECT balance FROM card WHERE number = '" + transfer_card + "';")
                                        conn.commit()
                                        new_balance = cur.fetchone()[0]
                                        new_balance = new_balance + int(transfer_amount)
                                        cur.execute("UPDATE card SET balance = " + str(new_balance) + " WHERE number = '" + transfer_card + "';")
                                        conn.commit()

                                        new_balance = 0
                                        cur.execute("SELECT balance FROM card WHERE number = '" + entered_card_number + "';")
                                        conn.commit()
                                        new_balance = cur.fetchone()[0]
                                        new_balance = new_balance - int(transfer_amount)
                                        cur.execute("UPDATE card SET balance = " + str(new_balance) + " WHERE number = '" + entered_card_number + "';")
                                        conn.commit()
                                        print("Success!")
                            else:
                                print("Such a card does not exist.")
                        else:
                            print("Probably you made a mistake in the card number. Please try again!")
                    elif logged_in_user_input == 4:
                        cur.execute("DELETE FROM card WHERE number = '" + entered_card_number + "';")
                        conn.commit()
                        print("The account has been closed!")
                    elif logged_in_user_input == 5:
                        break
                    elif logged_in_user_input == 0:
                        print("Bye!")
                        exit()
                    logged_in_user_input = int(input())
            else:
                print("Wrong PIN!")
        else:
            print("Wrong card number!")

    user_input = int(input())

print("Bye!")
