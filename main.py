import os
import mysql.connector as sql
from tabulate import tabulate
import customFunc
import User
import bColors
from testHelp import *
from loginProc import *
import maskpass

#############################
# DEFAULT ADMIN USER = "admin" AND PASSWORD = "pass"
# RUN autoFillTrainInfo(num of days, db) at the end of the file to fill the trainInfo table for testing purposes
#############################

db = sql.connect(user='root', password='00b', host='localhost')
cs = db.cursor()
cs.execute("Create database if not exists railway")
cs.execute("use railway")

cs.execute("CREATE TABLE IF NOT EXISTS logininfo(userId int primary key NOT NULL AUTO_INCREMENT," +
           " username varchar(30) NOT NULL, password varchar(30) NOT NULL, permLevel varchar(20) DEFAULT 'user'" +
           " NOT NULL, unique(username))")

try:
    cs.execute(
        "INSERT INTO logininfo(username, password, permLevel) VALUES('admin', 'pass', 'admin')")
except:
    pass
else:
    db.commit()

cs.execute(
    "create table if not exists customerInfo(userid int, customerId int primary key NOT NULL AUTO_INCREMENT," +
    " customerName varchar(30) NOT NULL, customerLastName varchar(30) NOT NULL, constraint foreign key " +
    "(userid) references loginInfo(userId) ON DELETE CASCADE, CONSTRAINT customerConstraint" +
    " unique(customerName, customerLastName))")

cs.execute("CREATE TABLE IF NOT EXISTS trainInfo(trainId int PRIMARY KEY NOT NULL AUTO_INCREMENT, trainName " +
           "varchar(30) NOT NULL, departingStation varchar(30), arrivingStation varchar(30)," +
           " departureTime datetime NOT NULL, maxPassengerCount int NOT NULL, ticketCost int)")

cs.execute(
    "create table if not exists ticketInfo(customerId int, ticketId int primary key NOT NULL AUTO_INCREMENT," +
    " trainId int, paid bool default false, constraint foreign key "
    "(customerId) references customerInfo(customerId) ON DELETE CASCADE, constraint foreign key (ticketId) " +
    " references trainInfo(trainId) ON DELETE CASCADE)")


def ticketSystem(user, passenger):
    print(bColors.bcolors.HEADER + """1) Ticket booking \n2) Ticket checking \n3) Ticket cancellation \n4) Ticket Payment 
5) Switch passenger \n6) Delete account \n7) Delete passenger \n8) Logout \n9) Exit \n(1/2/3/4/5/6/7/8/9)""")
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
            print(bColors.bcolors.OKGREEN + tabulate(t,
                                                     customFunc.getTableHeaders(cs, "traininfo")[:3]))
            trainId = input("Enter train id: ")
            passenger.addTicket(trainId)
            os.system('cls')
        else:
            print(bColors.bcolors.FAIL +
                  "Invalid date and/or time (Tickets must be booked at least a day in advance)")

    elif ticketChoice == '2':
        print(bColors.bcolors.HEADER + "Ticket checking")
        print(bColors.bcolors.OKGREEN + passenger.customerName +
              " has the following tickets: ")
        cs.execute("SELECT ticketId, trainId, paid FROM ticketInfo WHERE customerid = %s" %
                   passenger.customerId)
        t = cs.fetchall()
        tickets = []
        for i in t:
            cs.execute(
                "SELECT trainName, departingStation, arrivingStation, departureTime, ticketCost FROM traininfo WHERE trainId = %s" % i[1])
            r = cs.fetchall()
            a = "No"
            if i[2] == 1:
                a = "Yes"
            tickets.append([i[0], r[0][0], r[0][1], r[0][2], r[0][3], r[0][4], a])

        if len(tickets) != 0:
            print(bColors.bcolors.OKGREEN +
                  tabulate(tickets, ["Ticket Id", "Train Name", "Departing Station", "Arriving Station", "Departure time", "Ticket cost", "Paid"]))
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
        print(bColors.bcolors.HEADER + "Ticket payment")
        a = int(input("Enter ticketId of the ticket you'd like to pay for: "))
        os.system('cls')
        try:
            cs.execute("Update ticketInfo set paid = true where ticketId = %s" % a)
        except:
            print(bColors.bcolors.FAIL + "Error! Ticket does not exist")
        else:
            db.commit()
            print(bColors.bcolors.OKGREEN + "Ticket paid")

    elif ticketChoice == '5':
        del passenger
        main(user)

    elif ticketChoice == '6':
        user.deleteUser()
        del passenger
        main()
        return

    elif ticketChoice == '7':
        passenger.deletePassenger()
        del passenger
        main(user)
        return

    elif ticketChoice == '8':
        del passenger
        main()
        return

    elif ticketChoice == '9':
        print(bColors.bcolors.OKGREEN + "Goodbye")
        user.permLevel = 'exit'
        os.system('cls')
        return

    else:
        print(bColors.bcolors.FAIL + "Invalid option, input 1,2,3,4,5,6,7,8 or 9!")
        ticketSystem(user, passenger)
        return

    ticketSystem(user, passenger)


