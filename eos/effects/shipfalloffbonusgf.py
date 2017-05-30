# shipFalloffBonusGF
#
# Used by:
# Ship: Atron
# Ship: Daredevil
effectType = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Hybrid Turret"),
                                  "falloff", ship.getModifiedItemAttr("shipBonusGF2"), skill="Gallente Frigate")
