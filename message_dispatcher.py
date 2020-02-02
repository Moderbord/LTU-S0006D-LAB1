from timeit import default_timer
from copy import copy

from telegram import Telegram
import game_manager

class MessageDispatcher:

    def __init__(self, gm):
        self.gm = gm
        self.priorityQ = {}
        # TODO queues for separate entities

    def __Discharge(self, receiver, msg):
        receiver.HandleMessage(msg)

    def DispatchMessage(self, delay, senderID, receiverID, msg, extraInfo):
        receiver = self.gm.GetEntity(receiverID)
        telegram = Telegram(0, senderID, receiverID, msg, extraInfo)
        
        if(delay <= 0):
            self.__Discharge(receiver, telegram)
        else:
            currentLoop = self.gm.GetLoop()
            telegram.dispatchTime = currentLoop + delay
            key = str(senderID) + str(msg) + str(receiverID)
            self.priorityQ[key] = telegram

    def DispatchDelayedMessage(self):
        currentLoop = self.gm.GetLoop()
        # Loop through copy so main queue can change during loop
        copiedQ = copy(self.priorityQ)
        
        for telegram in copiedQ.values():
            if(telegram.dispatchTime == currentLoop):
                receiver = self.gm.GetEntity(telegram.receiverID)
                self.__Discharge(receiver, telegram)


