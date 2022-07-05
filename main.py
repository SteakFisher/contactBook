from pprint import pprint
import mysql.connector as sql
from tabulate import tabulate
from datetime import datetime

db = sql.connect(user='root', password='00b', host='localhost', database='jay')
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


def getTableHeaders(tableName):
    cs.execute("desc %s" % tableName)
    tableNames = []
    a = cs.fetchall()
    for i in a:
        tableNames.append(i[0])
    return tableNames

def timeChecks(dateAndTime):
    date = dateAndTime.split(" ")[0].split("-")
    time = dateAndTime.split(" ")[1].split(":")

    d1 = datetime(int(date[0]), int(date[1]), int(date[2]), int(time[0]), int(time[1]), int(time[2]))

    if d1.date() > datetime.now().date():
        return True
    elif d1.date() == datetime.now().date():
        if d1.time() > datetime.now().time():
            return True
        else:
            return False
    elif (d1.date() < datetime.now().date()):
        return False

class User:
    def __init__(self, userId, username, password, permLevel):
        self.username = username
        self.password = password
        self.userId = userId
        self.permLevel = permLevel
        # table, name = loginInfo with primary key = userId contains info such as user, pass and userId
        # create table logininfo(userId int primary key NOT NULL AUTO_INCREMENT, username varchar(30) NOT NULL,
        # password varchar(30) NOT NULL, unique(username));

        # create table if not exists customerInfo(userid int, customerId int primary key NOT NULL AUTO_INCREMENT,
        # customerName varchar(30) NOT NULL, customerSurname varchar(30), customerLastName varchar(30),
        # NOT NULL, constraint foreign key (userid) references loginInfo(userId))
        # insert into customerinfo(userid, customername, customerlastname) values(1, "jay", "Bej");

        # another table, name = contactInfo with foreign key = userId and primary key = contactId contains
        # info such as userId, contactId, contactName, contactSurname, contactLastName
        # create table contactInfo(userId int NOT NULL, contactId int primary key NOT NULL
        # AUTO_INCREMENT, contactName varchar(30), contactSurname varchar(30),
        # contactLastName varchar(30), constraint userId foreign key(userId) references loginInfo(userid));

        # another table, name = contactNumbers with Foreign Key = contactId
        # and primary key = numId has more info such as contactNumber, contactType
        # another table, name = events with Foreign Key = contactId and
        # primary key = eventId has more info such as eventName, eventDate, eventLocation

    def deleteUser(self):
        cs.execute("DELETE FROM logininfo WHERE userId = %s" % self.userId)
        db.commit()
        print("User deleted")

    def addPassenger(self):
        a = input("Enter passenger first name: ")
        b = input("Enter passenger last name: ")
        try:
            cs.execute("INSERT INTO customerInfo(userid, customerName, customerLastName) VALUES(%s, '%s', '%s')" % (self.userId, a, b))
        except:
            print("Error! Passenger with the same details already exists!")
            self.addPassenger()
        else:
            db.commit()
            print("Passenger added")
        cs.execute("SELECT customerid FROM customerInfo WHERE customerName = '%s' and customerLastName = '%s'" % (a, b))
        c = cs.fetchall()
        return Passenger(self.userId, c[0][0], a, b)

    def getPassengers(self):
        cs.execute("SELECT * FROM customerInfo WHERE userid = %s" % self.userId)
        passengers = cs.fetchall()
        return passengers


class Passenger:
    def __init__(self, userId, customerId, customerName, customerLastName):
        self.userId = userId
        self.customerId = customerId
        self.customerName = customerName
        self.customerLastName = customerLastName

    def addTicket(self, departureTime, trainName):
        cs.execute("Insert into ticketInfo(customerId, departureTime, trainName) values(%s, '%s', '%s')" % (self.customerId, departureTime, trainName))
        db.commit()
        print("Ticket added")

    def deletePassenger(self):
        cs.execute("DELETE FROM customerInfo WHERE customerId = %s" % self.customerId)
        db.commit()
        print("Passenger deleted")


