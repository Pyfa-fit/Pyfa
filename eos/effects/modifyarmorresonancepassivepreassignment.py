# modifyArmorResonancePassivePreAssignment
#
# Used by:
# Subsystems from group: Defensive Systems (16 of 16)
effectType = "passive"


def handler(fit, container, context):
    for resist_type in ("Em", "Explosive", "Kinetic", "Thermal"):
        fit.ship.preAssignItemAttr("armor{0}DamageResonance".format(resist_type),
                                   container.getModifiedItemAttr("passiveArmor{0}DamageResonance".format(resist_type)))
