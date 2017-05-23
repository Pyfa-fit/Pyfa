# republicsetbonus3
#
# Used by:
# Implants named like: High grade Jackal (6 of 6)
runTime = "early"
effectType = "passive"


def handler(fit, implant, context):
    fit.appliedImplants.filteredItemMultiply(lambda target: target.item.requiresSkill("Cybernetics"),
                                             "scanLadarStrengthPercent",
                                             implant.getModifiedItemAttr("implantSetRepublicFleet"))
