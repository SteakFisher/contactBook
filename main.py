import tkinter as tk
import os
import mysql.connector as sql
from tabulate import tabulate
from customFunc import *
from bColors import *
from User import *
from Passenger import *
from datetime import datetime


def getPassengerObj(user):
    cs.execute("SELECT * FROM customerInfo WHERE userid = %s" % user.userId)
    passengers = []
    for i in cs.fetchall():
        passengers.append(i[1:])

    if len(passengers) != 0:
        print(bcolors.HEADER + "You have the following passengers:")
        print(bcolors.OKGREEN + tabulate(passengers,
              getTableHeaders(cs, "customerinfo")[1:]))
        a = int(input(bcolors.OKCYAN +
                "Enter the customer id (-1 for new passenger): "))
        os.system('cls')
        if a == -1:
            passenger = user.addPassenger()
        else:
            cs.execute("SELECT * FROM customerInfo WHERE customerid = %s" % a)
            passengerDetails = cs.fetchall()
            passenger = Passenger(
                user.userId, passengerDetails[0][1], passengerDetails[0][2], passengerDetails[0][3], db)
    else:
        print(bcolors.WARNING + "You have no passengers as of now!")
        passenger = user.addPassenger()

    return passenger


def login():
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    cs.execute(
        "SELECT userId, permLevel FROM loginInfo WHERE username = '%s' AND password = '%s'" % (username, password))
    t = cs.fetchall()
    os.system('cls')
    if len(t) > 0:
        print(bcolors.OKGREEN + "Login successful")
        return User(t[0][0], username, password, t[0][1], db)
    else:
        print(bcolors.FAIL + "Login failed")
        return False


def signUp():
    username = input("Enter your username: ")
    cs.execute("SELECT userid FROM loginInfo WHERE username = '%s'" % username)
    t = cs.fetchall()
    if len(t) > 0:
        os.system('cls')
        print(bcolors.WARNING + "Username already exists")
        return False

    else:
        password = input("Enter your password: ")
        cs.execute("INSERT INTO loginInfo(username, password) VALUES('%s', '%s')" % (
            username, password))
        db.commit()
        os.system('cls')
        print(bcolors.OKGREEN + "Sign up successful")
        cs.execute(
            "SELECT userId, permLevel FROM loginInfo WHERE username = '%s' AND password = '%s'" % (username, password))
        t = cs.fetchall()
        return User(t[0][0], username, password, t[0][1],  db)


def ticketSystem(user, passenger):
    print()
    print(bcolors.HEADER + """1) Ticket booking \n2) Ticket checking \n3) Ticket cancellation \n4) Delete account
5) Delete passenger \n6) Logout \n7) Exit \n(1/2/3/4/5/6)""")
    ticketChoice = input(">>> ")
    os.system('cls')
    if ticketChoice == '1':
        print(bcolors.HEADER + "Ticket booking")
        dateAndTime = input(
            bcolors.OKCYAN + "Enter the departure time (YYYY-MM-DD HH:MI:SS): ")
        if timeChecks(dateAndTime):
            passenger.addTicket(dateAndTime, input("Enter train name: "))
            os.system('cls')
        else:
            print(bcolors.FAIL + "Invalid date and/or time")

    elif ticketChoice == '2':
        print(bcolors.HEADER + "Ticket checking")
        print(bcolors.OKGREEN + passenger.customerName +
              " has the following tickets: ")
        cs.execute("SELECT * FROM ticketInfo WHERE customerid = %s" %
                   passenger.customerId)
        tickets = []

        for i in cs.fetchall():
            tickets.append(i[1:])

        if len(tickets) != 0:
            print(bcolors.OKGREEN + tabulate(tickets,
                  getTableHeaders(cs, "ticketinfo")[1:]))
        else:
            print(bcolors.FAIL + "No tickets found")

    elif ticketChoice == '3':
        print(bcolors.HEADER + "Ticket cancellation")
        a = int(input("Enter ticketId of the ticket you'd like to cancel: "))
        os.system('cls')
        try:
            cs.execute("Delete from ticketInfo where ticketId = %s" % a)
        except:
            print(bcolors.FAIL + "Error! Ticket does not exist")
        else:
            db.commit()
            print(bcolors.OKGREEN + "Ticket cancelled")

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
        print(bcolors.OKGREEN + "Goodbye")
        return
    else:
        print(bcolors.FAIL + "Invalid option, input 1,2,3,4 or 5!")
        ticketSystem(user, passenger)
        return

    ticketSystem(user, passenger)


def main(user=False):
    os.system("cls")
    while user is False:
        print(bcolors.HEADER + """1) Login \n2) Sign up \n3) Exit \n(1/2/3)""")
        loginChoice = input(">>> ")
        if loginChoice == '1':
            user = login()
        elif loginChoice == '2':
            user = signUp()
        elif loginChoice == '3':
            print(bcolors.OKGREEN + "Goodbye")
            return
        else:
            print(bcolors.FAIL + "Invalid option, input 1,2 or 3!")
    print(bcolors.HEADER + "Welcome " + user.username + "!")
    passenger = getPassengerObj(user)
    ticketSystem(user, passenger)


db = sql.connect(user='root', password='00b', host='localhost')
cs = db.cursor()
cs.execute("Create database if not exists jay")
cs.execute("use jay")
cs.execute(" CREATE TABLE IF NOT EXISTS logininfo(userId int primary key NOT NULL AUTO_INCREMENT," +
           " username varchar(30) NOT NULL, password varchar(30) NOT NULL, permLevel varchar(20) DEFAULT 'user'" +
           " NOT NULL, unique(username))")
cs.execute("create table if not exists customerInfo(userid int, customerId int primary key NOT NULL AUTO_INCREMENT," +
           " customerName varchar(30) NOT NULL, customerLastName varchar(30) NOT NULL, constraint foreign key " +
           "(userid) references loginInfo(userId) ON DELETE CASCADE, CONSTRAINT customerConstraint unique(customerName, customerLastName))")
cs.execute("create table if not exists ticketInfo(customerId int, ticketId int primary key NOT NULL AUTO_INCREMENT," +
           " departureTime DATETIME NOT NULL, trainName varchar(30) NOT NULL, constraint foreign key " +
           "(customerId) references customerInfo(customerId)ON DELETE CASCADE)")

main()

# 2023-05-06 23:05:06
