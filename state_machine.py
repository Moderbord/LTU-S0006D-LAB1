from time import sleep

from globals import updateIntervall
from s_log import log

class StateMachine:

    def __init__(self, owner):
        # Make private?
        self.owner = owner
        self.currentState = None
        self.previousState = None
        self.globalState = None

    def Update(self):
        if(self.globalState):
            self.globalState.Execute(self.owner)

        if(self.currentState):
            self.currentState.Execute(self.owner)
        
    def ChangeState(self, newState):
        if(self.currentState and newState):
            log(str(self.owner) + " transition from " + str(self.currentState) + " to " + str(newState))
            self.previousState = self.currentState
            self.currentState.Exit(self.owner)
            self.currentState = newState
            self.currentState.Enter(self.owner)

    def EnterStateBlip(self, stateBlip):
        if(self.currentState and stateBlip):
            log(str(self.owner) + " transition from " + str(self.currentState) + " to " + str(stateBlip))
            self.previousState = self.currentState
            self.currentState = stateBlip
            self.currentState.Enter(self.owner)

    def RevertToPriorState(self):
        if(self.currentState and self.previousState):
            log(str(self.owner) + " reverting from " + str(self.currentState) + " to " + str(self.previousState))
            self.currentState.Exit(self.owner)
            self.currentState = self.previousState

    def IsInState(self, state):
        return self.currentState == state

    def HandleMessage(self, telegram):
        if(self.currentState and self.currentState.OnMessage(self.owner, telegram)):
            return True
        
        if(self.globalState and self.globalState.OnMessage(self.owner, telegram)):
            return True
        
        return False
        