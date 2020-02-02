from random import randint
from enum import Enum

from base_game_entity import BaseGameEntity
from state import State
from state_machine import StateMachine
from s_log import log
from s_print import out
import globals as G

##------------------------------HULK------------------------------##

class Hulk(BaseGameEntity):

    def __init__(self, val, name):
        super().__init__(val, name)
        self.eLocation = G.locations[G.LOC_HULK_HOME]
        self.fsm.globalState = HulkGlobalState()
        self.fsm.currentState = HulkAtHome()
        self.isHome = True

##------------------------------------------------------------------##
class HulkGlobalState(State):

    def Enter(self, entity):
        pass

    def Execute(self, entity):
        if(not entity.IsSleeping()):
            entity.hunger -= 3
            entity.thirst -= 2
            entity.fatigue -= 5
            entity.social -= 5

        if(entity.IsThirsty()):
            if(entity.IsHome() or entity.IsWorking()):
                out(entity, "'Hulk thirsty! *clunk*")
                entity.thirst += 25


    def Exit(self, entity):
        pass

    def OnMessage(self, entity, telegram):

        # Hulk goes to work
        if(telegram.msg == G.MSG.HulkGoWork):
            super().OnMessage(entity, telegram)
            
            out(entity, "'Stupid work every day! Hulk hates to go to work!'")
            entity.fsm.ChangeState(HulkTraverse())
            # Arrive in 2 loops
            entity.gm.Broadcast(2, entity, G.ID.Hulk, G.MSG.HulkArriveWork, None)
            return True

        return False

##------------------------------------------------------------------##
class HulkAtHome(State):

    def Enter(self, entity):
        entity.isHome = True
        entity.planGoPub = False

    def Execute(self, entity):
        #out(entity, "'Hulk at home!'")
        if(entity.IsHungry()):
            out(entity, "'Hulk HUNGRY!!'")
            entity.fsm.EnterStateBlip(HulkAtHomeDinner())
        elif(entity.IsTired()):
            out(entity, "'Hulk tired, go SLEEP!'")
            entity.fsm.EnterStateBlip(HulkAtHomeSleep())
        elif(entity.IsLonely() and entity.gm.GetTime() > 12 and not entity.planGoPub):
            out(entity, "'Hulk lonely! Maybe Rocket work?'")
            out(entity, "#You at the pub Rocket?#")
            entity.gm.Broadcast(0, entity, G.ID.Rocket, G.MSG.D_HulkAskRocketIfWorking_1, None)

    def Exit(self, entity):
        entity.isHome = False
        entity.planGoPub = False

    def OnMessage(self, entity, telegram):

        # Hulk goes to store
        if(telegram.msg == G.MSG.HulkGoStore):
            super().OnMessage(entity, telegram)
            
            out(entity, "'Hulk go to store! Need more chicken!'")
            entity.fsm.ChangeState(HulkTraverse())
            # Arrive in 2 loops
            entity.gm.Broadcast(2, entity, G.ID.Hulk, G.MSG.HulkArriveStore, None)
            return True

        elif(telegram.msg == G.MSG.D_HulkAskRocketIfWorking_2):
            super().OnMessage(entity, telegram)
            
            out(entity, "#Hulk come just to smash you!#")
            entity.fsm.ChangeState(HulkTraverse())
            # Arrive in 2 loops
            entity.gm.Broadcast(2, entity, G.ID.Hulk, G.MSG.HulkArrivePub, None)
            return True

        elif(telegram.msg == G.MSG.D_HulkAskRocketIfWorking_3):
            super().OnMessage(entity, telegram)
            
            out(entity, "#Good! Hulk be at the pub around " + entity.gm.ToTimeStr(entity.gm.GetTime() + telegram.extraInfo) + "#")
            entity.gm.Broadcast(telegram.extraInfo - 2, entity, G.ID.Hulk, G.MSG.HulkGoPub, None)
            entity.planGoPub = True
            return True

        elif(telegram.msg == G.MSG.HulkGoPub):
            super().OnMessage(entity, telegram)
            
            out(entity, "#Hulk walking to pub now!#")
            entity.fsm.ChangeState(HulkTraverse())
            # Arrive in 2 loops
            entity.gm.Broadcast(2, entity, G.ID.Hulk, G.MSG.HulkArrivePub, None)
            return True

        return False

##------------------------------------------------------------------##
class HulkAtHomeDinner(State):

    def Enter(self, entity):
        if(entity.HasItem("DINNER_CHICKEN")):
            out(entity, "'Chicken taste GOOOOD..'")
            entity.hunger = 90
            entity.RemoveItem("DINNER_CHICKEN")
            entity.fsm.RevertToPriorState()
        else:
            out(entity, "'NO CHICKEN!?!? Hulk will starve...'")
            # Revert and msg Hulk to go store
            entity.fsm.RevertToPriorState()
            if(entity.gm.GetTime() > 12 and entity.gm.GetTime() < 20):
                entity.gm.Broadcast(0, entity, G.ID.Hulk, G.MSG.HulkGoStore, None)

    def Execute(self, entity):
        pass

    def Exit(self, entity):
        pass

##------------------------------------------------------------------##
class HulkAtHomeSleep(State):

    def Enter(self, entity):
        entity.isSleeping = True
        # Sleep until 7:00
        entity.gm.Broadcast(entity.gm.HoursTo(7), entity, G.ID.Hulk, G.MSG.HulkWakeUp, None)

    def Execute(self, entity):
        out(entity, "ZZzzzZZzzz")

    def Exit(self, entity):
        entity.fatigue = 95
        entity.isSleeping = False

    def OnMessage(self, entity, telegram):
        if(telegram.msg == G.MSG.HulkWakeUp):
            super().OnMessage(entity, telegram)
            
            out(entity, "'Hulk Sleep goooood!'")
            entity.fsm.RevertToPriorState()
            entity.gm.Broadcast(1, entity, G.ID.Hulk, G.MSG.HulkGoWork, None)
            return True

        return False

