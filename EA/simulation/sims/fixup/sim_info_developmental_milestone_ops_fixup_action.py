from developmental_milestones.developmental_milestone_ops import DevelopmentalMilestoneStateChangeLootOpfrom event_testing.resolver import SingleSimResolverfrom sims.fixup.sim_info_fixup_action import _SimInfoFixupActionfrom sims4.tuning.tunable import TunableList
class _SimInfoDevelopmentalMilestoneOpsFixupAction(_SimInfoFixupAction):
    FACTORY_TUNABLES = {'developmental_milestone_state_change_list': TunableList(description='\n            A list of Developmental Milestones State Change Ops to run on the Sim.\n            ', tunable=DevelopmentalMilestoneStateChangeLootOp.TunableFactory())}

    def __call__(self, sim_info):
        resolver = SingleSimResolver(sim_info)
        for developmental_milestone_op in self.developmental_milestone_state_change_list:
            developmental_milestone_op.apply_to_resolver(resolver)
