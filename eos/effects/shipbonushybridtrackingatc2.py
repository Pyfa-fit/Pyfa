# shipBonusHybridTrackingATC2
#
# Used by:
# Ship: Adrestia
effectType = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Hybrid Turret"),
                                  "trackingSpeed", ship.getModifiedItemAttr("shipBonusATC2"))
