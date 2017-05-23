# scriptResistanceBonusBonus
#
# Used by:
# Charges named like: Resistance Script (8 of 8)
effectType = "passive"


def handler(fit, src, context):
    src.boostItemAttr("emDamageResistanceBonus", src.getModifiedChargeAttr("emDamageResistanceBonusBonus"))
    src.boostItemAttr("explosiveDamageResistanceBonus",
                      src.getModifiedChargeAttr("explosiveDamageResistanceBonusBonus"))
    src.boostItemAttr("kineticDamageResistanceBonus", src.getModifiedChargeAttr("kineticDamageResistanceBonusBonus"))
    src.boostItemAttr("thermalDamageResistanceBonus", src.getModifiedChargeAttr("thermalDamageResistanceBonusBonus"))
