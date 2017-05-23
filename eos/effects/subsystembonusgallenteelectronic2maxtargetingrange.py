# subsystemBonusGallenteElectronic2MaxTargetingRange
#
# Used by:
# Subsystem: Proteus Electronics - Dissolution Sequencer
effectType = "passive"


def handler(fit, module, context):
    fit.ship.boostItemAttr("maxTargetRange", module.getModifiedItemAttr("subsystemBonusGallenteElectronic2"),
                           skill="Gallente Electronic Systems")
