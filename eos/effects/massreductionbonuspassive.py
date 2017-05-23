# massReductionBonusPassive
#
# Used by:
# Modules from group: Rig Anchor (4 of 4)
effectType = "passive"


def handler(fit, module, context):
    fit.ship.boostItemAttr("mass", module.getModifiedItemAttr("massBonusPercentage"), stackingPenalties=True)
