# subsystemBonusGallentePropulsionAgility
#
# Used by:
# Subsystem: Proteus Propulsion - Interdiction Nullifier
effectType = "passive"


def handler(fit, module, context):
    fit.ship.boostItemAttr("agility", module.getModifiedItemAttr("subsystemBonusGallentePropulsion"),
                           skill="Gallente Propulsion Systems")
