# eliteBonusMaraudersCruiseAndTorpedoDamageRole1
#
# Used by:
# Ship: Golem
effectType = "passive"


def handler(fit, ship, context):
    damageTypes = ("em", "explosive", "kinetic", "thermal")
    for damageType in damageTypes:
        fit.modules.filteredChargeBoost(
                lambda mod: mod.charge.requiresSkill("Cruise Missiles") or mod.charge.requiresSkill("Torpedoes"),
                "{0}Damage".format(damageType), ship.getModifiedItemAttr("eliteBonusViolatorsRole1"))
