import services
class _BartenderSituationState(SituationState):
    pass

class BartenderSituation(SituationComplexCommon):
    INSTANCE_TUNABLES = {'bartender_job_and_role': TunableSituationJobAndRoleState(description='\n            The job and role of the bartender.\n            ')}
    REMOVE_INSTANCE_TUNABLES = Situation.NON_USER_FACING_REMOVE_INSTANCE_TUNABLES

    @classmethod
    def _states(cls):
        return (SituationStateData(1, _BartenderSituationState),)

    @classmethod
    def _get_tuned_job_and_default_role_state_tuples(cls):
        return [(cls.bartender_job_and_role.job, cls.bartender_job_and_role.role_state)]

    @classmethod
    def default_job(cls):
        pass

    def start_situation(self):
        super().start_situation()
        self._change_state(_BartenderSituationState())

class BartenderSpecificSimSituation(BartenderSituation):

    @classmethod
    def get_predefined_guest_list(cls):
        guest_list = SituationGuestList(invite_only=True)
        active_sim_info = services.active_sim_info()
        filter_result = services.sim_filter_service().submit_matching_filter(sim_filter=cls.bartender_job_and_role.job.filter, callback=None, requesting_sim_info=active_sim_info, allow_yielding=False, allow_instanced_sims=True, gsi_source_fn=cls.get_sim_filter_gsi_name)
        if not filter_result:
            logger.error('Failed to find/create any sims for {}.', cls)
            return guest_list
        guest_list.add_guest_info(SituationGuestInfo(filter_result[0].sim_info.sim_id, cls.bartender_job_and_role.job, RequestSpawningOption.DONT_CARE, BouncerRequestPriority.EVENT_VIP))
        return guest_list
