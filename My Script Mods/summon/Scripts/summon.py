import sims4.commands
import services
from sims4.commands import Output
#summon_grim_reaper using the commmand summon_grim_reaper
@sims4.commands.Command('killAll', command_type=sims4.commands.CommandType.Live)
def summon_grim_reaper(_connection=None):
    output = Output(_connection)

    client = services.client_manager().get_first_client()
    active_sim = client.active_sim

    # Check if the Grim Reaper is already present in the current lot
    if services.get_zone_situation_manager().has_situation('S4CL_GrimReaperSituation'):
        output('Grim Reaper is already present.')
        return False

    if active_sim is not None:
        # Summon the Grim Reaper
        services.get_zone_situation_manager().add_new_situation('S4CL_GrimReaperSituation', active_sim)

        output('Summoned the Grim Reaper.')
        return True  # Return True to indicate successful execution

    # If no active Sim is found
    output('No active Sim found.')

    return False  # Return False if the command fails
