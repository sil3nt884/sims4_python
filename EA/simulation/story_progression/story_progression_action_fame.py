from collections import Counter
class StoryProgressionActionFame(_StoryProgressionAction):
    FACTORY_TUNABLES = {'time_of_day': TunableTuple(description='\n            Only run this action when it is between a certain time of day.\n            ', start_time=TunableTimeOfDay(default_hour=2), end_time=TunableTimeOfDay(default_hour=6))}

    def should_process(self, options):
        current_time = services.time_service().sim_now
        if not current_time.time_between_day_times(self.time_of_day.start_time, self.time_of_day.end_time):
            return False
        return True

    def process_action(self, story_progression_flags):
        if FameTunables.FAME_RANKED_STATISTIC is None:
            return
        played_famous = 0
        non_played_famous = 0
        non_played_fame_level = Counter()
        for sim_info in services.sim_info_manager().get_all():
            if sim_info.lod == SimInfoLODLevel.MINIMUM:
                pass
            else:
                fame_stat = sim_info.get_statistic(FameTunables.FAME_RANKED_STATISTIC, add=False)
                if not fame_stat:
                    pass
                elif fame_stat.rank_level >= 1:
                    if sim_info.is_player_sim:
                        played_famous += 1
                    else:
                        non_played_famous += 1
                        non_played_fame_level[fame_stat.rank_level] += 1
        with telemetry_helper.begin_hook(fame_telemetry_writer, TELEMETRY_HOOK_FAME) as hook:
            hook.write_int(TELEMETRY_FIELD_FAME_PLAYED, played_famous)
            hook.write_int(TELEMETRY_FIELD_FAME_NON_PLAYED, non_played_famous)
            hook.write_int(TELEMETRY_FIELD_FAME_ONE_STAR_NON_PLAYED, non_played_fame_level[1])
            hook.write_int(TELEMETRY_FIELD_FAME_TWO_STAR_NON_PLAYED, non_played_fame_level[2])
            hook.write_int(TELEMETRY_FIELD_FAME_THREE_STAR_NON_PLAYED, non_played_fame_level[3])
            hook.write_int(TELEMETRY_FIELD_FAME_FOUR_STAR_NON_PLAYED, non_played_fame_level[4])
            hook.write_int(TELEMETRY_FIELD_FAME_FIVE_STAR_NON_PLAYED, non_played_fame_level[5])
