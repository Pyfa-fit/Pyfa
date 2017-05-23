# skillBonusDroneNavigation
#
# Used by:
# Skill: Drone Navigation
effectType = "passive"


def handler(fit, src, context):
    lvl = src.level
    fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Drones"), "maxVelocity",
                                 src.getModifiedItemAttr("maxVelocityBonus") * lvl)
    fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"), "maxVelocity",
                                   src.getModifiedItemAttr("maxVelocityBonus") * lvl)
