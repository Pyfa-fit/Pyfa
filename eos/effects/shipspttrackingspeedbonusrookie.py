# shipSPTTrackingSpeedBonusRookie
#
# Used by:
# Ship: Echo
effectType = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Projectile Turret"),
                                  "trackingSpeed", ship.getModifiedItemAttr("rookieSPTTracking"))
