import bColors
import Passenger
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
        print(bColors.bcolors.OKGREEN + "User deleted")

    def addPassenger(self):
        a = input(bColors.bcolors.OKCYAN + "Enter passenger first name: ")
        b = input("Enter passenger last name: ")
        os.system('cls')
        try:
            self.cs.execute("INSERT INTO customerInfo(userid, customerName, customerLastName) VALUES(%s, '%s', '%s')" % (
                self.userId, a, b))
        except:
            print(bColors.bcolors.WARNING +
                  "Error! Passenger with the same details already exists!")
            self.addPassenger()
        else:
            self.db.commit()
            print(bColors.bcolors.OKGREEN + "Passenger added")
        self.cs.execute(
            "SELECT customerid FROM customerInfo WHERE customerName = '%s' and customerLastName = '%s'" % (a, b))
        c = self.cs.fetchall()
        return Passenger.Passenger(self.userId, c[0][0], a, b, self.db)

    def getPassengers(self):
        self.cs.execute("SELECT * FROM customerInfo WHERE userid = %s" %
                        self.userId)
        passengers = self.cs.fetchall()
        return passengers

    def clearPayment(self, due):
        self.cs.execute("UPDATE logininfo SET paymentDue = paymentDue - %s WHERE userid = %s" % (self.userId, due))
        self.db.commit()
        print(bColors.bcolors.OKGREEN + "Payment cleared!")
