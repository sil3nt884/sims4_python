from sims4.gsi.dispatcher import GsiHandler
    cheat.add_token_param('whim')
    cheat.add_token_param('sim_id')
@GsiHandler('sim_whim_view', sim_whim_schema)
def generate_sim_whim_view_data(sim_id:int=None):
    whim_view_data = []
    sim_info_manager = services.sim_info_manager()
    if sim_info_manager is not None:
        for sim_info in sim_info_manager.objects:
            if sim_info.sim_id == sim_id:
                whim_tracker = sim_info._whim_tracker
                if whim_tracker is None:
                    pass
                else:
                    for whim_slot in whim_tracker.slots_gen():
                        whim_view_data.append(whim_slot.get_gsi_data())
    return whim_view_data

    cheat.add_token_param('whimset')
    cheat.add_token_param('sim_id')
    sub_schema.add_field('whim', label='Whim', width=3)
    sub_schema.add_field('status', label='Status', width=5)
    sub_schema.add_field('weight', label='Weight', width=1, type=GsiFieldVisualizers.FLOAT)
    sub_schema.add_field('whim_type', label='Type', width=3)
@GsiHandler('sim_activeset_view', sim_activeset_schema)
def generate_sim_activeset_view_data(sim_id:int=None):
    activeset_view_data = []
    sim_info_manager = services.sim_info_manager()
    if sim_info_manager is not None:
        for sim_info in sim_info_manager.objects:
            if sim_info.sim_id == sim_id:
                whim_tracker = sim_info._whim_tracker
                if whim_tracker is None:
                    pass
                else:
                    active_sets = whim_tracker.get_active_whimset_data()
                    for (whimset, whimset_data) in active_sets.items():
                        set_data = {'sim_id': str(sim_info.sim_id), 'whimset': whimset.__name__, 'priority': whim_tracker.get_priority(whimset), 'targets': str(whimset_data.targets)}
                        sub_data = []
                        for weighted_whim in whimset.whims:
                            whim = weighted_whim.whim
                            test_result = 'Not Chosen'
                            if whim.goal in whim_tracker._test_results_map:
                                test_result = whim_tracker._test_results_map[whim.goal]
                            whim_data = {'whim': whim.goal.__name__, 'status': test_result, 'weight': weighted_whim.weight, 'whim_type': str(whim.type)}
                            sub_data.append(whim_data)
                        set_data['potential_whims_view'] = sub_data
                        activeset_view_data.append(set_data)
    return activeset_view_data

    cheat.add_token_param('whimset')
    cheat.add_token_param('simId')
@GsiHandler('sim_whimset_view', sim_whimset_schema)
def generate_sim_whimset_view_data(sim_id:int=None):
    whimset_view_data = []
    sim_info_manager = services.sim_info_manager()
    if sim_info_manager is not None:
        sim_info = sim_info_manager.get(sim_id)
        if sim_info is not None:
            whim_tracker = sim_info._whim_tracker
            if whim_tracker is None:
                return whimset_view_data
            else:
                whim_set_list = []
                for whim_set in services.get_instance_manager(sims4.resources.Types.ASPIRATION).all_whim_sets_gen():
                    priority = whim_tracker.get_priority(whim_set)
                    whim_set_list.append((priority, whim_set))
                    whim_set_list = sorted(whim_set_list, key=lambda whim_set: whim_set[0])
                    whim_set_list.reverse()
                if whim_set_list is not None:
                    for whim_set_data in whim_set_list:
                        whim_set = whim_set_data[1]
                        whims_in_set_str = ', '.join(weighted_whim.whim.goal.__name__ for weighted_whim in whim_set.whims)
                        whim_set_entry = {'simId': str(sim_id), 'whimset': whim_set.__name__, 'priority': whim_tracker.get_priority(whim_set), 'target': str(whim_tracker.get_whimset_target(whim_set)), 'active_priority': getattr(whim_set, 'activated_priority', None), 'chained_priority': getattr(whim_set, 'chained_priority', None), 'whims_in_set': whims_in_set_str}
                        whimset_view_data.append(whim_set_entry)
                return whimset_view_data
