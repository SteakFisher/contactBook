from pprint import pprint
import mysql.connector as sql

db = sql.connect(username='root', password='00b', host='localhost', database='jay')
cs = db.cursor()

userId = 1
class User:
    def __init__(self, userId, username, password):
        self.username = username
        self.password = password
        self.userId = userId
        # table, name = loginInfo with primary key = userId contains info such as user, pass and userId
        # create table loginInfo(id int primary key, username varchar(30), password varchar(30), unique(username));
        # another table, name = contactInfo with foreign key = userId and primary key = contactId contains info such as userId, contactId, contactName, contactSurname, contactLastName
        # another table, name = contactNumbers with Foreign Key = contactId and primary key = numId has more info such as contactNumber, contactType
        # another table, name = events with Foreign Key = contactId and primary key = eventId has more info such as eventName, eventDate, eventLocation

def fetchUser(id):
    try:
        cs.execute("SELECT * FROM loginInfo WHERE id = %s" %(id))
    except:
        return False
    else:
        t = cs.fetchall()
        if(len(t) > 0):
            return User(t[0][0], t[0][1], t[0][2])
        else:
            return False

def login():
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    try:
        cs.execute("SELECT id FROM loginInfo WHERE username = '%s' AND password = '%s'" %(username, password))
    except:
        print("Login failed")
        return False
    else:
        t = cs.fetchall()
        if(len(t) > 0):
            print("Login successful")
            return User(t[0][0], username, password)
        else:
            print("Login failed")
            return False


def signUp():
    username = input("Enter your username: ")
    try:
        cs.execute("SELECT * FROM loginInfo WHERE username = '%s'" %(username))
    except:
        print("Sign up failed")
        return False
    else:
        t = cs.fetchall()
        if (len(t) > 0):
            print("Username already exists")
            return False
        else:
            password = input("Enter your password: ")
            global userId
            cs.execute("INSERT INTO loginInfo VALUES(%s, '%s', '%s')" % (userId, username, password))
            db.commit()
            userId += 1
            print("Sign up successful")
            return False

user = False
while (user is False):
    a = input("Login or Sign up? (l/s): ")
    if (a.lower() == 'l'):
        user = login()
    elif (a.lower() == 's'):
        user = signUp()
    else:
        print("Invalid input")
