import Venmo
import venmo
import json


def float_input():
    type_match = False
    while not type_match:
        strin = input()
        if strin.upper() == "DONE":
            break
        try:
            strin = float(strin)
        except ValueError:
            print("Please enter a valid amount of money")
        else:
            strin = str(strin)
            if len(strin[strin.index(".") + 1:]) > 2:
                print("Please enter a valid amount of money")
                continue
            type_match = True
            strin = float(strin)
    return strin


def int_input():
    type_match = False
    while not type_match:
        try:
            strin = int(input())
        except ValueError:
            print("Please enter a valid number of people")
        else:
            type_match = True
    return strin


def list_to_string(arr):
    out = ""
    for i in range(len(arr)-1):
        out += arr[i] + ", "
    out += "and " + arr[i]
    return out


total_amounts = []

# Collect first amount
print("Enter total on first receipt:")
total_amounts.append(float_input())
print("\n" * 5)

while True:
    # Display current list of amounts
    print("The current totals are:")
    for i, entry in enumerate(total_amounts):
        print(str(i+1) + ".\t$" + str(round(entry, 2)))
    print("Total amount: $" + str(round(sum(total_amounts), 2)))
    print("\nEnter the total from another receipt or enter \"DONE\" to continue:")

    # Collect another amount, or break if not a number
    t = float_input()
    try:
        t.upper() == "DONE"
    except AttributeError:
        pass
    else:
        break
    total_amounts.append(t)
    print("\n"*5)

print("\n"*10)
print("===============================================================================================================")

# Print out the total sum, split for the party, and return final amount due per person
total = round(sum(total_amounts), 2)
print("How many ways do you want to split $" + str(total) + "?")
party_size = int_input()

print("\nThe total amount owed per person is:")
final = round(total/party_size, 2)
final_str = str("$" + str(final))
print(final_str)

########################################################################################################################
# Venmo integration
print("Enter (yes) to send the payments automatically with Venmo?")
choice = input()

if choice[0].lower() == 'y':
    # Get transaction type
    print("Enter (1) for charge and (0) for payment")
    kind = int(input())  #kind of transaction

    # Collect names
    # TODO: Add list choices
    names = []
    i = 0
    print("Enter the usernames of the people to charge/pay, enter (done) to finish")
    while True:
        name = input()
        if name.lower() == "done":
            if names is False:
                print("No names chosen yet!")
                continue
            else:
                break
        elif name[0] != '@':
            name = '@' + name
        names.append(name)

    # Grab the message
    print("Enter a message for the order:")
    message = input()

    # Send the transaction
    while True:
        # if charge
        if kind:
            print("Press Enter to charge", list_to_string(names), final_str, "each.")
            input()
            for target in names:
                venmo.payment.charge(target, final, message)
        # if payment
        else:
            print("Press Enter to pay", list_to_string(names), final_str, "each.")
            input()
            for target in names:
                venmo.payment.pay(target, final, message)

        # if the token expired
        # TODO: determine the lifetime of the token and bake into the sending scripts
        choice2 = ''
        if not choice2:
            print("Do you need to refresh your login? (y/n)")
            choice2 = input().lower()
            if choice2[0] == "y":
                Venmo.venmo_configure()
                continue
        break

print("Press Enter to close...")
input()
