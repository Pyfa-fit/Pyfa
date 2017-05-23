# shipBonusAfterburnerSpeedFactor2CB
#
# Used by:
# Ship: Nightmare
effectType = "passive"


def handler(fit, module, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Afterburner"),
                                  "speedFactor", module.getModifiedItemAttr("shipBonus2CB"), skill="Caldari Battleship")
