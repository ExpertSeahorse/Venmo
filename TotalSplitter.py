import os
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


def list_to_string(arr):
    out = ""
    for i in range(len(arr)-1):
        out += arr[i] + ", "
    out += "and " + arr[i]
    return out


def venmo_configure():
    """
    status = subprocess.run("venmo status", capture_output=True)
    status = str(status.stdout, 'utf-8')
    i = status.index(':')
    age2 = datetime.strptime(status[i-13:i+3], "%Y-%m-%d %H:%M")
    now = datetime.now()
    delta = now - age2
    total_seconds = delta.seconds + (delta.days*3600*24)
    print(total_seconds)
    #if delta.seconds > 1200:
    """
    print("Type \"venmo configure\" to refresh your login information")
    os.system("start cmd /K cd C:\\Users\\dtfel\\PycharmProjects\\Venmo")


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

# Venmo integration
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
        elif name[0] != '@':
            name = '@' + name
        names.append(name)
    print("Enter a message for the order:")
    message = input()
    while True:
        if kind:
            print("Press Enter to charge", list_to_string(names), final_str, "each.")
            input()
            for target in names:
                venmo.payment.charge(target, final, message)
        else:
            print("Press Enter to pay", list_to_string(names), final_str, "each.")
            input()
            for target in names:
                venmo.payment.pay(target, final, message)
        choice2 = ''
        if not choice2:
            print("Do you need to refresh your login? (y/n)")
            choice2 = input().lower()
            if choice2[0] == "y":
                venmo_configure()
                continue
        break

print("Press Enter to close...")
input()
