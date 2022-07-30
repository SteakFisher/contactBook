from datetime import datetime


def dateChecks(date):
    date = date.split("-")
    d1 = datetime(int(date[0]), int(date[1]), int(date[2]))
    if d1.date() > datetime.now().date():
        return True
    elif d1.date() == datetime.now().date():
        return False
    elif d1.date() < datetime.now().date():
        return False

def timeChecks(dateAndTime):
    date = dateAndTime.split(" ")[0].split("-")
    time = dateAndTime.split(" ")[1].split(":")

    d1 = datetime(int(date[0]), int(date[1]), int(
        date[2]), int(time[0]), int(time[1]), int(time[2]))

    if d1.date() > datetime.now().date():
        return True
    elif d1.date() == datetime.now().date():
        if d1.time() > datetime.now().time():
            return True
        else:
            return False
    elif d1.date() < datetime.now().date():
        return False


def getTableHeaders(cs, tableName):
    cs.execute("desc %s" % tableName)
    tableNames = []
    a = cs.fetchall()
    for i in a:
        tableNames.append(i[0])
    return tableNames
