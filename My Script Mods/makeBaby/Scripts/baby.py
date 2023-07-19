import sims4.commands
import services
import sims4.log
from interactions.utils.death import DeathType
from server_commands.developer_commands import CheatWoohooTuning
from server_commands.relationship_commands import RelationshipCommandTuning
from sims.pregnancy.pregnancy_enums import PregnancyOrigin
from sims4 import random
from sims4.math import MAX_UINT32, EPSILON
from sims4.tuning.tunable import TunableRange


@sims4.commands.Command('makebaby', command_type=sims4.commands.CommandType.Live)
def make_baby(first_name: str = None, last_name: str = None, _connection=None):
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
            selected_sim.relationship_tracker.add_relationship_score(target_sim.id, 100,
                                                                     CheatWoohooTuning.CHEAT_WOOHOO_TRACK)
            selected_sim.relationship_tracker.add_relationship_score(target_sim.id, 100,
                                                                     CheatWoohooTuning.CHEAT_WOOHOO_SOCIALCONTEXT)
            tracker = selected_sim.get_tracker(CheatWoohooTuning.CHEAT_WOOHOO_COMMODITY)
            tracker.set_value(CheatWoohooTuning.CHEAT_WOOHOO_COMMODITY, 100)
            tracker = target_sim.get_tracker(CheatWoohooTuning.CHEAT_WOOHOO_COMMODITY)
            tracker.set_value(CheatWoohooTuning.CHEAT_WOOHOO_COMMODITY, 100)
            selected_sim.relationship_tracker.add_relationship_score(target_sim.id,
                                                                     100,
                                                                     RelationshipCommandTuning.INTRODUCE_TRACK)
            selected_sim.relationship_tracker.add_relationship_bit(target_sim.id,
                                                                   RelationshipCommandTuning.INTRODUCE_BIT)
            visible_only  = True
            single_sim_is_allowed = True
            selected_sim.commodity_tracker.set_all_commodities_to_best_value(visible_only=visible_only)
            pregnancy_tracker = selected_sim.pregnancy_tracker
            #add a line to shorten the time of pregnancy

            pregnancy_tracker.set_pregnancy_duration(1)
            pregnancy_tracker.start_pregnancy(selected_sim, target_sim, single_sim_is_allowed=single_sim_is_allowed)

            selected_sim.pregnancy_progress = 1


            return True  # Return True to indicate successful execution

    # If no valid first name or last name is provided or the Sim is not found
    output('Sim not found or invalid names provided.')

    return False  # Return False if the command fails
