from enum import Enum

updateIntervall = 0.4

# TODO implement locations, coordinates?
LOC_DEFAULT = "DEFAULT"
LOC_HULK_HOME = "HULK_HOME"

locations = { 
    "DEFAULT" : "Town sqaure",
    "HULK_HOME" : "Hulks home"
}

class ID(Enum):
    Bob = 1
    Elsie = 2
    Hulk = 3
    Rocket = 4


class MSG(Enum):
    HulkGoHome = 1
    HulkGoWork = 2
    HulkGoStore = 3
    HulkGoPub = 4
    HulkArriveHome = 5
    HulkArriveWork = 6
    HulkArriveStore = 7
    HulkArrivePub = 8
    HulkWakeUp = 9

    D_HulkAsRaccoonIfWorking_1 = 10
    D_HulkAsRaccoonIfWorking_2 = 11
    D_HulkRaccoonPub_1 = 12
    D_HulkRaccoonPub_2 = 13
    D_HulkRaccoonPub_3 = 14
    D_HulkRaccoonPub_4 = 15
    D_HulkRaccoonPub_5 = 16
    D_HulkRaccoonPub_6 = 17

