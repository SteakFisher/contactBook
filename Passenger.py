import bColors


class Passenger:
    def __init__(self, userId, customerId, customerName, customerLastName, db):
        self.userId = userId
        self.customerId = customerId
        self.customerName = customerName
        self.customerLastName = customerLastName
        self.db = db
        self.cs = db.cursor()

    def addTicket(self, trainId):
        self.cs.execute("Insert into ticketInfo(customerId, trainId) values(%s, %s)" % (
            self.customerId, trainId))
        self.db.commit()

        self.cs.execute("SELECT travelCost FROM traininfo WHERE trainId = %s" % trainId)
        cost = self.cs.fetchall()[0][0]

        self.cs.execute("UPDATE logininfo SET paymentDue = paymentDue + %s WHERE userid = %s" % (self.userId, cost))
        self.db.commit()

        print(bColors.bcolors.OKGREEN + "Ticket added")

    def deletePassenger(self):
        self.cs.execute("DELETE FROM customerInfo WHERE customerId = %s" %
                        self.customerId)
        self.db.commit()
        print(bColors.bcolors.OKGREEN + "Passenger deleted")
