class GameTime:

    def __init__(self):
        self.time = 8
        self.weekday = 0
        self.loop = 0
        self.timesteps = {
            0: "00:00",
            1: "01:00",
            2: "02:00",
            3: "03:00",
            4: "04:00",
            5: "05:00",
            6: "06:00",
            7: "07:00",
            8: "08:00",
            9: "09:00",
            10: "10:00",
            11: "11:00",
            12: "12:00",
            13: "13:00",
            14: "14:00",
            15: "15:00",
            16: "16:00",
            17: "17:00",
            18: "18:00",
            19: "19:00",
            20: "20:00",
            21: "21:00",
            22: "22:00",
            23: "23:00"
        }
        self.weekdays = {
            0: "Monday",
            1: "Tuesday",
            2: "Wednesday",
            3: "Thursday",
            4: "Friday",
            5: "Saturday",
            6: "Sunday"
        }

    def NextTimestep(self):
        if(self.time == 23):
            self.time = 0
            self.NextWeekday()
        else:
            self.time += 1

    def HoursTo(self, hour):
        if(hour > self.time):
            return hour - self.time
        else:
            return (24 - self.time) + hour

    def GetTime(self):
        return self.time

    def GetTimeStr(self):
        return self.timesteps.get(self.time)

    def ToTimeStr(self, time):
        return self.timesteps.get(time)

    def NextWeekday(self):
        if(self.weekday == 6):
            self.weekday = 0
        else:
            self.weekday += 1

    def GetWeekday(self):
        return self.weekday

    def GetWeekdayStr(self):
        return self.weekdays.get(self.weekday)

    def GetLoop(self):
        return self.loop

    def NextLoop(self):
        self.loop += 1
    
    def SetLoop(self, loop):
        self.loop = loop