##------------------------------------------------------------------##
class HulkAtStore(State):

    def Enter(self, entity):
        pass

    def Execute(self, entity):
        out(entity, "'There you are chicken! Hulk walk home happy!'")
        entity.AddItem("DINNER_CHICKEN")
        entity.money -= 30
        entity.fsm.ChangeState(HulkTraverse())
        entity.gm.Broadcast(2, entity, G.ID.Hulk, G.MSG.HulkArriveHome, None)

    def Exit(self, entity):
        pass

##------------------------------------------------------------------##
class HulkAtWork(State):

    def Enter(self, entity):
        entity.isWorking = True
        entity.gm.Broadcast(4 + randint(0, 2), entity, G.ID.Hulk, G.MSG.HulkGoHome, None)

    def Execute(self, entity):
        out(entity, "'Hulk work! Hulk SMASH! '")
        entity.money += 5

    def Exit(self, entity):
        entity.isWorking = False

    def OnMessage(self, entity, telegram):
        if(telegram.msg == G.MSG.HulkGoHome):
            super().OnMessage(entity, telegram)
            
            out(entity, "'Job done! Walking home!'")
            entity.fsm.ChangeState(HulkTraverse())
            entity.gm.Broadcast(2, entity, G.ID.Hulk, G.MSG.HulkArriveHome, None)

            return True

        return False

##------------------------------------------------------------------##
class HulkAtPub(State):

    def Enter(self, entity):
        out(entity, "*Walks into pub*")
        entity.isSocializing = True
        entity.gm.Broadcast(0, entity, G.ID.Rocket, G.MSG.HulkArrivePub, None)

    def Execute(self, entity):
        entity.social += 5
        out(entity, "'Rocket said he was working!'")
        entity.gm.Broadcast(1, entity, G.ID.Hulk, G.MSG.HulkGoHome, None)

    def Exit(self, entity):
        out(entity, "*Walks out from pub*")
        entity.isSocializing = False

    def OnMessage(self, entity, telegram):
        if(telegram.msg == G.MSG.HulkGoHome):
            super().OnMessage(entity, telegram)
            
            out(entity, "'No Rocket, no Hulk!'")
            entity.fsm.ChangeState(HulkTraverse())
            entity.gm.Broadcast(2, entity, G.ID.Hulk, G.MSG.HulkArriveHome, None)

            return True

        elif(telegram.msg == G.MSG.D_HulkRocketPub_1):
            super().OnMessage(entity, telegram)
            
            out(entity, "*grabs beer* 'Hulk always calm!'")
            entity.AddItem("BEER")
            entity.fsm.EnterStateBlip(HulkAtPubChillax())
            return True

        return False

##------------------------------------------------------------------##
class HulkAtPubChillax(State):

    def Enter(self, entity):
        pass

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
        
        if(entity.gm.HoursTo(9) <= 2):
            out(entity, "'Oh shit! Hulk must go to work!'")
            entity.gm.Broadcast(0, entity, G.ID.Rocket, G.MSG.D_HulkRocketPub_6, None)
            entity.fsm.RevertToPriorState()
            entity.fsm.ChangeState(HulkTraverse())
            entity.gm.Broadcast(2, entity, G.ID.Hulk, G.MSG.HulkArriveWork, None)
        elif(entity.social > 85):
            out(entity, "'Rocket good friend! Hulk must go home now'")
            entity.gm.Broadcast(0, entity, G.ID.Rocket, G.MSG.D_HulkRocketPub_6, None)
            entity.fsm.RevertToPriorState()
            entity.fsm.ChangeState(HulkTraverse())
            entity.gm.Broadcast(2, entity, G.ID.Hulk, G.MSG.HulkArriveHome, None)

    def Exit(self, entity):
        pass

    def OnMessage(self, entity, telegram):
        if(telegram.msg == G.MSG.D_HulkRocketPub_3):
            super().OnMessage(entity, telegram)
            out(entity, "'Good.. Hulk smash things'")
            return True

        if(telegram.msg == G.MSG.D_HulkRocketPub_5):
            super().OnMessage(entity, telegram)
            out(entity, "'Yes.. Hulk relaxed'")
            return True

        return False

##------------------------------------------------------------------##
class HulkTraverse(State):

    def Enter(self, entity):
        entity.isTraversing = True

    def Execute(self, entity):
        pass
        #out(entity, "'Walk is booring'")

    def Exit(self, entity):
        entity.isTraversing = False

    def OnMessage(self, entity, telegram):
        if(telegram.msg == G.MSG.HulkArriveStore):
            super().OnMessage(entity, telegram)
            
            out(entity, "'Finally! Store far from Hulk's home!'")
            entity.fsm.ChangeState(HulkAtStore())

            return True

        elif(telegram.msg == G.MSG.HulkArriveHome):
            super().OnMessage(entity, telegram)
            
            out(entity, "'Nice house! Hulk has good taste!'")
            entity.fsm.ChangeState(HulkAtHome())

            return True

        elif(telegram.msg == G.MSG.HulkArriveWork):
            super().OnMessage(entity, telegram)
            
            out(entity, "'Time to smash things!'")
            entity.fsm.ChangeState(HulkAtWork())

            return True

        elif(telegram.msg == G.MSG.HulkArrivePub):
            super().OnMessage(entity, telegram)
            
            #out(entity, "'Drink fun!'")
            entity.fsm.ChangeState(HulkAtPub())

            return True

        return False