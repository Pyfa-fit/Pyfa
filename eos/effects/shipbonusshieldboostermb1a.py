# shipBonusShieldBoosterMB1a
#
# Used by:
# Ship: Maelstrom
effectType = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Operation"),
                                  "shieldBonus", ship.getModifiedItemAttr("shipBonusMB"), skill="Minmatar Battleship")
