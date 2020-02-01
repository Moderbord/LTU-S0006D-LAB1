from state_machine import StateMachine
from s_log import log
import globals

class BaseGameEntity:
    
    __nextValidID = 0

    def __init__(self, val, name):
        self.__setID(val)
        self.name = name
        self.location = globals.locations[globals.LOC_DEFAULT]
        self.inventory = {}
        self.money = 50
        self.thirst = 75
        self.hunger = 50
        self.fatigue = 50
        self.social = 75
        
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
        log(self.name + " global state: " + str(type(self.fsm.globalState)))
        log(self.name + " current state: " + str(type(self.fsm.currentState)))
        log(self.name + " previous state: " + str(type(self.fsm.previousState)))
        log(self.name + " location: " + self.location)
        log(self.name + " inventory: " + str(self.inventory.items()))
        log(self.name + " money: " + str(self.money))
        log(self.name + " thirst: " + str(self.thirst))
        log(self.name + " hunger: " + str(self.hunger))
        log(self.name + " fatigue: " + str(self.fatigue))
        log(self.name + " social: " + str(self.social))

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
        return self.thirst <= 40

    def IsHungry(self):
        return self.hunger <= 30

    def IsTired(self):
        return self.fatigue <= 25

    def IsPoor(self):
        return self.money <= 10

    def IsLonely(self):
        return self.social <= 20

    def AddItem(self, item):
        self.inventory[item] = True

    def RemoveItem(self, item):
        self.inventory[item] = False

    def HasItem(self, item):
        return self.inventory.get(item, False)