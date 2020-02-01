from s_log import log
import game_manager

class State:

    def Enter(self, gameEntity):
        pass

    def Execute(self, gameEntity):
        pass

    def Exit(self, gameEntity):
        pass

    def OnMessage(self, gameEntity, telegram):
        log("At loop " + str(game_manager.currentLoop) + ", " + gameEntity.eName +
            " recieved message from " + str(game_manager.GetEntityName(telegram.senderID)) +
            " with message: " + str(telegram.msg) + ". Dispatch time: " +
             str(telegram.dispatchTime))