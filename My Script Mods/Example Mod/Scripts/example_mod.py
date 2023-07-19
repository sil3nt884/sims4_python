import sims4.commands
import services
import sims4.log
from interactions.utils.death import DeathType, DeathTracker


@sims4.commands.Command('kill', command_type=sims4.commands.CommandType.Live)
def get_selected_sim_name(_connection=None):
    # Get the first active client
    client = services.client_manager().get_first_client()
    selected_sim = client.active_sim_info
    selected_sim.add_buff(DeathTracker.IS_DYING_BUFF)
    death_type = DeathType.get_random_death_type()
    selected_sim.death_tracker.set_death_type(death_type, is_off_lot_death=True)

    output = sims4.commands.CheatOutput(_connection)
    output('Name of the selected Sim: {}'.format( selected_sim))

