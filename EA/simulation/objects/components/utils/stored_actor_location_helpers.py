import routing
class GoToStoredLocationSuperInteraction(SitOrStandSuperInteraction, HasTunableFactory):
    INSTANCE_TUNABLES = {'basic_content': TunableBasicContentSet(no_content=True, default='no_content')}

    @classmethod
    def _test(cls, target, context, slot=None, **kwargs):
        if target is None:
            return TestResult(False, 'Target is None and cannot be.')
        stored_actor_location_component = target.get_component(types.STORED_ACTOR_LOCATION_COMPONENT)
        if stored_actor_location_component is None:
            return TestResult(False, 'Attempting to test routability against a location stored on an object {} without the Stored Actor Location Component.')
        location = stored_actor_location_component.get_stored_location()
        if location is None:
            return TestResult(False, 'Stored Actor Location Component does not have a stored location.')
        lot = services.active_lot()
        position = location.translation
        if not lot.is_position_on_lot(position):
            return TestResult(False, 'Stored location is not on the active lot.', tooltip=StoredActorLocationTuning.UNROUTABLE_MESSAGE_OFF_LOT)
        routing_location = routing.Location(position, location.orientation, location.routing_surface)
        if not routing.test_connectivity_pt_pt(context.sim.routing_location, routing_location, context.sim.routing_context):
            return TestResult(False, 'Stored location is not routable.', tooltip=StoredActorLocationTuning.UNROUTABLE_MESSAGE_NOT_CONNECTED)
        return TestResult.TRUE
