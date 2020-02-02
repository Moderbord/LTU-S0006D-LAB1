from random import randint

from base_game_entity import BaseGameEntity
from state import State
from state_machine import StateMachine
from s_log import log
from s_print import out
import globals as G

##--------------------------THOR-------------------------------------##

class Thor(BaseGameEntity):

    def __init__(self, val, name):
        super().__init__(val, name)
        #self.location = G.locations[G.LOC_HULK_HOME]
        self.fsm.globalState = ThorGlobalstate()
        self.fsm.currentState = ThorAtHome()
        self.isHome = True
        self.AddItem("MJOLNIR")

##------------------------------------------------------------------##
class ThorGlobalstate(State):

    def Enter(self, entity):
        pass

    def Execute(self, entity):
        if(not entity.IsSleeping()):
            entity.hunger -= 1
            entity.thirst -= 2
            entity.fatigue -= 1
            entity.social -= 3

            if(entity.gm.GetTime() == 9):
                # Thor reminds himself to get to work (depending on state)
                entity.gm.Broadcast(0, entity, G.ID.Thor, G.MSG.GoWork, None)

    def Exit(self, entity):
        pass

    def OnMessage(self, entity, telegram):
        pass

##------------------------------------------------------------------##
class ThorAtHome(State):

    def Enter(self, entity):
        pass

    def Execute(self, entity):
        pass

    def Exit(self, entity):
        pass

    def OnMessage(self, entity, telegram):
        pass

##------------------------------------------------------------------##
class ThorAtWork(State):

    def Enter(self, entity):
        pass

    def Execute(self, entity):
        pass

    def Exit(self, entity):
        pass

    def OnMessage(self, entity, telegram):
        pass

##------------------------------------------------------------------##
class ThorAtStore(State):

    def Enter(self, entity):
        pass

    def Execute(self, entity):
        pass

    def Exit(self, entity):
        pass

    def OnMessage(self, entity, telegram):
        pass

##------------------------------------------------------------------##
class ThorAtMovies(State):

    def Enter(self, entity):
        pass

    def Execute(self, entity):
        pass

    def Exit(self, entity):
        pass

    def OnMessage(self, entity, telegram):
        pass

##------------------------------------------------------------------##
class ThorTraverse(State):

    def Enter(self, entity):
        pass

    def Execute(self, entity):
        pass

    def Exit(self, entity):
        pass

    def OnMessage(self, entity, telegram):
        if(telegram.msg == G.MSG.ArriveHome):
            super().OnMessage(entity, telegram)
            entity.fsm.ChangeState(ThorAtHome())
            return True

        elif(telegram.msg == G.MSG.ArriveWork):
            super().OnMessage(entity, telegram)
            entity.fsm.ChangeState(ThorAtWork())
            return True

        elif(telegram.msg == G.MSG.ArriveStore):
            super().OnMessage(entity, telegram)
            entity.fsm.ChangeState(ThorAtStore())
            return True

        elif(telegram.msg == G.MSG.ArriveMovies):
            super().OnMessage(entity, telegram)
            entity.fsm.ChangeState(ThorAtMovies())
            return True

        return False