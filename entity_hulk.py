from random import randint

from base_game_entity import BaseGameEntity
from state import State
from state_machine import StateMachine
from s_log import log
from s_print import out
import globals as G

##------------------------------HULK------------------------------##

class Hulk(BaseGameEntity):

    def __init__(self, val, name, gm):
        super().__init__(val, name, gm)
        self.eLocation = G.locations[G.LOC_HULK_HOME]
        self.fsm.globalState = HulkGlobalState()
        self.planGoMovies = False
        self.walkingToMovies = False

        # Hulk at work
        if(self.gm.GetTime() >= 9 and self.gm.GetTime() <= 12):
            self.fsm.currentState = HulkAtWork()
            self.isWorking = True
        # Hulk at home
        else:
            self.fsm.currentState = HulkAtHome()
            self.isHome = True

##------------------------------------------------------------------##
class HulkGlobalState(State):

    def Enter(self, entity):
        pass

    def Execute(self, entity):
        if(not entity.IsSleeping()):
            entity.hunger -= 4
            entity.thirst -= 2
            entity.fatigue -= 4
            entity.social -= 5

        if(entity.IsThirsty()):
            if(entity.IsHome() or entity.IsWorking()):
                out(entity, "'Hulk thirsty! *clunk*")
                entity.thirst += 25

        if(entity.gm.GetTime() == 13 and entity.IsWorking()):
            entity.gm.Broadcast(randint(0, 2), entity, G.ID.Hulk, G.MSG.GoHome, None)


    def Exit(self, entity):
        pass

    def OnMessage(self, entity, telegram):
        # Hulk goes to work
        if(telegram.msg == G.MSG.GoWork):
            super().OnMessage(entity, telegram)
            
            out(entity, "'Stupid work every day! Hulk hates to go to work!'")
            entity.fsm.ChangeState(HulkTraverse())
            # Arrive in 2 loops
            entity.gm.Broadcast(2, entity, G.ID.Hulk, G.MSG.ArriveWork, None)
            return True

        # Plan for movie
        elif(telegram.msg == G.MSG.D_ThorPlanGoMovies_1):
            super().OnMessage(entity, telegram)

            if(not entity.planGoMovies):
                entity.planGoMovies = True
                entity.gm.Broadcast(telegram.extraInfo - 2, entity, G.ID.Hulk, G.MSG.GoMovies, None)

            # If asleep, send reminder to check phone next loop
            if(entity.IsSleeping()):
                entity.gm.Broadcast(1, entity, G.ID.Hulk, G.MSG.D_ThorPlanGoMovies_1, None)
            # Awake, respond to text
            else:
                out(entity, "---> Thor #Hulk want to see movie! Hulk come!#")
            return True

        elif(telegram.msg == G.MSG.GoMovies):
            super().OnMessage(entity, telegram)

            if(entity.IsHungry()):
                out(entity, "'Hulk hungry, can't come! Hulk starve!")
                out(entity, "---> Thor #Hulk sorry! Can't come!#")
                entity.planGoMovies = False
                return True
            elif(entity.IsSleeping()):
                out(entity, "*Wakes up* 'Right! Must go to movies with Thor!'")
            else:
                out(entity, "'Must go to movies with Thor!'")

            entity.fsm.ChangeState(HulkTraverse())
            entity.walkingToMovies = True
            entity.gm.Broadcast(2, entity, G.ID.Hulk, G.MSG.ArriveMovies, None)
            return True

        return False

