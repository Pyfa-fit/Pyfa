# iceHarvesterDurationMultiplier
#
# Used by:
# Ship: Endurance
effectType = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemMultiply(lambda mod: mod.item.requiresSkill("Ice Harvesting"),
                                     "duration", ship.getModifiedItemAttr("iceHarvestCycleBonus"))
