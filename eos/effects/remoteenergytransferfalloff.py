# remoteEnergyTransferFalloff
#
# Used by:
# Modules from group: Remote Capacitor Transmitter (41 of 41)
effectType = "projected", "active"


def handler(fit, src, context):
    if "projected" in context:
        amount = src.getModifiedItemAttr("powerTransferAmount")
        duration = src.cycleTime
        fit.addDrain(src, duration, -amount, 0)