##------------------------------------------------------------------##
class HulkAtHome(State):

    def Enter(self, entity):
        entity.isHome = True
        entity.planGoPub = False
        out(entity, "*Enters home* 'Nice house! Hulk has good taste!'")

    def Execute(self, entity):
        if(entity.IsHungry()):
            out(entity, "'Hulk HUNGRY!!'")
            entity.fsm.EnterStateBlip(HulkAtHomeDinner())
        elif(entity.IsTired()):
            out(entity, "'Hulk tired, go SLEEP!'")
            entity.fsm.EnterStateBlip(HulkAtHomeSleep())
        elif(entity.IsLonely() and entity.gm.GetTime() > 12 and not entity.planGoPub):
            out(entity, "'Hulk lonely! Maybe Rocket work?'")
            out(entity, "---> Rocket #You at the pub?#")
            entity.gm.Broadcast(0, entity, G.ID.Rocket, G.MSG.D_HulkAskRocketIfWorking_1, None)
        else:
            out(entity, "*Watches TV*")

    def Exit(self, entity):
        entity.isHome = False
        entity.planGoPub = False
        out(entity, "*Leaves home*")

    def OnMessage(self, entity, telegram):

        # Hulk goes to store
        if(telegram.msg == G.MSG.GoStore):
            super().OnMessage(entity, telegram)
            out(entity, "'Hulk go to store! Need more chicken!'")
            entity.fsm.ChangeState(HulkTraverse())
            # Arrive in 2 loops
            entity.gm.Broadcast(2, entity, G.ID.Hulk, G.MSG.ArriveStore, None)
            return True

        # Rocket works
        elif(telegram.msg == G.MSG.D_HulkAskRocketIfWorking_2):
            super().OnMessage(entity, telegram)
            out(entity, "---> Rocket #Hulk come just to smash you!#")
            entity.fsm.ChangeState(HulkTraverse())
            # Arrive in 2 loops
            entity.gm.Broadcast(2, entity, G.ID.Hulk, G.MSG.ArrivePub, None)
            return True

        # Rocket works soon, plan to go
        elif(telegram.msg == G.MSG.D_HulkAskRocketIfWorking_3):
            super().OnMessage(entity, telegram)
            out(entity, "---> Rocket #Good! Hulk be at the pub around " + entity.gm.ToTimeStr(entity.gm.GetTime() + telegram.extraInfo) + "#")
            entity.gm.Broadcast(telegram.extraInfo - 2, entity, G.ID.Hulk, G.MSG.GoPub, None)
            entity.planGoPub = True
            return True

        # Follow plan and go pub
        elif(telegram.msg == G.MSG.GoPub):
            super().OnMessage(entity, telegram)
            out(entity, "---> Rocket #Hulk walking to pub now!#")
            entity.fsm.ChangeState(HulkTraverse())
            entity.gm.Broadcast(2, entity, G.ID.Hulk, G.MSG.ArrivePub, None)
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
            entity.gm.Broadcast(0, entity, G.ID.Hulk, G.MSG.GoStore, None)

    def Execute(self, entity):
        pass

    def Exit(self, entity):
        pass

##------------------------------------------------------------------##
class HulkAtHomeSleep(State):

    def Enter(self, entity):
        entity.isSleeping = True
        # Sleep until 7:00
        entity.gm.Broadcast(entity.gm.HoursTo(7), entity, G.ID.Hulk, G.MSG.WakeUp, None)

    def Execute(self, entity):
        out(entity, "'ZZzzzZZzzz'")

    def Exit(self, entity):
        entity.fatigue = 95
        entity.isSleeping = False

    def OnMessage(self, entity, telegram):
        if(telegram.msg == G.MSG.WakeUp):
            super().OnMessage(entity, telegram)
            
            out(entity, "'Hulk Sleep goooood!'")
            entity.fsm.RevertToPriorState()
            entity.gm.Broadcast(1, entity, G.ID.Hulk, G.MSG.GoWork, None)
            return True

        return False

##------------------------------------------------------------------##
class HulkAtStore(State):

    def Enter(self, entity):
        out(entity, "*Enters store* 'Finally! Store far from Hulk's home!'")

    def Execute(self, entity):
        out(entity, "*Finds chicken* 'There you are chicken! Hulk walk home happy!'")
        entity.AddItem("DINNER_CHICKEN")
        entity.money -= 30
        entity.fsm.ChangeState(HulkTraverse())
        entity.gm.Broadcast(2, entity, G.ID.Hulk, G.MSG.ArriveHome, None)

    def Exit(self, entity):
        out(entity, "*Leaves store*")

