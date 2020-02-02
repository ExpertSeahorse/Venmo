import Venmo
import json


class GroupJson:
    """
    This class handles the Groups JSON in the project directory
    """
    def __init__(self, save_file="Groups"):
        # Imports the saved dict of groups for use in class methods
        with open(save_file, "r") as file:
            try:
                self.group = json.load(file)
            except json.decoder.JSONDecodeError:
                self.group = {}
        self.print_dict(self.group)

    @staticmethod
    def print_dict(dic):
        """
        Prints out a dictionary
        :param dic:
        :return:
        """
        for title, names in dic.items():
            print("{}:\t{}".format(title, names))

    def group_builder(self):
        """
        Adds or replaces a group
        :return:
        """
        # Gets the title
        print("Enter a new group name: ")
        title = input().capitalize()

        # Adds names
        print("Enter the usernames of the people add to the group or enter (done) to finish")
        names = []
        while True:
            name = input()
            # handles quit
            if name.lower() == "done":
                if names is False:
                    print("No names chosen yet!")
                    continue
                else:
                    break
            # ensures that all names start with @
            elif name[0] != '@':
                name = '@' + name
            names.append(name)

        # Sets the name of the group
        self.group[title] = names

        # Prints out the new group
        self.print_dict(self.group)

        # Saves the new json of groups into save file
        with open("Groups", 'w') as file:
            json.dump(self.group, file, indent=2)


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


def venmo():
    """
    Sends the TotalSplitter to targets through venmo
    :return:
    """
    def group():
        """
        Handles requesting a group of preloaded usernames
        :return:
        """
        # Loads the group JSON
        with open("Groups", 'r') as file:
            groups = json.load(file)
        GroupJson.print_dict(groups)

        # Fills the venmo function with usernames from a group
        print("\nEnter the title of the group you want to pay/charge")
        title = input().capitalize()
        return groups[title]

    # Get transaction type
    print("Enter (1) for charge and (0) for payment")
    kind = int(input())  # kind of transaction

    # Collect names
    names = []
    print("Enter the usernames of the people to charge/pay, enter (group) if you want to use a group"
          ", or enter (done) to finish")
    while True:
        name = input()
        # Handles quitting
        if name.lower() == "done":
            if names is False:
                print("No names chosen yet!")
                continue
            else:
                break
        # Handles groups
        elif name.lower() == "group":
            names = group()
            break
        # Ensures that all names start with an @
        elif name[0] != '@':
            name = '@' + name

        names.append(name)

    # Confirms the list
    print("\n"*10)
    print("You are {}:".format("charging" if kind else "paying"))
    for name in names:
        print(name)
    print()

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
                Venmo.charge_money(final, target, message)
        # if payment
        else:
            print("Press Enter to pay", list_to_string(names), final_str, "each.")
            input()
            for target in names:
                Venmo.send_money(final, target, message)

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


def list_to_string(arr):
    """
    Converts a list into a comma delineated string ending with "and"
    :param arr:
    :return:
    """
    out = ""
    for i in range(len(arr)-1):
        out += str(arr[i]) + ", "
    out += "and " + str(arr[i+1])
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
    venmo()

print("Press Enter to close...")
input()
