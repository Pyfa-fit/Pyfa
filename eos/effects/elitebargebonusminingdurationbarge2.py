# eliteBargeBonusMiningDurationBarge2
#
# Used by:
# Ships from group: Exhumer (3 of 3)
effectType = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Mining"),
                                  "duration", ship.getModifiedItemAttr("eliteBonusBarge2"), skill="Exhumers")
