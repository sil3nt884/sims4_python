from sims4.gsi.dispatcher import GsiHandler
@GsiHandler('sim_spawner_service_queue', sim_spawner_service_queue_schema)
def generate_sim_spawner_service_queue(zone_id:int=None):
    sim_spawner_service = services.sim_spawner_service()
    if sim_spawner_service is None:
        return
    queue = sim_spawner_service.get_queue_for_gsi()
    return queue

@GsiHandler('sim_spawner_service_global', sim_spawner_service_global_schema)
def generate_sim_spawner_service_global(zone_id:int=None):
    sim_spawner_service = services.sim_spawner_service()
    if sim_spawner_service is None:
        return
    data = {'npcs_here': sim_spawner_service.number_of_npcs_instantiated, 'npcs_leaving': sim_spawner_service.number_of_npcs_leaving, 'npc_soft_cap': sim_spawner_service.npc_soft_cap, 'npc_cap_modifier': sim_spawner_service._npc_cap_modifier}
    return data
