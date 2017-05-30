# shipHeatDamageMinmatarTacticalDestroyer3
#
# Used by:
# Ship: Svipul
effectType = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: True, "heatDamage",
                                  ship.getModifiedItemAttr("shipBonusTacticalDestroyerMinmatar3"),
                                  skill="Minmatar Tactical Destroyer")
