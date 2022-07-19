from bColors import *
from Passenger import *
import os


class User:
    def __init__(self, userId, username, password, permLevel, db):
        self.username = username
        self.password = password
        self.userId = userId
        self.permLevel = permLevel
        self.db = db
        self.cs = db.cursor()

    def deleteUser(self):
        self.cs.execute(
            "DELETE FROM logininfo WHERE userId = %s" % self.userId)
        self.db.commit()
        print(bcolors.OKGREEN + "User deleted")

    def addPassenger(self):
        a = input(bcolors.OKCYAN + "Enter passenger first name: ")
        b = input("Enter passenger last name: ")
        os.system('cls')
        try:
            self.cs.execute("INSERT INTO customerInfo(userid, customerName, customerLastName) VALUES(%s, '%s', '%s')" % (
                self.userId, a, b))
        except:
            print(bcolors.WARNING +
                  "Error! Passenger with the same details already exists!")
            self.addPassenger()
        else:
            self.db.commit()
            print(bcolors.OKGREEN + "Passenger added")
        self.cs.execute(
            "SELECT customerid FROM customerInfo WHERE customerName = '%s' and customerLastName = '%s'" % (a, b))
        c = self.cs.fetchall()
        return Passenger(self.userId, c[0][0], a, b, self.db)

    def getPassengers(self):
        self.cs.execute("SELECT * FROM customerInfo WHERE userid = %s" %
                        self.userId)
        passengers = self.cs.fetchall()
        return passengers
