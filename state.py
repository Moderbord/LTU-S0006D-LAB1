from s_log import log

class State:

    def Enter(self, gameEntity):
        pass

    def Execute(self, gameEntity):
        pass

    def Exit(self, gameEntity):
        pass

    def OnMessage(self, gameEntity, telegram):
        log("At loop " + str(gameEntity.gm.GetLoop()) + ", " + gameEntity.eName +
            " recieved message from " + str(gameEntity.gm.GetEntityName(telegram.senderID)) +
            " with message: " + str(telegram.msg) + ". Dispatch time: " +
             str(telegram.dispatchTime))