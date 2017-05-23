# subsystemBonusAmarrPropulsionAgility
#
# Used by:
# Subsystem: Legion Propulsion - Interdiction Nullifier
effectType = "passive"


def handler(fit, module, context):
    fit.ship.boostItemAttr("agility", module.getModifiedItemAttr("subsystemBonusAmarrPropulsion"),
                           skill="Amarr Propulsion Systems")
