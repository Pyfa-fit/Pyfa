# drawbackMaxVelocity
#
# Used by:
# Modules from group: Rig Armor (48 of 72)
# Modules from group: Rig Resource Processing (8 of 10)
effectType = "passive"


def handler(fit, container, context):
    fit.ship.boostItemAttr("maxVelocity", container.getModifiedItemAttr("drawback"),
                           stackingPenalties=True)
