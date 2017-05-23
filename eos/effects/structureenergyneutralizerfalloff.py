# Not used by any item
from eos.saveddata.module import State

effectType = "active", "projected"


def handler(fit, container, context):
    amount = 0
    if "projected" in context:
        if (hasattr(container, "state") and container.state >= State.ACTIVE) or hasattr(container, "amountActive"):
            amount = container.getModifiedItemAttr("energyNeutralizerAmount")
            time = container.cycleTime
            fit.addDrain(container, time, amount, 0)
