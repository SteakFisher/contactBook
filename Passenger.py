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
        print(bColors.bcolors.OKGREEN + "Ticket added")

    def deletePassenger(self):
        self.cs.execute("DELETE FROM customerInfo WHERE customerId = %s" %
                        self.customerId)
        self.db.commit()
        print(bColors.bcolors.OKGREEN + "Passenger deleted")
