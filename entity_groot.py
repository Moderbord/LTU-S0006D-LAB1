from random import randint

from base_game_entity import BaseGameEntity
from state import State
from state_machine import StateMachine
from s_log import log
from s_print import out
import globals as G

##-----------------------------GROOT---------------------------------------##

class Groot(BaseGameEntity):

    def __init__(self, val, name, gm):
        super().__init__(val, name, gm)
        #self.location = G.locations[G.LOC_HULK_HOME]
        self.fsm.globalState = GrootGlobalstate()
        self.planGoMovies = False
        self.walkingToMovies = False
        self.money = 0

        # Groot at work
        if(self.gm.GetTime() >= 8 and self.gm.GetTime() <= 15):
            self.fsm.currentState = GrootAtWork()
            self.isWorking = True
        # Groot at home
        else:
            self.fsm.currentState = GrootAtHome()
            self.isHome = True



##------------------------------------------------------------------##
class GrootGlobalstate(State):

    def Enter(self, entity):
        pass

    def Execute(self, entity):

        if(not entity.IsSleeping()):
            entity.hunger -= 1
            entity.thirst -= 3
            entity.fatigue -= 2
            entity.social -= 2

        if(entity.gm.GetTime() == 5 and entity.IsHome()):
            if(entity.IsSleeping()):
                entity.gm.Broadcast(0, entity, G.ID.Groot, G.MSG.WakeUp, None)
            else:
                out(entity, "*Of to work* 'I am Groot...'")
                entity.fsm.ChangeState(GrootTraverse())
                # Groot slow
                entity.gm.Broadcast(3, entity, G.ID.Groot, G.MSG.ArriveWork, None)

        if(entity.gm.GetTime() == 15 and entity.IsWorking()):
            out(entity, "*End of workday* 'I am Groot.'")
            entity.fsm.ChangeState(GrootTraverse())
            entity.gm.Broadcast(3, entity, G.ID.Groot, G.MSG.ArriveHome, None)

    def Exit(self, entity):
        pass

    def OnMessage(self, entity, telegram):
        if(telegram.msg == G.MSG.D_ThorPlanGoMovies_1):
            super().OnMessage(entity, telegram)

            if(not entity.planGoMovies):
                entity.planGoMovies = True
                entity.gm.Broadcast(telegram.extraInfo - 3, entity, G.ID.Groot, G.MSG.GoMovies, None)

            # If asleep, send reminder to check phone next loop
            if(entity.IsSleeping()):
                entity.gm.Broadcast(1, entity, G.ID.Groot, G.MSG.D_ThorPlanGoMovies_1, None)
            # Awake, respond to text
            else:
                out(entity, "---> Thor #I am Groooooooot!#")
            return True

        elif(telegram.msg == G.MSG.GoMovies):
            super().OnMessage(entity, telegram)

            if(entity.IsWorking()):
                out(entity, "*Leaving work for movies* 'I am Groot, I am Groot!'")
            else:
                out(entity, "*Leaving for movies* 'I am Groot!'")

            entity.fsm.ChangeState(GrootTraverse())
            entity.walkingToMovies = True
            entity.gm.Broadcast(3, entity, G.ID.Groot, G.MSG.ArriveMovies, None)
            return True
        
        return False

##------------------------------------------------------------------##
class GrootAtHome(State):

    def Enter(self, entity):
        entity.isHome = True
        out(entity, "*Enters home*")

    def Execute(self, entity):
        if(entity.IsHungry()):
            out(entity, "*Hungry* 'I am Groot!'")
            out(entity, "*Eats fertilizer*")
            entity.hunger += 15
        elif(entity.IsThirsty()):
            out(entity, "*Thirsty* 'I am.. Groot!'")
            out(entity, "*Drinks nectar*")
            entity.thirst += 30
        elif(entity.IsTired()):
            out(entity, "*Tired* 'I.. am... Groo...'")
            entity.fsm.EnterStateBlip(GrootAtHomeSleep())
        else:
            if(entity.HasItem("BABY_GROOT")):
                out(entity, "*Dancing to music with Baby Groot*")
            else:
                out(entity, "*Dancing to music*")


    def Exit(self, entity):
        entity.isHome = False
        out(entity, "*Leaves home*")

    def OnMessage(self, entity, telegram):
        pass

##------------------------------------------------------------------##
class GrootAtHomeSleep(State):

    def Enter(self, entity):
        entity.isSleeping = True
        out(entity, "*Goes to sleep*")

    def Execute(self, entity):
        out(entity, "*Sleeping* '..'")

    def Exit(self, entity):
        entity.isSleeping = False
        out(entity, "*Yawn* 'I am groot..'")
        entity.fatigue = 75

    def OnMessage(self, entity, telegram):
        if(telegram.msg == G.MSG.WakeUp):
            super().OnMessage(entity, telegram)
            entity.fsm.RevertToPriorState()
            entity.fsm.ChangeState(GrootTraverse())
            entity.gm.Broadcast(3, entity, G.ID.Groot, G.MSG.ArriveWork, None)
            return True

        return False

##------------------------------------------------------------------##
class GrootAtWork(State):

    def Enter(self, entity):
        entity.isWorking = True
        out(entity, "*Arrives at store to work*")

    def Execute(self, entity):
        out(entity, "*Works at store*")
        entity.money += 3

        if(randint(0, 9) > 8 and entity.money >= 10):
            out(entity, "*Buys tampons*")
            entity.AddItem("TAMPONS")
            entity.money -= 10
        elif(randint(0, 9) > 8 and entity.money >= 15):
            out(entity, "*Buys Baby Groot*")
            entity.AddItem("BABY_GROOT")
            entity.money -= 15
        elif(randint(0, 9) > 8 and entity.money >= 5):
            out(entity, "*Buys a fork*")
            entity.AddItem("FORK")
            entity.money -= 5


    def Exit(self, entity):
        entity.isWorking = False
        out(entity, "*Leaves work*")

    def OnMessage(self, entity, telegram):
        pass

##------------------------------------------------------------------##
class GrootAtMovies(State):

    def Enter(self, entity):
        out(entity, "*Enters the movie saloon* 'I am Groot!'")
        entity.gm.Broadcast(0, entity, G.ID.Thor, G.MSG.GrootArriveMovies, None)
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
        entity.social += 45

    def OnMessage(self, entity, telegram):
        if(telegram.msg == G.MSG.MovieOver):
            super().OnMessage(entity, telegram)
            out(entity, "*Movie ended* 'I, am, Groot.'")
            entity.fsm.ChangeState(GrootTraverse())
            entity.gm.Broadcast(3, entity, G.ID.Groot, G.MSG.ArriveHome, None)
            return True
        
        return False

##------------------------------------------------------------------##
class GrootTraverse(State):

    def Enter(self, entity):
        entity.isTraversing = True

    def Execute(self, entity):
        pass

    def Exit(self, entity):
        entity.isTraversing = False

    def OnMessage(self, entity, telegram):
        if(telegram.msg == G.MSG.ArriveHome and not entity.walkingToMovies):
            super().OnMessage(entity, telegram)
            entity.fsm.ChangeState(GrootAtHome())
            return True

        elif(telegram.msg == G.MSG.ArriveWork and not entity.walkingToMovies):
            super().OnMessage(entity, telegram)
            entity.fsm.ChangeState(GrootAtWork())
            return True

        elif(telegram.msg == G.MSG.ArriveMovies):
            super().OnMessage(entity, telegram)
            entity.fsm.ChangeState(GrootAtMovies())
            entity.walkingToMovies = False
            return True

        return False
