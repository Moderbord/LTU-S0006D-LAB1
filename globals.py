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
    Thor = 5
    Groot = 6


class MSG(Enum):

    # Generic
    GoHome = 101
    ArriveHome = 102
    GoWork = 103
    ArriveWork = 104
    GoStore = 105
    ArriveStore = 106
    GoPub = 107
    ArrivePub = 108
    GoMovies = 109
    ArriveMovies = 110

    # Special
    WakeUp = 201
    PizzaDelivery = 202
    HulkArrivePub = 203
    HulkArriveMovies = 203
    RocketArriveMovies = 204
    GrootArriveMovies = 205
    MovieOver = 206

    # Dialogue and texts
    D_HulkAskRocketIfWorking_1 = 1001
    D_HulkAskRocketIfWorking_2 = 1002
    D_HulkAskRocketIfWorking_3 = 1003
    D_HulkRocketPub_1 = 1010
    D_HulkRocketPub_2 = 1011
    D_HulkRocketPub_3 = 1012
    D_HulkRocketPub_4 = 1013
    D_HulkRocketPub_5 = 1014
    D_HulkRocketPub_6 = 1015
    D_ThorPlanGoMovies_1 = 1020


