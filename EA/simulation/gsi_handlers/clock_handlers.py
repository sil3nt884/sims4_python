from gsi_handlers.gameplay_archiver import GameplayArchiver
def archive_speed_change(interaction, request_type, requested_speed, is_request):
    archive_data = {'sim': str(interaction.sim), 'interaction': str(interaction), 'request_type': str(request_type), 'requested_speed': str(requested_speed), 'is_request': is_request}
    speed_change_archiver.archive(data=archive_data)
