from timeit import default_timer

from entities import Miner
from entities import Wife
import entity_hulk
import entity_rocket
import entity_thor
import entity_groot

from s_log import log
from s_print import sysout
from game_manager import GameManager
import globals as G


# New run
log("-------- NEW RUN --------\n")

#inits
gm = GameManager()

# Give reference to game manager to new entity
hulk = entity_hulk.Hulk(G.ID.Hulk, "Hulk", gm)
rocket = entity_rocket.Rocket(G.ID.Rocket, "Rocket", gm)
thor = entity_thor.Thor(G.ID.Thor, "Thor", gm)
groot = entity_groot.Groot(G.ID.Groot, "Groot", gm)
gm.AddEntity(hulk)
gm.AddEntity(rocket)
gm.AddEntity(thor)
gm.AddEntity(groot)

#bob = Miner(globals.id_bob)
#elsie = Wife(globals.id_elsie)

#game_manager.AddEntity(bob)
#game_manager.AddEntity(elsie)

#Game loop
loops = 720
for i in range(loops):

    # logs before update
    sysout(gm.GetWeekdayStr() + " " + gm.GetTimeStr() + ", Update loop: " + str(i))
    log("¤--> " + gm.GetWeekdayStr() + " " + gm.GetTimeStr() + ", Update loop: " + str(i) + "\n")
    log("<Pre vals>")
    hulk.logStates()
    rocket.logStates()
    thor.logStates()
    groot.logStates()

    # Game update
    log("\n<update>")
    gm.messageDispatcher.DispatchDelayedMessage()
    # Entities goes here
    hulk.Update()
    rocket.Update()
    thor.Update()
    groot.Update()

    # logs after update
    log("\n<Post vals>")
    hulk.logStates()
    rocket.logStates()
    thor.logStates()
    groot.logStates()
    log("")
    print("\n")

    gm.NextTimeStep()
    gm.NextLoop()

# End of run
log("-------- END OF RUN --------\n")


