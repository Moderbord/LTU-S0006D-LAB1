from timeit import default_timer

from telegram import Telegram
import game_manager

class MessageDispatcher:

    def __init__(self):
        self.priorityQ = {}

    def __Discharge(self, receiver, msg):
        receiver.HandleMessage(msg)

    def DispatchMessage(self, delay, senderID, receiverID, msg, extraInfo):
        receiver = game_manager.GetEntity(receiverID)
        telegram = Telegram(0, senderID, receiverID, msg, extraInfo)
        
        if(delay <= 0):
            self.__Discharge(receiver, telegram)
        else:
            currentLoop = game_manager.currentLoop
            telegram.dispatchTime = currentLoop + delay
            self.priorityQ[msg] = telegram

    def DispatchDelayedMessage(self):
        currentLoop = game_manager.currentLoop
        
        for telegram in self.priorityQ.values():
            if(telegram.dispatchTime == currentLoop):
                receiver = game_manager.GetEntity(telegram.receiverID)
                self.__Discharge(receiver, telegram)


