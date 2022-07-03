from pprint import pprint
import mysql.connector as sql

db = sql.connect(user='root', password='00b', host='localhost', database='jay')
cs = db.cursor()

cs.execute(" CREATE TABLE IF NOT EXISTS logininfo(userId int primary key NOT NULL AUTO_INCREMENT," +
           " username varchar(30) NOT NULL, password varchar(30) NOT NULL, permLevel varchar(20) DEFAULT 'user'" +
           " NOT NULL, unique(username))")


class User:
    def __init__(self, userId, username, password, permLevel):
        self.username = username
        self.password = password
        self.userId = userId
        self.permLevel = permLevel
        # table, name = loginInfo with primary key = userId contains info such as user, pass and userId
        # create table logininfo(userId int primary key NOT NULL AUTO_INCREMENT, username varchar(30) NOT NULL,
        # password varchar(30) NOT NULL, unique(username));

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
        cs.execute("DELETE FROM logininfo WHERE userId = %s", (self.userId,))
        db.commit()
        print("User deleted")


def login():
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    cs.execute(
        "SELECT userId, permLevel FROM loginInfo WHERE username = '%s' AND password = '%s'" % (username, password))
    t = cs.fetchall()
    if len(t) > 0:
        print("Login successful")
        print(t[0][1])
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
        cs.execute(
            "SELECT userId, permLevel FROM loginInfo WHERE username = '%s' AND password = '%s'" % (username, password))
        t = cs.fetchall()
        return User(t[0][0], username, password, t[0][1])


def main():
    user = False
    while user is False:
        print("""1) Login \n2) Sign up \n3) Exit \n(1/2/3)""")
        loginChoice = input("")
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

    print("""1) Ticket booking \n2) Ticket checking \n3) Ticket cancellation \n4) Delete account \n5) Exit \n(1/2/3/4/5)""")
    userChoice = input("")
    if userChoice == '1':
        print("Ticket booking")
    elif userChoice == '2':
        print("Ticket checking")
    elif userChoice == '3':
        print("Ticket cancellation")
    elif userChoice == '4':
        user.deleteUser()
        del user
        main()
    elif userChoice == '5':
        del user
        print("Goodbye")


main()
