# setBonusSansha
#
# Used by:
# Implants named like: grade Slave (18 of 18)
# Implant: High-grade Halo Omega
runTime = "early"
effectType = "passive"


def handler(fit, implant, context):
    fit.appliedImplants.filteredItemMultiply(lambda target: target.item.requiresSkill("Cybernetics"),
                                             "armorHpBonus", implant.getModifiedItemAttr("implantSetSansha") or 1)
