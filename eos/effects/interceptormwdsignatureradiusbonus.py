# interceptorMWDSignatureRadiusBonus
#
# Used by:
# Ships from group: Interceptor (10 of 10)
effectType = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("High Speed Maneuvering"),
                                  "signatureRadiusBonus", ship.getModifiedItemAttr("eliteBonusInterceptor"),
                                  skill="Interceptors")
