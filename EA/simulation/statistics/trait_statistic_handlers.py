from gsi_handlers.sim_handlers import _get_sim_info_by_id
@GsiHandler('trait_statistic_view', trait_statistics_schema)
def generate_trait_statistic_view_data(sim_id:int=None):
    trait_statistic_data = []
    cur_sim_info = _get_sim_info_by_id(sim_id)
    if cur_sim_info is not None:
        trait_statistic_tracker = cur_sim_info.trait_statistic_tracker
        if trait_statistic_tracker is not None:
            for statistic in list(trait_statistic_tracker):
                entry = {'trait_statistic_name': type(statistic).__name__, 'trait_statistic_value': statistic.get_value(), 'trait_statistic_min_daily_cap': statistic._get_minimum_decay_level(), 'trait_statistic_max_daily_cap': statistic._get_maximum_decay_level(), 'trait_statistic_state': str(statistic.state), 'trait_statistic_group_limited': str(statistic.group_limited)}
                trait_statistic_data.append(entry)
    return trait_statistic_data
