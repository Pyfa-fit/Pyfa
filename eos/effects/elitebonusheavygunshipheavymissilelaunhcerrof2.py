# eliteBonusHeavyGunshipHeavyMissileLaunhcerRof2
#
# Used by:
# Ship: Cerberus
effectType = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Missile Launcher Heavy",
                                  "speed", ship.getModifiedItemAttr("eliteBonusHeavyGunship2"),
                                  skill="Heavy Assault Cruisers")
