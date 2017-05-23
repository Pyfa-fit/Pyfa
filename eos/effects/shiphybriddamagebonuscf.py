# shipHybridDamageBonusCF
#
# Used by:
# Ship: Raptor
effectType = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Hybrid Turret"),
                                  "damageMultiplier", ship.getModifiedItemAttr("shipBonusCF"), skill="Caldari Frigate")
