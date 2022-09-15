from datetime import datetime
import bColors
from tabulate import tabulate
import os
import Passenger
from credit_card_checker import CreditCardChecker


def dateChecks(date):
    date = date.split("-")
    d1 = datetime(int(date[0]), int(date[1]), int(date[2]))
    if d1.date() > datetime.now().date():
        return True
    elif d1.date() == datetime.now().date():
        return False
    elif d1.date() < datetime.now().date():
        return False


def timeChecks(dateAndTime):
    date = dateAndTime.split(" ")[0].split("-")
    time = dateAndTime.split(" ")[1].split(":")

    d1 = datetime(int(date[0]), int(date[1]), int(
        date[2]), int(time[0]), int(time[1]), int(time[2]))

    if d1.date() > datetime.now().date():
        return True
    elif d1.date() == datetime.now().date():
        if d1.time() > datetime.now().time():
            return True
        else:
            return False
    elif d1.date() < datetime.now().date():
        return False


def getTableHeaders(cs, tableName):
    cs.execute("desc %s" % tableName)
    tableNames = []
    a = cs.fetchall()
    for i in a:
        tableNames.append(i[0])
    return tableNames


def getPassengerObj(user, db):
    cs = db.cursor()
    cs.execute("SELECT * FROM customerInfo WHERE userid = %s" % user.userId)
    passengers = []
    for i in cs.fetchall():
        passengers.append(i[1:])

    if len(passengers) != 0:
        print(bColors.bcolors.HEADER + "You have the following passengers:")
        print(bColors.bcolors.OKGREEN + tabulate(passengers,
              getTableHeaders(cs, "customerinfo")[1:]))

        cs.execute("SELECT paymentDue FROM logininfo WHERE userid = %s" % user.userId)
        dueTotal = cs.fetchall()[0][0]
        print(f"You have a payment due of {dueTotal}!")

        a = int(input(bColors.bcolors.OKCYAN +
                "Enter the customer id (-1 for new passenger, -2 to clear payment dues): "))
        os.system('cls')
        if a == -1:
            passenger = user.addPassenger()

        if a == -2:
            due = int(input("Enter the amount you'd like to pay: "))
            ccNum = input("Enter your credit card number: ")
            if CreditCardChecker(ccNum).valid():
                pin = input("Enter your CVC code: ")
                user.clearPayment(due)
            else:
                print(bColors.bcolors.FAIL + "Invalid credit card number!")
                getPassengerObj(user, db)

            user.clearPayment(due)
            return None

        else:
            cs.execute("SELECT * FROM customerInfo WHERE customerid = %s" % a)
            passengerDetails = cs.fetchall()
            passenger = Passenger.Passenger(
                user.userId, passengerDetails[0][1], passengerDetails[0][2], passengerDetails[0][3], db)
    else:
        print(bColors.bcolors.WARNING + "You have no passengers as of now!")
        passenger = user.addPassenger()

    return passenger
