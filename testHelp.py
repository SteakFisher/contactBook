from datetime import datetime, timedelta

info = {
    1: "Train 1",
    2: "Train 2",
    3: "Train 3",
    4: "Train 4",
    5: "Train 5",
    6: "Train 6"
}


def autoFillTrainInfo(dayCount, db):
    cs = db.cursor()
    for i in range(dayCount):
        NextDayDate = str(datetime.today() + timedelta(days=i + 1))[:10]
        NextDayTime = '00:00:00'
        counter = 1
        for j in range(12):
            cs.execute(
                "INSERT INTO trainInfo (trainName, departureTime, departingStation, arrivingStation, ticketCost, maxPassengerCount) VALUES ('%s', '%s %s', '%s', '%s', %s, %s)" % (
                    info[counter], NextDayDate, NextDayTime, 'Station 1', 'Station 2', 5, 100))
            db.commit()
            if counter == 6:
                counter = 1

            else:
                counter += 1
            check = str(int(NextDayTime[:2]) + 2)
            if len(check) == 1:
                NextDayTime = '0' + check + NextDayTime[2:]
            else:
                NextDayTime = check + NextDayTime[2:]