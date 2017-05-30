# shipBonusCarrierRole1NumWarfareLinks
#
# Used by:
# Ships from group: Carrier (4 of 4)
effectType = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemIncrease(lambda mod: mod.item.requiresSkill("Leadership"), "maxGroupActive",
                                     src.getModifiedItemAttr("shipBonusRole1"))
