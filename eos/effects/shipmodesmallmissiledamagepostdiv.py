# shipModeSmallMissileDamagePostDiv
#
# Used by:
# Module: Jackdaw Sharpshooter Mode
effectType = "passive"


def handler(fit, container, context):
    types = ("thermal", "em", "explosive", "kinetic")
    for damage_type in types:
        fit.modules.filteredChargeMultiply(lambda mod: mod.charge.requiresSkill("Rockets") or mod.charge.requiresSkill("Light Missiles"),
                                           "{}Damage".format(damage_type),
                                           1 / container.getModifiedItemAttr("modeDamageBonusPostDiv"),
                                           stackingPenalties=True,
                                           penaltyGroup="postDiv")
