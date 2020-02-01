from enum import Enum

id_bob = 1
id_elsie = 2
id_hulk = 3

updateIntervall = 0.4

LOC_DEFAULT = "DEFAULT"
LOC_HULK_HOME = "HULK_HOME"

locations = { 
    "DEFAULT" : "Town sqaure",
    "HULK_HOME" : "Hulks home"
}

class Msg(Enum):
    HulkGoHome = 1
    HulkGoWork = 2
    HulkGoStore = 3
    HulkGoPub = 4
    HulkArriveHome = 5
    HulkArriveWork = 6
    HulkArriveStore = 7
    HulkArrivePub = 8
    HulkWakeUp = 9
