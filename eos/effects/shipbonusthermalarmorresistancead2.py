# shipBonusThermalArmorResistanceAD2
#
# Used by:
# Ship: Pontifex
effectType = "passive"


def handler(fit, src, context):
    fit.ship.boostItemAttr("armorThermalDamageResonance", src.getModifiedItemAttr("shipBonusAD2"),
                           skill="Amarr Destroyer")
