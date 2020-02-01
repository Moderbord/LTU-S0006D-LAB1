class Telegram:

    def __init__(self, delay, senderID, receiverID, msg, extraInfo):
        self.senderID = senderID
        self.receiverID = receiverID
        self.msg = msg
        self.dispatchTime = delay
        self.extraInfo = extraInfo