# remoteWebifierEntity
#
# Used by:
# Drones from group: Stasis Webifying Drone (3 of 3)
effectType = "active", "projected"


def handler(fit, container, context, *args, **kwargs):
    if "projected" not in context:
        return
    fit.ship.boostItemAttr("maxVelocity", container.getModifiedItemAttr("speedFactor"),
                           stackingPenalties=True, *args, **kwargs)
