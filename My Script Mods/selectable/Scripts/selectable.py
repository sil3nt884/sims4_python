import sims4.commands
import services
import sims4.log
from interactions.utils.death import DeathType


@sims4.commands.Command('selectable', command_type=sims4.commands.CommandType.Live)
def selectable(_connection=None):
    output = sims4.commands.CheatOutput(_connection)
    services.client_manager().make_all_sims_selectable()



