import sims4.commands
import services
import sims4.log
from interactions.utils.death import DeathType, DeathTracker
#
#     BABY = 1
#     TODDLER = 2
#     CHILD = 4
#     TEEN = 8
#     YOUNGADULT = 16
#     ADULT = 32
#     ELDER = 64
#     INFANT = 128


@sims4.commands.Command('age', command_type=sims4.commands.CommandType.Live)
def age_sim_name(first_name: str = None, last_name: str = None, _connection=None):
    output = sims4.commands.CheatOutput(_connection)
    output('Name of the selected Sim: {} {}'.format(first_name, last_name))
    sim_info_manager = services.sim_info_manager()


    # Check if both first name and last name are provided
    if first_name and last_name:
        target_sim = None
        for target_sim_info in sim_info_manager.get_all():
            if (target_sim_info.first_name.lower() == first_name.lower() and
                    target_sim_info.last_name.lower() == last_name.lower()):
                target_sim = target_sim_info
                break

        if target_sim:
            output('Target found for {} {}'.format(first_name, last_name))
            target_sim.callback_auto_age()
            return True  # Return True to indicate successful execution

    # If no valid first name or last name is provided or the Sim is not found
    output('Sim not found or invalid names provided.')

    return False  # Return False if the command fails
