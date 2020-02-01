from state_machine import StateMachine
from s_log import log
import globals

class BaseGameEntity:
    
    __nextValidID = 0

    def __init__(self, val, name):
        self.__setID(val)
        self.eName = name
        self.eLocation = globals.locations[globals.LOC_DEFAULT]
        self.eInventory = {}
        self.eMoney = 50
        self.eThirst = 75
        self.eHunger = 50
        self.eFatigue = 50
        self.eSocial = 75
        
        self.isAlive = True
        self.isWorking = False
        self.isHome = False
        self.isSocializing = False
        self.isSleeping = False
        self.isTraversing = False

        self.fsm = StateMachine(self)

    def GetID(self):
        return self.__ID

    def __setID(self, val):
        # check valid ID?
        self.__ID = val

    def Update(self):
        self.fsm.Update()

    def HandleMessage(self, telegram):
        return self.fsm.HandleMessage(telegram)

    def logStates(self):
        log(self.eName + " global state: " + str(type(self.fsm.globalState)))
        log(self.eName + " current state: " + str(type(self.fsm.currentState)))
        log(self.eName + " previous state: " + str(type(self.fsm.previousState)))
        log(self.eName + " location: " + self.eLocation)
        log(self.eName + " inventory: " + str(self.eInventory.items()))
        log(self.eName + " money: " + str(self.eMoney))
        log(self.eName + " thirst: " + str(self.eThirst))
        log(self.eName + " hunger: " + str(self.eHunger))
        log(self.eName + " fatigue: " + str(self.eFatigue))
        log(self.eName + " social: " + str(self.eSocial))

    def IsAlive(self):
        return self.isAlive

    def IsWorking(self):
        return self.isWorking

    def IsHome(self):
        return self.isHome

    def IsSocializing(self):
        return self.isSocializing

    def IsSleeping(self):
        return self.isSleeping

    def IsTraversing(self):
        return self.isTraversing

    def IsThirsty(self):
        return self.eThirst <= 40

    def IsHungry(self):
        return self.eHunger <= 30

    def IsTired(self):
        return self.eFatigue <= 25

    def IsPoor(self):
        return self.eMoney <= 10

    def IsLonely(self):
        return self.eSocial <= 20

    def AddItem(self, item):
        self.eInventory[item] = True

    def RemoveItem(self, item):
        self.eInventory[item] = False

    def HasItem(self, item):
        return self.eInventory.get(item, False)