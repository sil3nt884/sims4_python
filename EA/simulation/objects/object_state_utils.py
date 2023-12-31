from build_buy import get_room_idfrom event_testing.resolver import SingleObjectResolverfrom event_testing.tests import TunableTestSetfrom objects.components.state_references import TunableStateValueReferencefrom sims4.tuning.tunable import AutoFactoryInit, HasTunableSingletonFactory, TunableVariantfrom tag import TunableTagsimport servicesimport sims4logger = sims4.log.Logger('ObjectStateUtils', default_owner='mkartika')
def all_objects_gen(objects):
    plex_service = services.get_plex_service()
    for obj in objects:
        if not plex_service.is_active_zone_a_plex() or plex_service.get_plex_zone_at_position(obj.position, obj.level) is None:
            pass
        else:
            yield obj

def objects_in_target_room_gen(target, objects):
    target_room_id = get_room_id(target.zone_id, target.position, target.level)
    for obj in objects:
        obj_room_id = get_room_id(obj.zone_id, obj.position, obj.level)
        if obj_room_id != target_room_id:
            pass
        else:
            yield obj

class _ObjectTargetAll(HasTunableSingletonFactory):

    def get_object_target_gen(self, _, objects):
        yield from all_objects_gen(objects)

class _ObjectTargetRoom(HasTunableSingletonFactory):

    def get_object_target_gen(self, target, objects):
        if target is None:
            logger.error('Trying to find an object in room but got a None target.', owner='trevor')
            yield None
            return
        yield from objects_in_target_room_gen(target, objects)

class TunableObjectTargetVariant(TunableVariant):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, all_objects=_ObjectTargetAll.TunableFactory(), room_objects=_ObjectTargetRoom.TunableFactory(), default='room_objects', **kwargs)

class ObjectStateHelper(AutoFactoryInit, HasTunableSingletonFactory):
    FACTORY_TUNABLES = {'object_target': TunableObjectTargetVariant(description='\n            Define the set of objects that this interaction is applied to.\n            '), 'object_tags': TunableTags(description='\n            Find all of the objects based on these tags.\n            ', filter_prefixes=('func',)), 'desired_state': TunableStateValueReference(description='\n            State that will be set to the objects.\n            ', pack_safe=True), 'tests': TunableTestSet(description="\n            If pass these tests, the object's state will be changed to\n            Desired State.\n            ")}

    def execute_helper(self, target=None):
        if self.desired_state is not None:
            objects = list(services.object_manager().get_objects_with_tags_gen(*self.object_tags))
            for obj in self.object_target.get_object_target_gen(target, objects):
                resolver = SingleObjectResolver(obj)
                if self.tests.run_tests(resolver):
                    obj.set_state(self.desired_state.state, self.desired_state)
