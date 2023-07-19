from services import get_instance_manager
class TunableStateValueReference(TunableReference):

    def __init__(self, class_restrictions=DEFAULT, **kwargs):
        if class_restrictions is DEFAULT:
            class_restrictions = 'ObjectStateValue'
        super().__init__(manager=get_instance_manager(Types.OBJECT_STATE), class_restrictions=class_restrictions, **kwargs)

class TunablePackSafeStateValueReference(TunablePackSafeReference):

    def __init__(self, class_restrictions=DEFAULT, **kwargs):
        if class_restrictions is DEFAULT:
            class_restrictions = 'ObjectStateValue'
        super().__init__(manager=get_instance_manager(Types.OBJECT_STATE), class_restrictions=class_restrictions, **kwargs)

class TunableStateTypeReference(TunableReference):

    def __init__(self, class_restrictions=DEFAULT, **kwargs):
        if class_restrictions is DEFAULT:
            class_restrictions = 'ObjectState'
        super().__init__(manager=get_instance_manager(Types.OBJECT_STATE), class_restrictions=class_restrictions, **kwargs)