def getPassengerObj(user):
    passenger = False
    cs.execute("SELECT * FROM customerInfo WHERE userid = %s" % user.userId)
    passengers = cs.fetchall()
    if len(passengers) != 0:
        print("You have the following passengers:")
        print(tabulate(passengers, getTableHeaders("customerinfo")))
        a = int(input("Enter the customer id (-1 for new passenger): "))
        if a == -1:
            passenger = user.addPassenger()
        else:
            cs.execute("SELECT * FROM customerInfo WHERE customerid = %s" % a)
            passengerDetails = cs.fetchall()
            passenger = Passenger(user.userId, passengerDetails[0][1], passengerDetails[0][2], passengerDetails[0][3])
    else:
        print("You have no passengers as of now!")
        passenger = user.addPassenger()

    return passenger

def login():
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    cs.execute("SELECT userId, permLevel FROM loginInfo WHERE username = '%s' AND password = '%s'" % (username, password))
    t = cs.fetchall()
    if len(t) > 0:
        print("Login successful")
        return User(t[0][0], username, password, t[0][1])
    else:
        print("Login failed")
        return False


def signUp():
    username = input("Enter your username: ")
    cs.execute("SELECT userid FROM loginInfo WHERE username = '%s'" % username)
    t = cs.fetchall()
    if len(t) > 0:
        print("Username already exists")
        return False
    else:
        password = input("Enter your password: ")
        cs.execute("INSERT INTO loginInfo(username, password) VALUES('%s', '%s')" % (username, password))
        db.commit()
        print("Sign up successful")
        cs.execute("SELECT userId, permLevel FROM loginInfo WHERE username = '%s' AND password = '%s'" % (username, password))
        t = cs.fetchall()
        return User(t[0][0], username, password, t[0][1])


def ticketSystem(user, passenger):
    print("""1) Ticket booking \n2) Ticket checking \n3) Ticket cancellation \n4) Delete account \n5) Delete passenger \n6) Logout \n7) Exit \n(1/2/3/4/5/6)""")
    ticketChoice = input(">>> ")
    if ticketChoice == '1':
        print("Ticket booking")
        dateAndTime = input("Enter the departure time (YYYY-MM-DD HH:MI:SS): ")
        if timeChecks(dateAndTime):
            passenger.addTicket(dateAndTime, input("Enter train name: "))
        else:
            print("Invalid date and/or time")

    elif ticketChoice == '2':
        print("Ticket checking")
        print(passenger.customerName + " has the following tickets: ")
        cs.execute("SELECT * FROM ticketInfo WHERE customerid = %s" % passenger.customerId)
        tickets = cs.fetchall()
        if(len(tickets) != 0):
            print(tabulate(tickets, getTableHeaders("ticketinfo")))
        else:
            print("No tickets found")

    elif ticketChoice == '3':
        print("Ticket cancellation")
        a = int(input("Enter ticketId of the ticket you'd like to cancel: "))
        try:
            cs.execute("Delete from ticketInfo where ticketId = %s" % a)
        except:
            print("Error! Ticket does not exist")
        else:
            db.commit()
            print("Ticket cancelled")

    elif ticketChoice == '4':
        user.deleteUser()
        del passenger
        user = False
        main()

    elif ticketChoice == '5':
        passenger.deletePassenger()
        del passenger
        main(user)

    elif ticketChoice == '6':
        del passenger
        user = False
        main()
        return

    elif ticketChoice == '7':
        user = False
        print("Goodbye")
        return
    else:
        print("Invalid option, input 1,2,3,4 or 5!")

    ticketSystem(user, passenger)


def main(user=False):
    while user is False:
        print("""1) Login \n2) Sign up \n3) Exit \n(1/2/3)""")
        loginChoice = input(">>> ")
        if loginChoice == '1':
            user = login()
        elif loginChoice == '2':
            user = signUp()
        elif loginChoice == '3':
            print("Goodbye")
            return
        else:
            print("Invalid option, input 1,2 or 3!")

    print("Welcome " + user.username + "!")
    passenger = getPassengerObj(user)
    ticketSystem(user, passenger)

main()

# 2023-05-06 23:05:06