import os
import mysql.connector as sql
from tabulate import tabulate
import customFunc
import bColors
from datetime import datetime
from testHelp import *
from loginProc import *

db = sql.connect(user='root', password='00b', host='localhost')
cs = db.cursor()
cs.execute("Create database if not exists railway")
cs.execute("use railway")

cs.execute("CREATE TABLE IF NOT EXISTS logininfo(userId int primary key NOT NULL AUTO_INCREMENT," +
           " username varchar(30) NOT NULL, password varchar(30) NOT NULL, permLevel varchar(20) DEFAULT 'user'" +
           " NOT NULL, unique(username))")

cs.execute(
    "create table if not exists customerInfo(userid int, customerId int primary key NOT NULL AUTO_INCREMENT," +
    " customerName varchar(30) NOT NULL, customerLastName varchar(30) NOT NULL, constraint foreign key " +
    "(userid) references loginInfo(userId) ON DELETE CASCADE, CONSTRAINT customerConstraint" +
    " unique(customerName, customerLastName))")

cs.execute("CREATE TABLE IF NOT EXISTS trainInfo(trainId int PRIMARY KEY NOT NULL AUTO_INCREMENT, trainName " +
           "varchar(30) NOT NULL, departureTime datetime NOT NULL, maxPassengerCount int NOT NULL)")

cs.execute(
    "create table if not exists ticketInfo(customerId int, ticketId int primary key NOT NULL AUTO_INCREMENT," +
    " trainId int, constraint foreign key "
    "(customerId) references customerInfo(customerId) ON DELETE CASCADE, constraint foreign key (ticketId) " +
    " references trainInfo(trainId) ON DELETE CASCADE)")


def ticketSystem(user, passenger):
    print()
    print(bColors.bcolors.HEADER + """1) Ticket booking \n2) Ticket checking \n3) Ticket cancellation \n4) Delete account
5) Delete passenger \n6) Logout \n7) Exit \n(1/2/3/4/5/6)""")
    ticketChoice = input(">>> ")
    os.system('cls')
    if ticketChoice == '1':
        print(bColors.bcolors.HEADER + "Ticket booking")
        dateAlone = input(
            bColors.bcolors.OKCYAN + "Enter the departure date (YYYY-MM-DD): ")

        if customFunc.dateChecks(dateAlone):
            cs.execute(
                "SELECT trainId, trainName, departureTime FROM traininfo WHERE departuretime LIKE '%s %%'" % dateAlone)
            t = cs.fetchall()
            print(f"Available trains on {dateAlone}:")
            print(bColors.bcolors.OKGREEN + tabulate(t, customFunc.getTableHeaders(cs, "traininfo")[:3]))
            print(t)
            trainId = input("Enter train id: ")
            passenger.addTicket(trainId)
            os.system('cls')
        else:
            print(bColors.bcolors.FAIL + "Invalid date and/or time (Tickets must be booked at least a day in advance)")

    elif ticketChoice == '2':
        print(bColors.bcolors.HEADER + "Ticket checking")
        print(bColors.bcolors.OKGREEN + passenger.customerName +
              " has the following tickets: ")
        cs.execute("SELECT ticketId, trainId FROM ticketInfo WHERE customerid = %s" %
                   passenger.customerId)
        t = cs.fetchall()
        tickets = [t[0][0]]
        cs.execute("SELECT trainName, departureTime FROM traininfo WHERE trainId = %s" % t[0][1])

        for i in cs.fetchall()[0]:
            tickets.append(i)
        print(tickets)

        if len(tickets) != 0:
            print(bColors.bcolors.OKGREEN + tabulate(tickets, ["Ticket Id", "Train Name", "Departure time"]))
        else:
            print(bColors.bcolors.FAIL + "No tickets found")

    elif ticketChoice == '3':
        print(bColors.bcolors.HEADER + "Ticket cancellation")
        a = int(input("Enter ticketId of the ticket you'd like to cancel: "))
        os.system('cls')
        try:
            cs.execute("Delete from ticketInfo where ticketId = %s" % a)
        except:
            print(bColors.bcolors.FAIL + "Error! Ticket does not exist")
        else:
            db.commit()
            print(bColors.bcolors.OKGREEN + "Ticket cancelled")

    elif ticketChoice == '4':
        user.deleteUser()
        del passenger
        main()
        return

    elif ticketChoice == '5':
        passenger.deletePassenger()
        del passenger
        main(user)
        return

    elif ticketChoice == '6':
        del passenger
        main()
        return

    elif ticketChoice == '7':
        print(bColors.bcolors.OKGREEN + "Goodbye")
        return
    else:
        print(bColors.bcolors.FAIL + "Invalid option, input 1,2,3,4 or 5!")
        ticketSystem(user, passenger)
        return

    ticketSystem(user, passenger)


def main(user=False):
    os.system("cls")
    while user is False:
        print(bColors.bcolors.HEADER + """1) Login \n2) Sign up \n3) Exit \n(1/2/3)""")
        loginChoice = input(">>> ")
        if loginChoice == '1':
            user = login(db)
        elif loginChoice == '2':
            user = signUp(db)
        elif loginChoice == '3':
            print(bColors.bcolors.OKGREEN + "Goodbye")
            return
        else:
            print(bColors.bcolors.FAIL + "Invalid option, input 1,2 or 3!")
    print(bColors.bcolors.HEADER + "Welcome " + user.username + "!")
    passenger = customFunc.getPassengerObj(user, db)
    ticketSystem(user, passenger)


main()

# 2023-05-06 23:05:06
