import enum
class AdditionalBillSource(DynamicEnum):
    Miscellaneous = 0

class UtilityEndOfBillAction(enum.Int, export=False):
    SELL = 0
    STORE = 1