##------------------------------------------------------------------##
class HulkAtWork(State):

    def Enter(self, entity):
        entity.isWorking = True
        out(entity, "*Enters work* 'Time to smash things!'")

    def Execute(self, entity):
        out(entity, "'Hulk work! Hulk SMASH! '")
        entity.money += 5

    def Exit(self, entity):
        entity.isWorking = False
        out(entity, "*Leaves work*")

    def OnMessage(self, entity, telegram):
        if(telegram.msg == G.MSG.GoHome):
            super().OnMessage(entity, telegram)
            
            out(entity, "'Job done! Walking home!'")
            entity.fsm.ChangeState(HulkTraverse())
            entity.gm.Broadcast(2, entity, G.ID.Hulk, G.MSG.ArriveHome, None)

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
        entity.gm.Broadcast(1, entity, G.ID.Hulk, G.MSG.GoHome, None)

    def Exit(self, entity):
        out(entity, "*Walks out from pub*")
        entity.isSocializing = False

    def OnMessage(self, entity, telegram):
        if(telegram.msg == G.MSG.GoHome):
            super().OnMessage(entity, telegram)
            
            out(entity, "'No Rocket, no Hulk!'")
            entity.fsm.ChangeState(HulkTraverse())
            entity.gm.Broadcast(2, entity, G.ID.Hulk, G.MSG.ArriveHome, None)

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
            entity.gm.Broadcast(2, entity, G.ID.Hulk, G.MSG.ArriveWork, None)
        elif(entity.social > 85):
            out(entity, "'Rocket good friend! Hulk must go home now'")
            entity.gm.Broadcast(0, entity, G.ID.Rocket, G.MSG.D_HulkRocketPub_6, None)
            entity.fsm.RevertToPriorState()
            entity.fsm.ChangeState(HulkTraverse())
            entity.gm.Broadcast(2, entity, G.ID.Hulk, G.MSG.ArriveHome, None)

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
class HulkAtMovies(State):

    def Enter(self, entity):
        out(entity, "*Enters the movie saloon* 'Hulk watch movie!'")
        entity.gm.Broadcast(0, entity, G.ID.Thor, G.MSG.HulkArriveMovies, None)
        entity.planGoMovies = False
        entity.wathingMovie = False

    def Execute(self, entity):
        if(entity.wathingMovie):
            out(entity, "*Watches movie*")
        else:
            entity.wathingMovie = True

    def Exit(self, entity):
        out(entity, "*Exits the movie saloon*")
        entity.planGoMovies = False
        entity.wathingMovie = False
        entity.social = 50

    def OnMessage(self, entity, telegram):
        if(telegram.msg == G.MSG.MovieOver):
            super().OnMessage(entity, telegram)
            out(entity, "*Movie ended* 'Hulk entertained! Now go home!'")
            entity.fsm.ChangeState(HulkTraverse())
            entity.gm.Broadcast(2, entity, G.ID.Hulk, G.MSG.ArriveHome, None)
            return True
        
        return False


##------------------------------------------------------------------##
class HulkTraverse(State):

    def Enter(self, entity):
        entity.isTraversing = True

    def Execute(self, entity):
        pass

    def Exit(self, entity):
        entity.isTraversing = False

    def OnMessage(self, entity, telegram):
        if(telegram.msg == G.MSG.ArriveStore and not entity.walkingToMovies):
            super().OnMessage(entity, telegram)
            entity.fsm.ChangeState(HulkAtStore())
            return True

        elif(telegram.msg == G.MSG.ArriveHome and not entity.walkingToMovies):
            super().OnMessage(entity, telegram)
            entity.fsm.ChangeState(HulkAtHome())
            return True

        elif(telegram.msg == G.MSG.ArriveWork and not entity.walkingToMovies):
            super().OnMessage(entity, telegram)
            entity.fsm.ChangeState(HulkAtWork())
            return True

        elif(telegram.msg == G.MSG.ArrivePub and not entity.walkingToMovies):
            super().OnMessage(entity, telegram)
            entity.fsm.ChangeState(HulkAtPub())
            return True

        elif(telegram.msg == G.MSG.ArriveMovies):
            super().OnMessage(entity, telegram)
            entity.fsm.ChangeState(HulkAtMovies())
            entity.walkingToMovies = False
            return True

        return False