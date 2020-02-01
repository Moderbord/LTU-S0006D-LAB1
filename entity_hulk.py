from random import randint
from enum import Enum

from base_game_entity import BaseGameEntity
from state import State
from state_machine import StateMachine
from s_log import log
from s_print import out
import game_manager
import globals

# --------------------------------------------------------------- MINER

class Hulk(BaseGameEntity):

    def __init__(self, val, name):
        super().__init__(val, name)
        self.eLocation = globals.locations[globals.LOC_HULK_HOME]
        self.fsm.globalState = HulkGlobalState()
        self.fsm.currentState = HulkAtHome()



class HulkGlobalState(State):

    def Enter(self, gameEntity):
        pass

    def Execute(self, gameEntity):
        pass

    def Exit(self, gameEntity):
        pass

class HulkAtHome(State):

    def Enter(self, gameEntity):
        pass

    def Execute(self, gameEntity):
        out(gameEntity, "Hulk at home!")

    def Exit(self, gameEntity):
        pass