import collections
class TunableAffordanceLinkList(TunableList):

    def __init__(self, class_restrictions=(), **kwargs):
        super().__init__(TunableReference(services.get_instance_manager(sims4.resources.Types.INTERACTION), category='asm', description='Linked Affordance', class_restrictions=class_restrictions, pack_safe=True), **kwargs)

class TunableStatisticAdvertisements(TunableList):

    def __init__(self, **kwargs):
        super().__init__(TunableStatisticChange(locked_args={'subject': ParticipantType.Actor, 'advertise': True}, statistic_override=StatisticChangeOp.get_statistic_override(pack_safe=True)), **kwargs)

class TunableContinuation(TunableList):
    TAGGED_ITEM = 0
    ITEM_DEFINITION = 1
    ITEM_TUNING_ID = 2

    def __init__(self, target_default=ParticipantType.Object, locked_args={}, carry_target_default=ParticipantType.Object, class_restrictions=(), **kwargs):
        super().__init__(tunable=TunableTuple(description='\n                A continuation entry.\n                ', affordance=TunableReference(description='\n                    The affordance to push as a continuation on the specified\n                    actor Sim.\n                    ', manager=services.get_instance_manager(sims4.resources.Types.INTERACTION), class_restrictions=class_restrictions, pack_safe=True), si_affordance_override=TunableReference(description="\n                When the tuned affordance is a mixer for a different SI, use\n                this to specify the mixer's appropriate SI. This is useful for\n                pushing socials.\n                ", manager=services.get_instance_manager(sims4.resources.Types.INTERACTION), allow_none=True), actor=TunableEnumEntry(description='\n                The Sim on which the affordance is pushed.\n                ', tunable_type=ParticipantType, default=ParticipantType.Actor), target=TunableEnumEntry(description='\n                The participant the affordance will target.\n                ', tunable_type=ParticipantType, default=target_default), carry_target=OptionalTunable(description='\n                If enabled, specify a carry target for this continuation.\n                ', tunable=TunableEnumEntry(description='\n                    The participant the affordance will set as a carry target.\n                    ', tunable_type=ParticipantType, default=carry_target_default)), inventory_carry_target=TunableVariant(description='\n                Item in inventory (of continuations actor) to use as carry\n                target for continuation if carry target is None\n                ', object_with_tag=CraftTaggedItemFactory(locked_args={'check_type': TunableContinuation.TAGGED_ITEM}), object_with_definition=TunableTuple(definition=TunableReference(description='\n                        The exact object definition to look for inside\n                        inventory.\n                        ', manager=services.definition_manager()), locked_args={'check_type': TunableContinuation.ITEM_DEFINITION}), object_with_base_definition=TunableTuple(definition=TunableReference(description='\n                        The base definition to look for inside inventory.\n                        Objects that redirect (like counters) will match if base\n                        definition is the same.\n                        ', manager=services.definition_manager()), locked_args={'check_type': TunableContinuation.ITEM_TUNING_ID}), locked_args={'None': None}, default='None'), preserve_preferred_object=Tunable(description="\n                If checked, the pushed interaction's preferred objects are\n                determined by the current preferred objects.\n                \n                If unchecked, the transition sequence would not award bonuses to\n                any specific part.\n                ", tunable_type=bool, default=True), preserve_target_part=Tunable(description='\n                If checked, the pushed interaction will use the same target part\n                if applicable. Defaults to false because typically we will want\n                to let the transition select which part to use.\n                ', tunable_type=bool, default=False), locked_args=locked_args), **kwargs)

class TimeoutLiability(Liability, HasTunableFactory):
    LIABILITY_TOKEN = 'TimeoutLiability'
    FACTORY_TUNABLES = {'description': 'Establish a timeout for this affordance. If it has not run when the timeout hits, cancel and push timeout_affordance, if set.', 'timeout': TunableSimMinute(4, minimum=0, description='The time, in Sim minutes, after which the interaction is canceled and time_toute affordance is pushed, if set.'), 'timeout_affordance': TunableReference(manager=services.get_instance_manager(sims4.resources.Types.INTERACTION), allow_none=True, description='The affordance to push when the timeout expires. Can be unset, in which case the interaction will just be canceled.')}

    def __init__(self, interaction, *, timeout, timeout_affordance, **kwargs):
        super().__init__(**kwargs)

        def on_alarm(*_, **__):
            if interaction.running:
                return
            if interaction.transition is not None and interaction.transition.running:
                return
            if timeout_affordance is not None:
                context = interaction.context.clone_for_continuation(interaction)
                interaction.sim.push_super_affordance(timeout_affordance, interaction.target, context)
            interaction.cancel(FinishingType.LIABILITY, cancel_reason_msg='Timeout after {} sim minutes.'.format(timeout))

        time_span = clock.interval_in_sim_minutes(timeout)
        self._handle = alarms.add_alarm(self, time_span, on_alarm)

    def release(self):
        alarms.cancel_alarm(self._handle)

    def should_transfer(self, continuation):
        return False
