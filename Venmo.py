import subprocess
from datetime import datetime, timedelta
import os
import venmo


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


def send_money(amount, target, message):
    """
    Sends money to people with Venmo
    :param amount: The amount to send to the target
    :param target: The username of the person to recieve the money
    :param message: The message for the transaction
    :return:
    """
    if target[0] != '@':
        target = '@' + target
    command = "venmo pay "+target+" "+str(round(amount, 2))+" \""+message+"\""
    print(command)
    subprocess.call(command)


def charge_money(amount, target, message):
    """
    Requests money from people with Venmo
    :param amount:
    :param target:
    :param message:
    :return:
    """
    if target[0] != '@':
        target = '@' + target
    command = "venmo charge "+target+" "+str(round(amount, 2))+" \""+message+"\""
    subprocess.call(command)


if __name__ == '__main__':
    venmo_configure()
    venmo.payment.charge("@Pedro-Marquez1433", 0.01, "Python testing")
