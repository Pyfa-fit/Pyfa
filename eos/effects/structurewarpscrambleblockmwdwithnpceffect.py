# Not used by any item
from eos.saveddata.module import State

# Not used by any item
runTime = "early"
effectType = "projected", "active"


def handler(fit, container, context):
    if "projected" not in context:
        return
    # this is such a dirty hack
    for mod in fit.modules:
        if not mod.isEmpty and mod.item.requiresSkill("High Speed Maneuvering") and mod.state > State.ONLINE:
            mod.state = State.ONLINE
