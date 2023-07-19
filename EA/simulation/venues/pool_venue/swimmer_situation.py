import random
class _SwimmerSituationState(SituationState):
    pass

class PoolVenueSwimmerSituation(SituationComplexCommon):
    INSTANCE_TUNABLES = {'swimmer_job_and_role': TunableSituationJobAndRoleState(description='\n            The job and role for Pool Venue swimmers.\n            ')}
    REMOVE_INSTANCE_TUNABLES = Situation.NON_USER_FACING_REMOVE_INSTANCE_TUNABLES

    @classmethod
    def _states(cls):
        return (SituationStateData(1, _SwimmerSituationState),)

    @classmethod
    def _get_tuned_job_and_default_role_state_tuples(cls):
        return [(cls.swimmer_job_and_role.job, cls.swimmer_job_and_role.role_state)]

    @classmethod
    def default_job(cls):
        return cls.swimmer_job_and_role.job

    def start_situation(self):
        super().start_situation()
        self._change_state(_SwimmerSituationState())
