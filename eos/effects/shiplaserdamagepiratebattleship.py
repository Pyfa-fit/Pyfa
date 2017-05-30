# shipLaserDamagePirateBattleship
#
# Used by:
# Ship: Bhaalgorn
# Ship: Nightmare
effectType = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Energy Turret"),
                                  "damageMultiplier", ship.getModifiedItemAttr("shipBonusRole7"))
