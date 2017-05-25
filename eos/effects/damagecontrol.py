# damageControl
#
# Used by:
# Variations of module: Damage Control I (16 of 16)
# Module: Civilian Damage Control
effectType = "passive"


def handler(fit, container, context):
    for layer, attrPrefix in (('shield', 'shield'), ('armor', 'armor'), ('hull', '')):
        for damageType in ('Kinetic', 'Thermal', 'Explosive', 'Em'):
            bonus = "%s%sDamageResonance" % (attrPrefix, damageType)
            bonus = "%s%s" % (bonus[0].lower(), bonus[1:])
            booster = "%s%sDamageResonance" % (layer, damageType)
            penalize = False if layer == 'hull' else True
            fit.ship.multiplyItemAttr(bonus, container.getModifiedItemAttr(booster),
                                      stackingPenalties=penalize, penaltyGroup="preMul")
