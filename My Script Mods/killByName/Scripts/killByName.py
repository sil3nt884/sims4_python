import sims4.commands
import services
import sims4.log
from event_testing import test_events
from interactions.utils.death import DeathType, DeathTracker


@sims4.commands.Command('namekill', command_type=sims4.commands.CommandType.Live)
def kill_sim_name(first_name: str = None, last_name: str = None, _connection=None):
    output = sims4.commands.CheatOutput(_connection)
    output('Name of the selected Sim: {} {}'.format(first_name, last_name))

    # Check if both first name and last name are provided
    if first_name and last_name:
        target_sim = None
        sim_info_manager = services.sim_info_manager()
        for target_sim_info in sim_info_manager.get_all():
            if (target_sim_info.first_name.lower() == first_name.lower() and
                    target_sim_info.last_name.lower() == last_name.lower()):
                target_sim = target_sim_info
                break

        if target_sim:
            output('Target found for {} {}'.format(first_name, last_name))
            death_type = DeathType.get_random_death_type()
            target_sim.add_buff(DeathTracker.IS_DYING_BUFF)
            target_sim.death_tracker.set_death_type(death_type, is_off_lot_death=True)
            return True  # Return True to indicate successful execution

    # If no valid first name or last name is provided or the Sim is not found
    output('Sim not found or invalid names provided.')

    return False  # Return False if the command fails
