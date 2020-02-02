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
        #self.AddItem("MJOLNIR")

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

        if(entity.IsTired()):
            entity.fsm.EnterStateBlip(ThorSleep())


    def Exit(self, entity):
        pass

    def OnMessage(self, entity, telegram):
        pass

##------------------------------------------------------------------##
class ThorAtHome(State):

    def Enter(self, entity):
        entity.isHome = True
        out(entity, "*Enters home*")

    def Execute(self, entity):
        out(entity, "*Playing video games*")
        if(randint(0, 9) > 5):
            out(entity, "'HA! Suck on that'")
        elif(randint(0, 9) > 3):
            out(entity, "'Of course! You all need cheats to beat me!'")
        else:
            out(entity, "*Reads* 'I'm-gonna-teabag-your-mom.' 'Pfff, puny insults!'")

    def Exit(self, entity):
        entity.isHome = False
        out(entity, "*Leaves home*")

    def OnMessage(self, entity, telegram):
        if(telegram.msg == G.MSG.GoWork and not entity.IsSleeping()):
            super().OnMessage(entity, telegram)

            if(entity.HasItem("MJOLNIR")):
                out(entity, "Stupid mortals and their silly working habit! I have better things to do than work. Pwning noobs, for example..")
            else:
                out(entity, "I do need a new hammer.. A god cannot be without his mighty weapon! Of to work!")
                entity.fsm.ChangeState(ThorTraverse())
                # Thor is fast
                entity.gm.Broadcast(1, entity, G.ID.Thor, G.MSG.ArriveWork, None)
            return True

        return False

##------------------------------------------------------------------##
class ThorAtWork(State):

    def Enter(self, entity):
        entity.isWorking = True
        out(entity, "*Arrives at work*")
        out(entity, "'Lets see what needs cleaning...'")

    def Execute(self, entity):
        out(entity, "*Cleaning*")

        if(entity.gm.GetTime() >= 15):
            out(entity, "'I'm done cleaning for today!!'")
            entity.fsm.ChangeState(ThorTraverse())
            entity.gm.Broadcast(1, entity, G.ID.Thor, G.MSG.ArriveHome, None)

        elif(entity.HasItem("MJOLNIR")):
            entity.money += 5
            if(randint(0, 9) > 7): # Random chance Mjolnir breaks
                out(entity, "*Mjolnir breaks* 'AGAIN!?'")
                entity.RemoveItem("MJOLNIR")
        
        elif(entity.money > 45): # Thor has money for new Mjolnir
            out(entity, "'Of to buy a new hammer!'")
            entity.fsm.ChangeState(ThorTraverse())
            # Thor is fast
            entity.gm.Broadcast(1, entity, G.ID.Thor, G.MSG.ArriveStore, None)
       
        else:
            entity.money += 3

        

    def Exit(self, entity):
        entity.isWorking = False
        out(entity, "*Leaves work*")

    def OnMessage(self, entity, telegram):
        pass

##------------------------------------------------------------------##
class ThorAtStore(State):

    def Enter(self, entity):
        out(entity, "*Arrives at store*")
        entity.searchTries = 0

    def Execute(self, entity):
        out(entity, "*Searches for new hammer* 'God why do mortals always move stuff around!?'")
        
        if(randint(0, 9) > 6): # Thor finds new hammes sometimes
            out(entity, "*Finds hammes* 'There we go, back to work'")
            entity.AddItem("MJOLNIR")
            entity.money -= 45
            entity.fsm.ChangeState(ThorTraverse())
            entity.gm.Broadcast(1, entity, G.ID.Thor, G.MSG.ArriveWork, None)
        elif(entity.searchTries >= 2):
            out(entity, "*Swears* '3 hours and still nothing! I'm out!'")
            entity.fsm.ChangeState(ThorTraverse())
            entity.gm.Broadcast(1, entity, G.ID.Thor, G.MSG.ArriveWork, None)
        else:
            entity.searchTries += 1


    def Exit(self, entity):
        out(entity, "*Leaves store*")

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
class ThorSleep(State):

    def Enter(self, entity):
        entity.isSleeping = True
        out(entity, "*Falls asleep*")
        entity.gm.Broadcast(1, entity, G.ID.Thor, G.MSG.WakeUp, None)

    def Execute(self, entity):
        pass

    def Exit(self, entity):
        entity.isSleeping = False
        entity.fatigue = 60
        out(entity, "*Wakes up* '.. OH yes madam straight away...'")

    def OnMessage(self, entity, telegram):
        if(telegram.msg == G.MSG.WakeUp):
            super().OnMessage(entity, telegram)
            entity.fsm.RevertToPriorState()
            return True

        return False

##------------------------------------------------------------------##
class ThorTraverse(State):

    def Enter(self, entity):
        entity.isTraversing = True

    def Execute(self, entity):
        pass

    def Exit(self, entity):
        entity.isTraversing = False

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