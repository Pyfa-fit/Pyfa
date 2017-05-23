# Interceptor2WarpScrambleRange
#
# Used by:
# Ships from group: Interceptor (6 of 10)
effectType = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Warp Scrambler",
                                  "maxRange", ship.getModifiedItemAttr("eliteBonusInterceptor2"), skill="Interceptors")
