# Not used by any item
from eos.saveddata.module import State

effectType = "active", "projected"


def handler(fit, src, context):
    if "projected" in context and ((hasattr(src, "state") and src.state >= State.ACTIVE) or hasattr(src, "amountActive")):
        multiplier = src.amountActive if hasattr(src, "amountActive") else 1
        amount = src.getModifiedItemAttr("energyNeutralizerAmount")
        time = src.cycleTime
        fit.addDrain(src, time, amount * multiplier, 0)
