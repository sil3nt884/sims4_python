from gsi_handlers.gameplay_archiver import GameplayArchiver
def archive_sim_spawner_service_log_entry(action, sim_info, reason, priority, position):
    entry = {'action': action, 'sim': str(sim_info), 'reason': str(reason), 'priority': str(priority), 'position': str(position), 'sim_time': str(services.time_service().sim_now)}
    sim_spawner_service_log_archiver.archive(data=entry)
