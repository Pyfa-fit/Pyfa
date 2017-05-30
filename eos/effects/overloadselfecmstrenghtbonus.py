# overloadSelfECMStrenghtBonus
#
# Used by:
# Modules from group: Burst Jammer (11 of 11)
# Modules from group: ECM (39 of 39)
effectType = "overheat"


def handler(fit, container, context):
    if "projected" not in context:
        for scanType in ("Gravimetric", "Magnetometric", "Radar", "Ladar"):
            container.boostItemAttr("scan{0}StrengthBonus".format(scanType),
                                    container.getModifiedItemAttr("overloadECMStrengthBonus"),
                                    stackingPenalties=True)