def adminSystem(user):
    print()
    print(bColors.bcolors.HEADER + """1) Add train \n2) Delete train \n3) List trains \n4) Add admin \n5) List users 
6) Select user \n7) Exit \n(1/2/3/4/5/7)""")

    adminChoice = input(">>> ")
    os.system('cls')

    if adminChoice == '1':
        print(bColors.bcolors.HEADER + "Add train")
        trainName = input(bColors.bcolors.OKCYAN + "Enter train name: ")
        departureTime = input(bColors.bcolors.OKCYAN +
                              "Enter departure time (YYYY-MM-DD HH:MM): ")
        if customFunc.timeChecks(departureTime):
            maxPassengerCount = int(
                input(bColors.bcolors.OKCYAN + "Enter max passenger count: "))
            os.system('cls')
            try:
                cs.execute("INSERT INTO traininfo(trainName, departureTime, maxPassengerCount) VALUES('%s', '%s', %s)" %
                           (trainName, departureTime, maxPassengerCount))
            except:
                print(bColors.bcolors.FAIL + "Error! Train already exists")
            else:
                db.commit()
                print(bColors.bcolors.OKGREEN + "Train added")
        else:
            print(bColors.bcolors.FAIL + "Invalid date and/or time")
        adminSystem(user)

    elif adminChoice == '2':
        print(bColors.bcolors.HEADER + "Delete train")
        trainId = int(input(bColors.bcolors.OKCYAN + "Enter train id: "))
        os.system('cls')
        try:
            cs.execute("DELETE FROM traininfo WHERE trainId = %s" % trainId)
        except:
            print(bColors.bcolors.FAIL + "Error! Train does not exist")
        else:
            db.commit()
            print(bColors.bcolors.OKGREEN + "Train deleted")
        adminSystem(user)

    elif adminChoice == '3':
        print(bColors.bcolors.HEADER + "List trains")
        cs.execute(
            "SELECT trainId, trainName, departureTime, maxPassengerCount FROM traininfo")
        t = cs.fetchall()
        print(f"Available trains:")
        print(bColors.bcolors.OKGREEN + tabulate(t,
                                                 customFunc.getTableHeaders(cs, "traininfo")[:4]))
        adminSystem(user)

    elif adminChoice == '4':
        print(bColors.bcolors.HEADER + "Add admin")
        adminName = input(bColors.bcolors.OKCYAN + "Enter admin name: ")
        adminPassword = input(bColors.bcolors.OKCYAN +
                              "Enter admin password: ")
        os.system('cls')
        try:
            cs.execute("INSERT INTO logininfo(username, password, permLevel) VALUES('%s', '%s', 'admin')" %
                       (adminName, adminPassword))
        except:
            print(bColors.bcolors.FAIL + "Error! User already exists")
        else:
            db.commit()
            print(bColors.bcolors.OKGREEN + "Admin added")
        adminSystem(user)

    elif adminChoice == '5':
        print(bColors.bcolors.HEADER + "List users")
        cs.execute(
            "SELECT userId, username, password, permLevel FROM logininfo WHERE permLevel = 'user'")
        nt = []
        t = cs.fetchall()

        for i in t:
            a, b, c = i[0], i[1], i[3]
            t = (a, b, c)
            nt.append(t)

        print("Available users:")
        print(bColors.bcolors.OKGREEN + tabulate(nt,
                                                 customFunc.getTableHeaders(cs, "logininfo")[:2]))
        adminSystem(user)

    elif adminChoice == '6':
        print(bColors.bcolors.HEADER + "Select user")
        userId = int(input(bColors.bcolors.OKCYAN + "Enter user id: "))
        os.system('cls')
        try:
            cs.execute("SELECT username, password, permLevel FROM logininfo WHERE userId = %s and "
                       "permLevel = 'user'" % userId)
        except:
            print(bColors.bcolors.FAIL + "Error! User does not exist")
        else:
            t = cs.fetchall()
        pretUser = User.User(userId, t[0][0], t[0][1], t[0][2], db)
        main(pretUser)
        main(user)

    elif adminChoice == '7':
        print(bColors.bcolors.OKGREEN + "Goodbye")
        return

    else:
        print(bColors.bcolors.FAIL + "Invalid option, input 1,2,3,4,5,6 or 7!")
        adminSystem(user)
        return


def main(user=False):
    os.system("cls")
    while user is False:
        print(bColors.bcolors.HEADER +
              """1) Login \n2) Sign up \n3) Exit \n(1/2/3)""")
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

    if user.permLevel == "user":
        print(bColors.bcolors.OKCYAN + "You have a due of $" + str(user.due()))
        passenger = customFunc.getPassengerObj(user, db)
        ticketSystem(user, passenger)
    elif user.permLevel == 'admin':
        adminSystem(user)
    else:
        return


def recurseTry():
    try:
        main()
    except:
        print(bColors.bcolors.FAIL + "Something went wrong, try again")
        recurseTry()

recurseTry()

# 2022-09-26 23:05:06
