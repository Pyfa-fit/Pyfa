# Not used by any item
"""
Since fighter abilities do not have any sort of item entity in the EVE database, we must derive the abilities from the
effects, and thus this effect file contains some custom information useful only to fighters.
"""
# User-friendly name for the ability
displayName = "Bomb"

# Attribute prefix that this ability targets
prefix = "fighterAbilityLaunchBomb"

effectType = "active"

# This flag is required for effects that use charges in order to properly calculate reload time
hasCharges = True


def handler(fit, src, context):
    pass
