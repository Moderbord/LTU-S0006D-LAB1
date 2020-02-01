from time import sleep

from globals import updateIntervall

def sysout(msg):
    print(msg)
    sleep(updateIntervall)

def out(entity, msg):
    print(entity.name + ": " + msg)
    sleep(updateIntervall)

