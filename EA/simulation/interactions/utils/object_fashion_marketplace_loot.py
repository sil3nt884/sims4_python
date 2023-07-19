from interactions.utils.loot_basic_op import BaseLootOperation, BaseTargetedLootOperation
class ListOnMarketplace(HasTunableSingletonFactory, AutoFactoryInit):

    def __call__(self, seller, obj):
        if not obj.has_component(OBJECT_FASHION_MARKETPLACE_COMPONENT):
            obj.add_dynamic_component(OBJECT_FASHION_MARKETPLACE_COMPONENT, list_cost_multiplier=None, sale_price_multiplier=None, sale_chance_multplier=None)
        obj.list(seller)

class DelistOnMarketplace(HasTunableSingletonFactory, AutoFactoryInit):

    def __call__(self, seller, obj):
        if not obj.has_component(OBJECT_FASHION_MARKETPLACE_COMPONENT):
            return
        fashion_marketplace_component = obj.get_component(OBJECT_FASHION_MARKETPLACE_COMPONENT)
        if fashion_marketplace_component.is_listed() or not fashion_marketplace_component.is_pending_sale():
            return
        obj.delist()

class SellOnMarketplace(HasTunableSingletonFactory, AutoFactoryInit):

    def __call__(self, owner, obj):
        if not obj.has_component(OBJECT_FASHION_MARKETPLACE_COMPONENT):
            logger.error('Attempting to sell an object {} that is not listed on fashion marketplace', obj)
            return
        obj.sell()

class ObjectFashionMarketplaceLootOp(BaseTargetedLootOperation):
    FACTORY_TUNABLES = {'marketplace_operation': TunableVariant(description='\n            The marketplace operation to perform.\n            ', list=ListOnMarketplace.TunableFactory(), delist=DelistOnMarketplace.TunableFactory(), sell=SellOnMarketplace.TunableFactory(), default='list')}

    def __init__(self, marketplace_operation, **kwargs):
        super().__init__(**kwargs)
        self.marketplace_operation = marketplace_operation

    def _apply_to_subject_and_target(self, subject, target, resolver):
        self.marketplace_operation(subject, target)
        return True
