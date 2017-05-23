# remoteArmorRepairEntity
#
# Used by:
# Drones named like: Armor Maintenance Bot (6 of 6)
effectType = "projected", "active"


def handler(fit, container, context):
    if "projected" in context:
        bonus = container.getModifiedItemAttr("armorDamageAmount")
        duration = container.cycleTime / 1000.0
        fit.extraAttributes.increase("armorRepair", bonus / duration)
