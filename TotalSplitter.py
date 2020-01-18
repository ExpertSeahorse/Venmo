import Venmo
import venmo


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
# Print out the total sum and split for the party
total = round(sum(total_amounts), 2)
print("How many ways do you want to split $" + str(total) + "?")
party_size = int_input()

print("\nThe total amount owed per person is:")
final = round(total/party_size, 2)
final_str = str("$" + str(final))
print(final_str)

print("Enter (yes) to send the payments automatically with Venmo?")
choice = input()

if choice[0] == 'y':
    print("Enter (1) for charge and (0) for payment")
    kind = int(input())  #kind of transaction
    names = []
    i = 0
    print("Enter the usernames of the people to charge/pay, enter (stop) to finish")
    while True:
        name = input()
        if name.lower() == "stop":
            break
        names.append(name)
    print("Enter a message for the order:")
    message = input()
    while True:
        if kind:
            print("Press Enter to charge", *names, final_str, "each.")
            input()
            for target in names:
                venmo.payment.charge(target, final, message)
        else:
            print("Press Enter to pay", *names, final_str, "each.")
            input()
            for target in names:
                venmo.payment.pay(target, final, message)
        choice2 = '\0'
        if not choice2:
            print("Do you need to refresh the token? (y/n)")
            choice2 = input().lower()
            if choice2[0] == "y":
                Venmo.venmo_configure()
                continue
        break

print("Press Enter to close...")
input()
