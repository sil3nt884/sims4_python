from gsi_handlers.gameplay_archiver import GameplayArchiver
def is_archive_enabled():
    return archiver.enabled

def archive_removed_statistic(statistic, owner):
    archive_data = {'statistic': statistic, 'owner': owner}
    archiver.archive(archive_data)

def dump_to_csv(connection=None):
    archiver.dump_to_csv('removed_statistics', connection)
