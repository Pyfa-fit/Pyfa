# caldarisetLGbonus
#
# Used by:
# Implants named like: Low grade Talon (6 of 6)
runTime = "early"
effectType = "passive"


def handler(fit, implant, context):
    fit.appliedImplants.filteredItemMultiply(lambda target: target.item.requiresSkill("Cybernetics"),
                                             "scanGravimetricStrengthModifier",
                                             implant.getModifiedItemAttr("implantSetLGCaldariNavy"))
