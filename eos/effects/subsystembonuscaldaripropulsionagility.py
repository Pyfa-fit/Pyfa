# subsystemBonusCaldariPropulsionAgility
#
# Used by:
# Subsystem: Tengu Propulsion - Intercalated Nanofibers
# Subsystem: Tengu Propulsion - Interdiction Nullifier
effectType = "passive"


def handler(fit, module, context):
    fit.ship.boostItemAttr("agility", module.getModifiedItemAttr("subsystemBonusCaldariPropulsion"),
                           skill="Caldari Propulsion Systems")
