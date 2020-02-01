from entity_manager import EntityManager
from message_dispatcher import MessageDispatcher
from game_time import GameTime
from s_log import log

class GameManager:

    def __init__(self):
        self.entityManager = EntityManager()
        self.messageDispatcher = MessageDispatcher(self)
        self.gameTime = GameTime()

    def AddEntity(self, entity):
        # Give reference to game manager to new entity
        entity.gm = self
        self.entityManager.Register(entity)

    def GetEntityName(self, ID):
        return self.entityManager.GetFromID(ID).name

    def GetEntity(self, ID):
        return self.entityManager.GetFromID(ID)

    def Broadcast(self, delay, sender, receiverID, msg, extraInfo):
        log("At loop " + str(self.gameTime.GetLoop()) + ", " + str(self.entityManager.GetFromID(sender.GetID()).name) +
        " sent message to " + str(self.entityManager.GetFromID(receiverID).name) + " with message: " +
        str(msg) + ". Delay: " + str(delay))
        self.messageDispatcher.DispatchMessage(delay, sender.GetID(), receiverID, msg, extraInfo)

    def NextTimeStep(self):
        self.gameTime.NextTimestep()

    def HoursTo(self, time):
        return self.gameTime.HoursTo(time)

    def GetTime(self):
        return self.gameTime.GetTime()

    def GetTimeStr(self):
        return self.gameTime.GetTimeStr()

    def GetWeekday(self):
        return self.gameTime.GetWeekday()

    def GetWeekdayStr(self):
        return self.gameTime.GetWeekdayStr()

    def NextLoop(self):
        self.gameTime.NextLoop()

    def GetLoop(self):
        return self.gameTime.GetLoop()

