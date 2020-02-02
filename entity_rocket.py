from random import randint

from base_game_entity import BaseGameEntity
from state import State
from state_machine import StateMachine
from s_log import log
from s_print import out
import globals as G

##--------------------------ROCKET-RACCOON-------------------------------------##

class Rocket(BaseGameEntity):

    def __init__(self, val, name):
        super().__init__(val, name)
        #self.location = G.locations[G.LOC_HULK_HOME]
        self.fsm.globalState = RocketGlobalstate()
        self.fsm.currentState = RocketAtWork()
        self.isWorking = True
        self.planGoMovies = False
        self.walkingToMovies = False
        self.toxicity = 0
        self.AddItem("SNACKBAR")

    def IsDrunk(self):
        return self.toxicity > 40

##------------------------------------------------------------------##
class RocketGlobalstate(State):

    def Enter(self, entity):
        pass

    def Execute(self, entity):

        entity.toxicity -= 1

        if(not entity.IsSleeping()):
            entity.hunger -= 3
            entity.thirst -= 5
            entity.fatigue -= 2
            entity.social -= 3

        if(entity.IsThirsty()):
            if(entity.IsHome() or entity.IsWorking()):
                out(entity, "'Maybe another little beer for myself..' *clunk*")
                entity.thirst += 25
                entity.toxicity += 10

        if(entity.IsHungry()):
            if(entity.HasItem("SNACKBAR")):
                out(entity, "*Eats snaskbar*")
                entity.RemoveItem("SNACKBAR")
                entity.hunger += 35

        if(entity.gm.GetTime() == 8 and entity.IsWorking()):
            out(entity, "*Yawn* 'Time to head home!'")
            entity.fsm.ChangeState(RocketTraverse())
            entity.gm.Broadcast(2, entity, G.ID.Rocket, G.MSG.ArriveHome, None)

        if(entity.gm.GetTime() == 18 and entity.IsHome()):
            if(entity.IsSleeping()):
                entity.gm.Broadcast(0, entity, G.ID.Rocket, G.MSG.WakeUp, None)
            else:
                out(entity, "'Back to work at the bar!'")
                entity.fsm.ChangeState(RocketTraverse())
                entity.gm.Broadcast(2, entity, G.ID.Rocket, G.MSG.ArriveWork, None)


    def Exit(self, entity):
        pass

    def OnMessage(self, entity, telegram):
        if(telegram.msg == G.MSG.D_HulkAskRocketIfWorking_1 and not entity.IsSleeping()):
            super().OnMessage(entity, telegram)
            
            out(entity, "---> Hulk #Not yet! I'm working in " + str(entity.gm.HoursTo(20)) + " hours.#")
            entity.gm.Broadcast(0, entity, G.ID.Hulk, G.MSG.D_HulkAskRocketIfWorking_3, entity.gm.HoursTo(20))
            return True

        elif(telegram.msg == G.MSG.D_ThorPlanGoMovies_1):
            super().OnMessage(entity, telegram)

            if(not entity.planGoMovies):
                entity.planGoMovies = True
                entity.gm.Broadcast(telegram.extraInfo - 2, entity, G.ID.Rocket, G.MSG.GoMovies, None)

            # If asleep, send reminder to check phone next loop
            if(entity.IsSleeping()):
                entity.gm.Broadcast(1, entity, G.ID.Rocket, G.MSG.D_ThorPlanGoMovies_1, None)
            # Awake, respond to text
            else:
                out(entity, "---> Thor #Sounds fun! I love movies!#")
                out(entity, "*Sets alarm*")
            return True

        elif(telegram.msg == G.MSG.GoMovies):
            super().OnMessage(entity, telegram)

            if(entity.IsWorking()):
                out(entity, "'Someone cover for me! I'm taking a break!")
            elif(entity.IsSleeping()):
                out(entity, "*Wakes from alarm* 'Time to go to the movies!'")
            else:
                out(entity, "'Of to the movies!'")

            entity.fsm.ChangeState(RocketTraverse())
            entity.walkingToMovies = True
            entity.gm.Broadcast(2, entity, G.ID.Rocket, G.MSG.ArriveMovies, None)
            return True
        
        return False

##------------------------------------------------------------------##
class RocketAtHome(State):

    def Enter(self, entity):
        entity.isHome = True
        entity.orderedPizza = False
        out(entity, "*Enters home*")

    def Execute(self, entity):
        if(entity.IsHungry() and entity.money >= 45 and not entity.orderedPizza):
            out(entity, "*Orders pizza*")
            entity.gm.Broadcast(2, entity, G.ID.Rocket, G.MSG.PizzaDelivery, None)
            entity.money -= 45
            entity.orderedPizza = True

        elif(entity.IsTired()):
            out(entity, "'Maybe a little quick nap'")
            entity.fsm.EnterStateBlip(RocketAtHomeSleep())

    def Exit(self, entity):
        entity.isHome = False
        out(entity, "*Leaves home*")

    def OnMessage(self, entity, telegram):
        if(telegram.msg == G.MSG.PizzaDelivery):
            super().OnMessage(entity, telegram)

            out(entity, "*Doorbell rings* 'PIZZA TIME!'")
            out(entity, "*Eats pizza*")
            entity.hunger = 100
            return True

        return False

