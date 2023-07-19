import sims4.commands
import services
import sims4.log
from interactions.utils.death import DeathType
from sims.fixup.sim_info_fixup_action import SimInfoFixupActionTiming
from sims.household_enums import HouseholdChangeOrigin


@sims4.commands.Command('namehousehold', command_type=sims4.commands.CommandType.Live)
def kill_sim_name(first_name: str = None, last_name: str = None, _connection=None):
    output = sims4.commands.CheatOutput(_connection)
    output('Name of the selected Sim: {} {}'.format(first_name, last_name))
    client = services.client_manager().get_first_client()
    selected_sim = client.active_sim_info


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
            selected_sim.household.add_sim_info_to_household(target_sim)
            client.add_selectable_sim_info(target_sim)
            target_sim.apply_fixup_actions(SimInfoFixupActionTiming.ON_ADDED_TO_ACTIVE_HOUSEHOLD)


    # If no valid first name or last name is provided or the Sim is not found
    output('Sim not found or invalid names provided.')

    return False  # Return False if the command fails
