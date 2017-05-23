# shipPTspeedBonusMB2
#
# Used by:
# Variations of ship: Tempest (4 of 4)
# Ship: Maelstrom
# Ship: Panther
# Ship: Typhoon Fleet Issue
effectType = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Projectile Turret"),
                                  "speed", ship.getModifiedItemAttr("shipBonusMB2"), skill="Minmatar Battleship")
