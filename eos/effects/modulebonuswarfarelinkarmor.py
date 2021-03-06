# moduleBonusWarfareLinkArmor
#
# Used by:
# Variations of module: Armor Command Burst I (2 of 2)

"""
Some documentation:
When the fit is calculated, we gather up all the gang effects and stick them onto the fit. We don't run the actual
effect yet, only give the fit details so that it can run the effect at a later time. We need to do this so that we can
only run the strongest effect. When we are done, one of the last things that we do with the fit is to loop through those
bonuses and actually run the effect. To do this, we have a special argument passed into the effect handler that tells it
which warfareBuffID to run (shouldn't need this right now, but better safe than sorry)
"""

effectType = "active", "gang"


def handler(fit, container, context, **kwargs):
    for x in xrange(1, 5):
        if container.getModifiedChargeAttr("warfareBuff{}ID".format(x)):
            value = container.getModifiedItemAttr("warfareBuff{}Value".format(x))
            container_id = container.getModifiedChargeAttr("warfareBuff{}ID".format(x))

            if container_id:
                fit.addCommandBonus(container_id, value, container, kwargs['effect'])
