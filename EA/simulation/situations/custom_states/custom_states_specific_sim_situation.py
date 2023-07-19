import services
class SpecificSimCustomStatesSituation(CustomStatesSituation):

    @classmethod
    def _verify_tuning_callback(cls):
        if cls.specific_sim_job.sim_auto_invite.lower_bound > 0 or cls.specific_sim_job.sim_auto_invite.upper_bound > 0:
            logger.error('The auto-invite count for specific sim job {} is greater than 0', cls.specific_sim_job)
        if cls.specific_sim_job.no_show_action == JobHolderNoShowAction.REPLACE_THEM:
            logger.error('The no show action for specific sim job {} is set to REPLACE THEM which can cause duplicate sims.', cls.specific_sim_job)
        if cls.specific_sim_job.died_or_left_action == JobHolderDiedOrLeftAction.REPLACE_THEM:
            logger.error('The Died or Left for specific sim job {} is set to REPLACE THEM which can cause duplicate sims.', cls.specific_sim_job)

    INSTANCE_TUNABLES = {'specific_sim_job': TunableReference(description='\n            The job specific Sim that has to be put into this situation no matter their current situation.\n            ', manager=services.get_instance_manager(Types.SITUATION_JOB), tuning_group=GroupNames.CORE), 'specific_sim_expectation_preference': Tunable(description='\n            If the expectation preference is set for the invite to this situation.  This is a function of\n            exclusivity.  Please talk to your GPE partner of if this should be checked or not.\n            ', tunable_type=bool, default=True)}

    @classmethod
    def get_predefined_guest_list(cls):
        guest_list = SituationGuestList(invite_only=True)
        active_sim_info = services.active_sim_info()
        filter_result = services.sim_filter_service().submit_matching_filter(sim_filter=cls.specific_sim_job.filter, callback=None, requesting_sim_info=active_sim_info, allow_yielding=False, allow_instanced_sims=True, gsi_source_fn=cls.get_sim_filter_gsi_name)
        guest_list.add_guest_info(SituationGuestInfo(filter_result[0].sim_info.sim_id, cls.specific_sim_job, RequestSpawningOption.DONT_CARE, BouncerRequestPriority.EVENT_VIP, expectation_preference=cls.specific_sim_expectation_preference))
        return guest_list