##------------------------------------------------------------------##
class RocketAtHomeSleep(State):

    def Enter(self, entity):
        entity.isSleeping = True
        out(entity, "*Goes to sleep*")

    def Execute(self, entity):
        out(entity, "'zz zz'")

    def Exit(self, entity):
        entity.isSleeping = False
        entity.fatigue = 90

    def OnMessage(self, entity, telegram):
        if(telegram.msg == G.MSG.PizzaDelivery):
            super().OnMessage(entity, telegram)
            out(entity, "*Doorbell rings* 'PIZZA TIME!'")
            out(entity, "*Wakes up*")
            entity.fsm.RevertToPriorState()
            out(entity, "*Eats pizza*")
            entity.hunger = 100
            return True
        
        elif(telegram.msg == G.MSG.WakeUp):
            super().OnMessage(entity, telegram)
            out(entity, "*Yaaaawn* 'I guess it's back to work..'")
            entity.fsm.RevertToPriorState()
            entity.fsm.ChangeState(RocketTraverse())
            entity.gm.Broadcast(2, entity, G.ID.Rocket, G.MSG.ArriveWork, None)
            return True

        return False
##------------------------------------------------------------------##
class RocketAtWork(State):

    def Enter(self, entity):
        entity.isWorking = True
        out(entity, "*Arrives at the pub to work*")
        out(entity, "*Grabs todays snackbar*")
        entity.AddItem("SNACKBAR")

    def Execute(self, entity):
        out(entity, "*Serving customers*")
        entity.money += 3

    def Exit(self, entity):
        out(entity, "*Leaves work*")
        entity.isWorking = False

    def OnMessage(self, entity, telegram):
        # Hulk ask if Rocket is working
        if(telegram.msg == G.MSG.D_HulkAskRocketIfWorking_1):
            super().OnMessage(entity, telegram)
            out(entity, "---> Hulk #Sure am! You lonely broccoli boy? Come over then!#")
            entity.gm.Broadcast(0, entity, G.ID.Hulk, G.MSG.D_HulkAskRocketIfWorking_2, None)
            return True

        elif(telegram.msg == G.MSG.HulkArrivePub):
            super().OnMessage(entity, telegram)
            out(entity, "'There you are! Calmed down yet, big guy? Here, grab a beer and follow me will ya?'")
            entity.fsm.EnterStateBlip(RocketAtWorkChillax())
            entity.gm.Broadcast(0, entity, G.ID.Hulk, G.MSG.D_HulkRocketPub_1, None)
            return True

        return False

##------------------------------------------------------------------##
class RocketAtWorkChillax(State):

    def Enter(self, entity):
        entity.isSocializing = True
        out(entity, "'There is plenty of snacks and drinks, help yourself!'")
        # Start talking in a moment
        entity.gm.Broadcast(2, entity, G.ID.Rocket, G.MSG.D_HulkRocketPub_2, None)

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
        if(telegram.msg == G.MSG.D_HulkRocketPub_2):
            super().OnMessage(entity, telegram)
            out(entity, "'So big guy, how ya day been?'")
            entity.gm.Broadcast(0, entity, G.ID.Hulk, G.MSG.D_HulkRocketPub_3, None)
            # Pause between dialogue
            entity.gm.Broadcast(2, entity, G.ID.Rocket, G.MSG.D_HulkRocketPub_4, None)
            return True

        elif(telegram.msg == G.MSG.D_HulkRocketPub_4):
            super().OnMessage(entity, telegram)
            out(entity, "'This is nice...'")
            entity.gm.Broadcast(0, entity, G.ID.Hulk, G.MSG.D_HulkRocketPub_5, None)
            return True

        elif(telegram.msg == G.MSG.D_HulkRocketPub_6):
            super().OnMessage(entity, telegram)
            out(entity, "'Catch you later Hulk!'")
            entity.fsm.RevertToPriorState()
            return True

        return False

##------------------------------------------------------------------##
class RocketAtMovies(State):

    def Enter(self, entity):
        out(entity, "*Enters the movie saloon* 'Rocket is here!'")
        entity.gm.Broadcast(0, entity, G.ID.Thor, G.MSG.RocketArriveMovies, None)
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

    def OnMessage(self, entity, telegram):
        if(telegram.msg == G.MSG.MovieOver):
            super().OnMessage(entity, telegram)
            out(entity, "*Movie ended* 'That was fun! Cya later!'")
            entity.fsm.ChangeState(RocketTraverse())
            entity.gm.Broadcast(2, entity, G.ID.Rocket, G.MSG.ArriveHome, None)
            return True
        
        return False

##------------------------------------------------------------------##
class RocketTraverse(State):

    def Enter(self, entity):
        entity.isTraversing = True

    def Execute(self, entity):
        pass

    def Exit(self, entity):
        entity.isTraversing = False

    def OnMessage(self, entity, telegram):
        if(telegram.msg == G.MSG.ArriveHome and not entity.walkingToMovies):
            super().OnMessage(entity, telegram)
            entity.fsm.ChangeState(RocketAtHome())
            return True

        elif(telegram.msg == G.MSG.ArriveWork and not entity.walkingToMovies):
            super().OnMessage(entity, telegram)
            entity.fsm.ChangeState(RocketAtWork())
            return True

        elif(telegram.msg == G.MSG.ArriveMovies):
            super().OnMessage(entity, telegram)
            entity.fsm.ChangeState(RocketAtMovies())
            entity.walkingToMovies = False
            return True

        return False