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

class Miner(BaseGameEntity):

    def __init__(self, val):
        super().__init__(val)
        self.location = "Mine"
        self.moneyInBank = 10
        self.goldCarried = 19
        self.thirst = 0
        self.fatigue = 10
        self.fsm = StateMachine(self)
        self.fsm.globalState = MinerGlobalState()
        self.fsm.currentState = MineForGold()

    def Update(self):
        self.fsm.Update()

    def IsThirsty(self):
        return self.thirst >= 10

    def IsTired(self):
        return self.fatigue >= 10

    def IsWealthy(self):
        return self.goldCarried >= 20

    def HandleMessage(self, telegram):
        return self.fsm.HandleMessage(telegram)

    def logStates(self):
        log(str(self) + " global state: " + str(self.fsm.globalState))
        log(str(self) + " current state: " + str(self.fsm.currentState))
        log(str(self) + " previous state: " + str(self.fsm.previousState))
        log(str(self) + " location: " + self.location)
        log(str(self) + " moneyInBank: " + str(self.moneyInBank))
        log(str(self) + " goldCarried: " + str(self.goldCarried))
        log(str(self) + " thirst: " + str(self.thirst))
        log(str(self) + " fatigue: " + str(self.fatigue))

class MinerGlobalState(State):

    def Enter(self, gameEntity):
        pass

    def Execute(self, gameEntity):
        if(gameEntity.location == "Mine"):
            if(randint(0, 9) > 8):
                gameEntity.fsm.EnterStateBlip(MinerThinking())

    def Exit(self, gameEntity):
        pass

class HomeAndSleep(State):

    def Enter(self, gameEntity):
        out("Sore and tired you arrive back at home")
        out("Honey i'm home!")
        gameEntity.location = "Home"

        game_manager.Broadcast(0, gameEntity.GetID(), globals.id_elsie, Msg.HiHoneyImHome, None)

    def Execute(self, gameEntity):
        out("*Snore*")
        gameEntity.thirst += 1
        gameEntity.fatigue -= 2
        if(gameEntity.fatigue <= 2):
            gameEntity.fsm.ChangeState(MineForGold())

    def Exit(self, gameEntity):
        out("Refreshed, you head back to the mine")

    def OnMessage(self, gameEntity, telegram):
        if(telegram.msg == Msg.StewReady):
            super().OnMessage(gameEntity, telegram)
            
            out("Alright honey! I'm coming!")
            gameEntity.fsm.EnterStateBlip(EatStew())

            return True
        return False

class EatStew(State):

    def Enter(self, gameEntity):
        out("Smells real nice Elsie!")

    def Execute(self, gameEntity):
        out("Taste super good as well!")
        gameEntity.fsm.RevertToPriorState()

    def Exit(self, gameEntity):
        out("Thank you wifey! Time to get back to whatever i was doin")

class DepositAtBank(State):

    def Enter(self, gameEntity):
        out("Your enter the bank with pockets filled to the brim with gold")
        gameEntity.location = "Bank"

    def Execute(self, gameEntity):
        out("You shower the local peasants in a golden rain")
        gameEntity.goldCarried -= 5
        gameEntity.moneyInBank += 3
        if(gameEntity.goldCarried < 5):
            gameEntity.fsm.ChangeState(MineForGold())
        elif(gameEntity.IsTired()):
            gameEntity.fsm.ChangeState(HomeAndSleep())

    def Exit(self, gameEntity):
        out("With the pockets finally empty, you head back to the mine")

class MineForGold(State):

    def Enter(self, gameEntity):
        out("Back at the mine you grab your tools and get to work")
        gameEntity.location = "Mine"

    def Execute(self, gameEntity):
        out("*Chunk*")
        gameEntity.fatigue += 1
        gameEntity.thirst += 2
        gameEntity.goldCarried += 4

        if(gameEntity.IsThirsty()):
            gameEntity.fsm.ChangeState(SaloonAndDrink())
        elif(gameEntity.IsWealthy()):
            gameEntity.fsm.ChangeState(DepositAtBank())

    def Exit(self, gameEntity):
        if(gameEntity.IsThirsty()):
            out("...*Chunk* That is it! You need a drink!")
        elif(gameEntity.IsWealthy()):
            out("...*Chunk* Phew.. You can not carry any more gold!")

