# subsystemBonusMinmatarPropulsionAgility
#
# Used by:
# Subsystem: Loki Propulsion - Intercalated Nanofibers
# Subsystem: Loki Propulsion - Interdiction Nullifier
effectType = "passive"


def handler(fit, module, context):
    fit.ship.boostItemAttr("agility", module.getModifiedItemAttr("subsystemBonusMinmatarPropulsion"),
                           skill="Minmatar Propulsion Systems")
