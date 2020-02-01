from entity_manager import EntityManager
from message_dispatcher import MessageDispatcher
from game_time import GameTime
from s_log import log

__entityManager = EntityManager()
__messageDispatcher = MessageDispatcher()
__gameTime = GameTime()

def AddEntity(entity):
    __entityManager.Register(entity)

def GetEntityName(ID):
    return __entityManager.GetFromID(ID).eName

def GetEntity(ID):
    return __entityManager.GetFromID(ID)

def Broadcast(delay, senderID, receiverID, msg, extraInfo):
    log("At loop " + str(__gameTime.GetLoop()) + ", " + str(__entityManager.GetFromID(senderID).eName) +
     " sent message to " + str(__entityManager.GetFromID(receiverID).eName) + " with message: " +
      str(msg) + ". Delay: " + str(delay))
    __messageDispatcher.DispatchMessage(delay, senderID, receiverID, msg, extraInfo)

def NextTimeStep():
    __gameTime.NextTimestep()

def GetTime():
    return __gameTime.GetTime()

def GetWeekday():
    return __gameTime.GetWeekday()

def NextLoop():
    __gameTime.NextLoop()

def GetLoop():
    return __gameTime.GetLoop()

