from gsi_handlers.gameplay_archiver import GameplayArchiver
def archive_gsi_dump(filename_str, error_str):
    callstack = generate_message_with_callstack('GSI Dump')
    archive_data = {'game_time': str(services.time_service().sim_now), 'gsi_filename': filename_str, 'error_log_or_exception': error_str, 'callstack': callstack}
    gsi_dump_archiver.archive(data=archive_data)
