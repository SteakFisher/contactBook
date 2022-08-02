import os
import bColors
import User


def login(db):
    cs = db.cursor()
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    cs.execute(
        "SELECT userId, permLevel FROM loginInfo WHERE username = '%s' AND password = '%s'" % (username, password))
    t = cs.fetchall()
    os.system('cls')
    if len(t) > 0:
        print(bColors.bcolors.OKGREEN + "Login successful")
        return User.User(t[0][0], username, password, t[0][1], db)
    else:
        print(bColors.bcolors.FAIL + "Login failed")
        return False


def signUp(db):
    cs = db.cursor()
    username = input("Enter your username: ")
    cs.execute("SELECT userid FROM loginInfo WHERE username = '%s'" % username)
    t = cs.fetchall()
    if len(t) > 0:
        os.system('cls')
        print(bColors.bcolors.WARNING + "Username already exists")
        return False

    else:
        password = input("Enter your password: ")
        cs.execute("INSERT INTO loginInfo(username, password) VALUES('%s', '%s')" % (
            username, password))
        db.commit()
        os.system('cls')
        print(bColors.bcolors.OKGREEN + "Sign up successful")
        cs.execute(
            "SELECT userId, permLevel FROM loginInfo WHERE username = '%s' AND password = '%s'" % (username, password))
        t = cs.fetchall()
        return User.User(t[0][0], username, password, t[0][1],  db)
