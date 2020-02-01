from random import randint
from enum import Enum

from base_game_entity import BaseGameEntity
from state import State
from state_machine import StateMachine
from s_log import log
from s_print import out
import globals as G

# --------------------------------------------------------------- Rocket Raccoon

class Raccoon(BaseGameEntity):

    def __init__(self, val, name):
        super().__init__(val, name)
        #self.location = G.locations[G.LOC_HULK_HOME]
        self.fsm.globalState = RaccoonGlobalstate()
        self.fsm.currentState = RaccoonAtWork()
        self.isWorking = True
        self.toxicity = 0

    def IsDrunk(self):
        return self.toxicity > 40

class RaccoonGlobalstate(State):

    def Enter(self, entity):
        pass

    def Execute(self, entity):

        entity.toxicity -= 1

        if(not entity.IsSleeping()):
            entity.hunger -= 3
            entity.thirst -= 5
            entity.fatigue -= 5
            entity.social -= 5

        if(entity.IsThirsty()):
            if(entity.IsHome() or entity.IsWorking()):
                out(entity, "'Maybe a another little beer for myself..' *clunk*")
                entity.thirst += 25
                entity.toxicity += 10


    def Exit(self, entity):
        pass

    def OnMessage(self, entity, telegram):
        pass

class RaccoonAtHome(State):

    def Enter(self, entity):
        entity.isHome = True

    def Execute(self, entity):
        pass

    def Exit(self, entity):
        entity.isHome = False

    def OnMessage(self, entity, telegram):
        pass

class RaccoonAtWork(State):

    def Enter(self, entity):
        entity.isWorking = True

    def Execute(self, entity):
        out(entity, "*Serving customers*")
        entity.money += 3

    def Exit(self, entity):
        entity.isWorking = False

    def OnMessage(self, entity, telegram):
        # Hulk ask if Rocket is working
        if(telegram.msg == G.MSG.D_HulkAsRaccoonIfWorking_1):
            super().OnMessage(entity, telegram)
            
            out(entity, "#Sure am! You lonely broccoli boy? Come over then!#")

            entity.gm.Broadcast(0, entity, G.ID.Hulk, G.MSG.D_HulkAsRaccoonIfWorking_2, None)

            return True

        elif(telegram.msg == G.MSG.HulkArrivePub):
            super().OnMessage(entity, telegram)
            
            out(entity, "'There you are! Calmed down yet, big guy? Here, grab a beer and follow me will ya?'")
            
            entity.fsm.EnterStateBlip(RaccoonAtWorkChillax())
            entity.gm.Broadcast(0, entity, G.ID.Hulk, G.MSG.D_HulkRaccoonPub_1, None)

            return True

        return False

class RaccoonAtWorkChillax(State):

    def Enter(self, entity):
        entity.isSocializing = True
        out(entity, "'There is plenty of snacks and drinks, help yourself!'")
        # Start talking in a moment
        entity.gm.Broadcast(2, entity, G.ID.Rocket, G.MSG.D_HulkRaccoonPub_2, None)

    def Execute(self, entity):
        entity.hunger += 5
        entity.thirst += 5
        entity.social += 15
        
        if(randint(0, 9) < 5):
            out(entity, "*crunch*")
        elif(randint(0, 9) > 5):
            out(entity, "*gulp*")
        else:
            out(entity, "*burp*")

    def Exit(self, entity):
        entity.isSocializing = False

    def OnMessage(self, entity, telegram):
        if(telegram.msg == G.MSG.D_HulkRaccoonPub_2):
            super().OnMessage(entity, telegram)
            
            out(entity, "'So big guy, how ya day been?'")
            entity.gm.Broadcast(0, entity, G.ID.Hulk, G.MSG.D_HulkRaccoonPub_3, None)
            # Pause between dialogue
            entity.gm.Broadcast(2, entity, G.ID.Rocket, G.MSG.D_HulkRaccoonPub_4, None)

            return True

        elif(telegram.msg == G.MSG.D_HulkRaccoonPub_4):
            super().OnMessage(entity, telegram)
            
            out(entity, "'This is nice...'")
            entity.gm.Broadcast(0, entity, G.ID.Hulk, G.MSG.D_HulkRaccoonPub_5, None)

            return True

        elif(telegram.msg == G.MSG.D_HulkRaccoonPub_6):
            super().OnMessage(entity, telegram)
            
            out(entity, "'Catch you later Hulk!'")
            entity.fsm.RevertToPriorState()
            return True

        return False

class RaccoonTraverse(State):

    def Enter(self, entity):
        entity.isTraversing = True

    def Execute(self, entity):
        pass

    def Exit(self, entity):
        entity.isTraversing = False

    def OnMessage(self, entity, telegram):
        pass