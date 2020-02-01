from random import randint
from enum import Enum

from base_game_entity import BaseGameEntity
from state import State
from state_machine import StateMachine
from s_log import log
from s_print import out
import globals

# --------------------------------------------------------------- HULK

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
        if(not gameEntity.IsSleeping()):
            gameEntity.eHunger -= 3
            gameEntity.eThirst -= 2
            gameEntity.eFatigue -= 5
            gameEntity.eSocial -= 5

        if(gameEntity.IsThirsty()):
            if(gameEntity.IsHome() or gameEntity.IsWorking()):
                out(gameEntity, "'Hulk thirsty! *clunk*")
                gameEntity.eThirst += 25


    def Exit(self, gameEntity):
        pass

    def OnMessage(self, gameEntity, telegram):

        # Hulk goes to work
        if(telegram.msg == globals.Msg.HulkGoWork):
            super().OnMessage(gameEntity, telegram)
            
            out(gameEntity, "'Stupid work every day! Hulk hates to go to work!'")
            gameEntity.fsm.ChangeState(HulkTraverse())
            # Arrive in 2 loops
            gameEntity.gm.Broadcast(2, gameEntity.GetID(), globals.id_hulk, globals.Msg.HulkArriveWork, None)

            return True

        return False

class HulkAtHome(State):

    def Enter(self, gameEntity):
        gameEntity.isHome = True

    def Execute(self, gameEntity):
        #out(gameEntity, "'Hulk at home!'")
        if(gameEntity.IsHungry()):
            out(gameEntity, "'Hulk HUNGRY!!'")
            gameEntity.fsm.EnterStateBlip(HulkAtHomeDinner())
        elif(gameEntity.IsTired()):
            out(gameEntity, "'Hulk tired, go SLEEP!'")
            gameEntity.fsm.EnterStateBlip(HulkAtHomeSleep())

    def Exit(self, gameEntity):
        gameEntity.isHome = False

    def OnMessage(self, gameEntity, telegram):

        # Hulk goes to store
        if(telegram.msg == globals.Msg.HulkGoStore):
            super().OnMessage(gameEntity, telegram)
            
            out(gameEntity, "'Hulk go to store! Need more chicken!'")
            gameEntity.fsm.ChangeState(HulkTraverse())
            # Arrive in 2 loops
            gameEntity.gm.Broadcast(2, gameEntity.GetID(), globals.id_hulk, globals.Msg.HulkArriveStore, None)

            return True

        return False

class HulkAtHomeDinner(State):

    def Enter(self, gameEntity):
        if(gameEntity.HasItem("DINNER_CHICKEN")):
            out(gameEntity, "'Chicken taste GOOOOD..'")
            gameEntity.eHunger = 90
            gameEntity.RemoveItem("DINNER_CHICKEN")
            gameEntity.fsm.RevertToPriorState()
        else:
            out(gameEntity, "'NO CHICKEN!?!? Hulk will starve...'")
            # Revert and msg Hulk to go store
            gameEntity.fsm.RevertToPriorState()
            if(gameEntity.gm.GetTime() > 12 and gameEntity.gm.GetTime() < 20):
                gameEntity.gm.Broadcast(0, gameEntity.GetID(), globals.id_hulk, globals.Msg.HulkGoStore, None)

    def Execute(self, gameEntity):
        pass

    def Exit(self, gameEntity):
        pass

class HulkAtHomeSleep(State):

    def Enter(self, gameEntity):
        gameEntity.isSleeping = True
        gameEntity.gm.Broadcast(gameEntity.gm.HoursTo(7), gameEntity.GetID(), globals.id_hulk, globals.Msg.HulkWakeUp, None)

    def Execute(self, gameEntity):
        out(gameEntity, "ZZzzzZZzzz")

    def Exit(self, gameEntity):
        gameEntity.eFatigue = 95
        gameEntity.isSleeping = False

    def OnMessage(self, gameEntity, telegram):
        if(telegram.msg == globals.Msg.HulkWakeUp):
            super().OnMessage(gameEntity, telegram)
            
            out(gameEntity, "'Hulk Sleep goooood!'")
            gameEntity.fsm.RevertToPriorState()
            gameEntity.gm.Broadcast(1, gameEntity.GetID(), globals.id_hulk, globals.Msg.HulkGoWork, None)
            return True

        return False

class HulkAtStore(State):

    def Enter(self, gameEntity):
        pass

    def Execute(self, gameEntity):
        out(gameEntity, "'There you are chicken! Hulk walk home happy!'")
        gameEntity.AddItem("DINNER_CHICKEN")
        gameEntity.eMoney -= 30
        gameEntity.fsm.ChangeState(HulkTraverse())
        gameEntity.gm.Broadcast(2, gameEntity.GetID(), globals.id_hulk, globals.Msg.HulkArriveHome, None)

    def Exit(self, gameEntity):
        pass

class HulkAtWork(State):

    def Enter(self, gameEntity):
        gameEntity.isWorking = True
        gameEntity.gm.Broadcast(4 + randint(0, 2), gameEntity.GetID(), globals.id_hulk, globals.Msg.HulkGoHome, None)

    def Execute(self, gameEntity):
        out(gameEntity, "'Hulk work! Hulk SMASH! '")
        gameEntity.eMoney += 5

    def Exit(self, gameEntity):
        gameEntity.isWorking = False

    def OnMessage(self, gameEntity, telegram):
        if(telegram.msg == globals.Msg.HulkGoHome):
            super().OnMessage(gameEntity, telegram)
            
            out(gameEntity, "'Job done! Walking home!'")
            gameEntity.fsm.ChangeState(HulkTraverse())
            gameEntity.gm.Broadcast(2, gameEntity.GetID(), globals.id_hulk, globals.Msg.HulkArriveHome, None)

            return True

        return False

class HulkTraverse(State):

    def Enter(self, gameEntity):
        gameEntity.isTraversing = True

    def Execute(self, gameEntity):
        pass
        #out(gameEntity, "'Walk is booring'")

    def Exit(self, gameEntity):
        gameEntity.isTraversing = False

    def OnMessage(self, gameEntity, telegram):
        if(telegram.msg == globals.Msg.HulkArriveStore):
            super().OnMessage(gameEntity, telegram)
            
            out(gameEntity, "'Finally! Store far from Hulk's home!'")
            gameEntity.fsm.ChangeState(HulkAtStore())

            return True

        elif(telegram.msg == globals.Msg.HulkArriveHome):
            super().OnMessage(gameEntity, telegram)
            
            out(gameEntity, "'Nice house! Hulk has good taste!'")
            gameEntity.fsm.ChangeState(HulkAtHome())

            return True

        elif(telegram.msg == globals.Msg.HulkArriveWork):
            super().OnMessage(gameEntity, telegram)
            
            out(gameEntity, "'Time to smash things!'")
            gameEntity.fsm.ChangeState(HulkAtWork())

            return True

        return False