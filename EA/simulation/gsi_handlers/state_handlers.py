from gsi_handlers.gameplay_archiver import GameplayArchiver
def archive_state_trigger(obj, triggered_state, at_state, at_states, source=''):
    archive_data = {'objId': hex(obj.id), 'def': obj.definition.name, 'state': str(triggered_state.state), 'state_value': str(triggered_state), 'at_state': str(at_state), 'at_states': str(at_states), 'src': source}
    if obj.parent is not None:
        archive_data['parent'] = gsi_handlers.gsi_utils.format_object_name(obj.parent)
    state_trigger_archiver.archive(data=archive_data)

def archive_timed_state_trigger(obj, triggered_state, at_state, trigger_time):
    archive_data = {'objId': hex(obj.id), 'def': obj.definition.name, 'state': str(triggered_state.state), 'state_value': str(triggered_state), 'at_state': str(at_state), 'trigger_time': round(trigger_time, 2)}
    timed_state_trigger_archiver.archive(data=archive_data)
