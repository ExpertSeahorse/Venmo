from datetime import datetime, timedelta
import venmo

# Venmo documentation: https://pypi.org/project/venmo/


def venmo_configure():
    """
    Checks if the token has expired and renews it if so.
    :return:
    """
    # Get the datetime the token was created
    status = venmo.cli.status(feldman=True)

    # Isolate the datetime and find the amount of time between then and now
    i = status.index(':')
    age = datetime.strptime(status[i-13:i+3], "%Y-%m-%d %H:%M")
    now = datetime.now()
    delta = now - age
    total_seconds = delta.seconds + (delta.days*3600*24)

    # If the token is older than a week old, renew the token
    if total_seconds > 6048005:
        venmo.auth.configure()


def send_money(amount, target, message):
    """
    Sends money to people with Venmo
    :param amount: The amount to send to the target
    :param target: The username of the person to receive the money
    :param message: The message for the transaction
    :return:
    """
    if target[0] != '@':
        target = '@' + target

    final_amount = str(round(amount, 2))
    venmo_configure()
    venmo.payment.pay(target, final_amount, message)


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

    final_amount = str(round(amount, 2))
    venmo_configure()
    venmo.payment.charge(target, final_amount, message)


if __name__ == '__main__':
    venmo_configure()
    # print(venmo.payment.charge("@Kristen-Lockhart-4", 0.01, "Python testing"))
