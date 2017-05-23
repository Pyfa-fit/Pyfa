# shipHeavyAssaultMissileAOECloudSizeCC2
#
# Used by:
# Ship: Caracal Navy Issue
effectType = "passive"


def handler(fit, ship, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Assault Missiles"),
                                    "aoeCloudSize", ship.getModifiedItemAttr("shipBonusCC2"), skill="Caldari Cruiser")
