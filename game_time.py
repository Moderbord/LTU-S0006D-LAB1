class GameTime:

    def __init__(self):
        self.time = 5
        self.weekday = 6
        self.loop = 0

    def NextTimestep(self):
        if(self.time == 23):
            self.time = 0
            self.NextWeekday()
        else:
            self.time += 1

    def GetTime(self):
        timesteps = {
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
        return timesteps.get(self.time)

    def NextWeekday(self):
        if(self.weekday == 7):
            self.weekday = 1
        else:
            self.weekday += 1

    def GetWeekday(self):
        weekdays = {
            1: "Monday",
            2: "Tuesday",
            3: "Wednesday",
            4: "Thursday",
            5: "Friday",
            6: "Saturday",
            7: "Sunday"
        }
        return weekdays.get(self.weekday)

    def GetLoop(self):
        return self.loop

    def NextLoop(self):
        self.loop += 1
    
    def SetLoop(self, loop):
        self.loop = loop