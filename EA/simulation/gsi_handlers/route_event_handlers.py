from gsi_handlers.gameplay_archiver import GameplayArchiver
    gsi_log_id = UniqueIdGenerator()
    path_events_archive = {}
    update_log_enabled = False
class PathRouteEventsArchiveGSILog:

    def __init__(self):
        self.clear_log()

    def clear_log(self):
        self.id = gsi_log_id()
        services_time_service = services.time_service()
        if services_time_service is not None and services_time_service.sim_timeline is not None:
            self.now = str(services_time_service.sim_timeline.now)
        else:
            self.now = 'Unavailable'
        self.route_events = {}

def get_path_route_events_log(path, clear=False):
    if path.sim is not None:
        all_path_logs = setdefault_callable(path_events_archive, path.sim.id, dict)
        path_log = setdefault_callable(all_path_logs, id(path), PathRouteEventsArchiveGSILog)
        if clear:
            del path_events_archive[path.sim.id][id(path)]
        return path_log

    sub_schema.add_field('time', label='Time', type=GsiFieldVisualizers.FLOAT, width=1)
    sub_schema.add_field('status', label='Status', width=1)
    sub_schema.add_field('duration', label='Duration', type=GsiFieldVisualizers.FLOAT, width=2)
    sub_schema.add_field('event_cls', label='Event Class', width=3)
    sub_schema.add_field('event_type', label='Event Type', width=3)
    sub_schema.add_field('tag', label='Tag', type=GsiFieldVisualizers.INT, width=1)
    sub_schema.add_field('executed', label='Executed', width=1)
def gsi_fill_route_event_data(route_event, path_log, additional_data=None):
    event_dict = {'time': route_event.time, 'duration': route_event.duration, 'event_cls': str(type(route_event)), 'event_type': str(type(route_event.event_data)), 'tag': route_event.tag}
    if additional_data is not None:
        event_dict.update(additional_data)
    if route_event.id in path_log.route_events:
        path_log.route_events[route_event.id].update(event_dict)
    else:
        path_log.route_events[route_event.id] = event_dict

def archive_route_events(path, sim, archive_type, clear=False):
    path_log = get_path_route_events_log(path, clear=clear)
    if archive_type == PATH_TYPE_UPDATE and not path_log.route_events.values():
        return
    if not sim.is_sim:
        return
    archive_data = {'duration': path.duration(), 'path_id': id(path), 'master_sim': str(path.sim)}
    archive_data['path_type'] = archive_type
    archive_data['Route Events'] = tuple(path_log.route_events.values())
    archiver.archive(data=archive_data, object_id=sim.id)

def gsi_route_event_executed(path, sim, executed_event):
    path_log = get_path_route_events_log(path)
    if executed_event.id in path_log.route_events:
        path_log.route_events[executed_event.id]['executed'] = True
    else:
        logger.warn('Route Event Executed but was never logged')