class MinerThinking(State):

    def Enter(self, gameEntity):
        pass

    def Execute(self, gameEntity):
        out("'Wonder what i'll do tomorrow?'")
        gameEntity.fsm.RevertToPriorState()

    def Exit(self, gameEntity):
        out("'Ayee, snap out of it'")

class SaloonAndDrink(State):

    def Enter(self, gameEntity):
        out("You hastily travel to the saloon")
        gameEntity.location = "Saloon"

    def Execute(self, gameEntity):
        out("*Chug*")
        gameEntity.thirst -= 2
        if(gameEntity.thirst <= 2):
            gameEntity.fsm.ChangeState(MineForGold())

    def Exit(self, gameEntity):
        out("Sated, you stumble back to the mine")

# --------------------------------------------------------------- WIFE

class Wife(BaseGameEntity):

    def __init__(self, val):
        super().__init__(val)
        self.location = "Home"
        self.peeNeed = 5
        self.cookingStew = False
        self.fsm = StateMachine(self)
        self.fsm.globalState = WifeGlobalState()
        self.fsm.currentState = WifeClean()

    def Update(self):
        self.fsm.Update()

    def NeedToRelief(self):
        return self.peeNeed >= 10

    def CookingStew(self):
        return self.cookingStew

    def HandleMessage(self, telegram):
        return self.fsm.HandleMessage(telegram)

    def logStates(self):
        log(str(self) + " global state: " + str(self.fsm.globalState))
        log(str(self) + " current state: " + str(self.fsm.currentState))
        log(str(self) + " previous state: " + str(self.fsm.previousState))
        log(str(self) + " location: " + self.location)
        log(str(self) + " peeNeed: " + str(self.peeNeed))
        log(str(self) + " cookingStew: " + str(self.cookingStew))

class WifeGlobalState(State):

    def Enter(self, gameEntity):
        pass

    def Execute(self, gameEntity):
        if(gameEntity.NeedToRelief()):
            gameEntity.fsm.EnterStateBlip(WifeToilet())

    def Exit(self, gameEntity):
        pass

    def OnMessage(self, gameEntity, telegram):
        if(telegram.msg == Msg.HiHoneyImHome):
            super().OnMessage(gameEntity, telegram)

            out("Hi honey! Let me make ye some stew!")
            gameEntity.fsm.ChangeState(MakeStew())

            return True
        return False

class MakeStew(State):

    def Enter(self, gameEntity):
        if (not gameEntity.CookingStew()):
            out("Putting on some stew")

            game_manager.Broadcast(2, gameEntity.GetID(), globals.id_elsie, Msg.StewReady, None)
            gameEntity.cookingStew = True

    def Execute(self, gameEntity):
        out("*Waiting for stew*")

    def Exit(self, gameEntity):
        out("*Putting food in front of Bob*")
        out("Oh, almost forgot to clean! Have a nice meal darling")

    def OnMessage(self, gameEntity, telegram):
        if(telegram.msg == Msg.StewReady):
            super().OnMessage(gameEntity, telegram)

            out("Stew is ready Bob!")

            game_manager.Broadcast(0, gameEntity.GetID(), globals.id_bob, Msg.StewReady, None)
            gameEntity.cookingStew = False
            gameEntity.fsm.ChangeState(WifeClean())

            return True
        return False

class WifeToilet(State):

    def Enter(self, gameEntity):
        out("Ohhh noe, nature's calling again!")

    def Execute(self, gameEntity):
        out("Ahhhhh! Sweet relief!")
        gameEntity.peeNeed  -= 10
        gameEntity.fsm.RevertToPriorState()

    def Exit(self, gameEntity):
        out("*flush* Household's waiting!")

class WifeClean(State):

    def Enter(self, gameEntity):
        pass

    def Execute(self, gameEntity):
        out("Doin some cleaning for my love!")
        gameEntity.peeNeed  += 7

    def Exit(self, gameEntity):
        pass

# --------------------------------------------------------------- MESSAGES

class Msg(Enum):
    HiHoneyImHome = 1
    StewReady = 2