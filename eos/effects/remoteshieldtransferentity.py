# remoteShieldTransferEntity
#
# Used by:
# Drones named like: Shield Maintenance Bot (6 of 6)
effectType = "projected", "active"


def handler(fit, container, context):
    if "projected" in context:
        bonus = container.getModifiedItemAttr("shieldBonus")
        duration = container.cycleTime / 1000.0
        fit.extraAttributes.increase("shieldRepair", bonus / duration)
