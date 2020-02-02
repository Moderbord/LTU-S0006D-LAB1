from enum import Enum

updateIntervall = 0.1

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
    HulkGoHome = 101
    HulkGoWork = 102
    HulkGoStore = 103
    HulkGoPub = 104
    HulkArriveHome = 105
    HulkArriveWork = 106
    HulkArriveStore = 107
    HulkArrivePub = 108
    HulkWakeUp = 109

    D_HulkAskRocketIfWorking_1 = 1001
    D_HulkAskRocketIfWorking_2 = 1002
    D_HulkAskRocketIfWorking_3 = 1003
    D_HulkRocketPub_1 = 1010
    D_HulkRocketPub_2 = 1011
    D_HulkRocketPub_3 = 1012
    D_HulkRocketPub_4 = 1013
    D_HulkRocketPub_5 = 1014
    D_HulkRocketPub_6 = 1015

    RocketGoHome = 201
    RocketGoWork = 202
    RocketArriveHome = 203
    RocketArriveWork = 204
    RocketWakeUp = 205
    RocketPizzaDelivery = 206

