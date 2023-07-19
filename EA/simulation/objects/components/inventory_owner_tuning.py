from objects.components.state_references import TunableStateValueReference
class InventoryTuning:
    INVALID_ACCESS_STATES = TunableList(TunableStateValueReference(description='\n        If an inventory owner is in any of the states tuned here, it will not\n        be available to grab objects out of.\n        ', pack_safe=True))
