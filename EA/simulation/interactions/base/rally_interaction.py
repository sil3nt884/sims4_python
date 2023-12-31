from autonomy.autonomy_modes import FullAutonomyfrom autonomy.autonomy_request import AutonomyRequestfrom event_testing.resolver import SingleSimResolverfrom interactions.aop import AffordanceObjectPairfrom interactions.base.super_interaction import RallySourcefrom interactions.context import QueueInsertStrategy, InteractionContextfrom interactions.priority import Priorityfrom objects.base_interactions import ProxyInteractionfrom sims.party import Partyfrom sims4.utils import classproperty, flexmethodfrom singletons import DEFAULTimport servicesimport sims4.logimport singletonslogger = sims4.log.Logger('RallyInteraction', default_owner='jdimailig')
class RallyInteraction(ProxyInteraction):
    INSTANCE_SUBCLASSES_ONLY = True

    @classproperty
    def proxy_name(cls):
        return '[Rally]'

    def __init__(self, *args, from_rally_interaction=None, push_social=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._rally_targets = None
        self._from_rally_interaction = from_rally_interaction
        self._push_social = push_social
        self.preferred_carrying_sims = set()
        self._eligible_carryable_sims = set()
        self._eligible_carrying_sims = set()

    @classmethod
    def generate(cls, proxied_affordance, rally_tag, rally_level, rally_data, rally_push_social=None, rally_constraint=None, rally_sources=(), rally_pie_menu_icon=None, rally_allow_forward=False, rally_carry_rule=None):
        rally_affordance = proxied_affordance
        result = super().generate(rally_affordance)
        result.rally_tag = rally_tag
        result.rally_level = rally_level
        result.rally_data = rally_data
        result.rally_push_social = rally_push_social
        result.rally_constraint = rally_constraint
        result.rally_sources = rally_sources
        if rally_pie_menu_icon is not None:
            result.pie_menu_icon = rally_pie_menu_icon
        result.rally_allow_forward = rally_allow_forward
        result.rally_carry_rule = rally_carry_rule
        return result

    @classproperty
    def is_rally_interaction(cls):
        return True

    @classmethod
    def potential_interactions(cls, target, context, **kwargs):
        yield AffordanceObjectPair(cls, target, cls, None, **kwargs)

    @classmethod
    def generate_continuation_affordance(cls, affordance, **kwargs):
        return RallyInteraction.generate(affordance, rally_tag=cls.rally_tag, rally_level=cls.rally_level + 1, rally_data=None, rally_sources=cls.rally_sources, **kwargs)

    @flexmethod
    def _get_name(cls, inst, target=DEFAULT, context=DEFAULT, **kwargs):
        if inst is not None or cls.rally_data is None:
            return super(ProxyInteraction, inst)._get_name(target=target, context=context, **kwargs)
        original_name = super(ProxyInteraction, cls)._get_name(target=target, context=context, **kwargs)
        return cls.rally_data.loc_display_name(original_name)

    @classmethod
    def autonomy_ads_gen(cls, *args, **kwargs):
        for op in Party.RALLY_FALSE_ADS:
            cls._add_autonomy_ad(op, overwrite=False)
        for ad in super().autonomy_ads_gen(*args, **kwargs):
            yield ad
        for op in Party.RALLY_FALSE_ADS:
            cls._remove_autonomy_ad(op)

    @flexmethod
    def _constraint_gen(cls, inst, *args, **kwargs):
        inst_or_cls = inst if inst is not None else cls
        for constraint in super(__class__, inst_or_cls)._constraint_gen(*args, **kwargs):
            yield constraint
        if cls.rally_constraint is not None:
            yield cls.rally_constraint

    def _run_interaction_gen(self, timeline):
        main_group = self.sim.get_visible_group()
        if self._push_social is not None and main_group is None:
            context = InteractionContext(self.sim, InteractionContext.SOURCE_SCRIPT, self.context.priority)
            self.sim.push_super_affordance(self._push_social, self._from_rally_interaction.sim, context)
        yield from super()._run_interaction_gen(timeline)

    def disable_displace(self, other):
        if isinstance(other, RallyInteraction):
            return self._from_rally_interaction is other or other._from_rally_interaction is self
        return False

    def excluded_posture_destination_objects(self):
        excluded = set()
        if self._from_rally_interaction is None or self._from_rally_interaction.transition is None:
            return excluded
        for dest in self._from_rally_interaction.transition.final_destinations_gen():
            if dest.body_target is not None:
                excluded.add(dest.body_target)
        return excluded

    def _get_rally_affordance(self):
        affordance = None
        if hasattr(self.rally_data, 'affordance'):
            affordance = self.rally_data.affordance
        if affordance is None:
            return self.proxied_affordance
        return affordance or None

    def _get_rally_affordance_target(self):
        affordance_target_type = self.rally_data.affordance_target
        if affordance_target_type is not None:
            return self.get_participant(affordance_target_type)
        return affordance_target_type

    def _get_rally_static_commodity(self):
        if hasattr(self.rally_data, 'static_commodity'):
            return self.rally_data.static_commodity

    def _do_rally_behavior(self, sim, constraint):
        if sim is self.sim:
            return False
        if sim in self.preferred_carrying_sims:
            return False
        preferred_carrying_sim = None
        if sim in self._eligible_carryable_sims:
            preferred_carrying_sim = self._get_preferred_carrying_sim()
        if self.rally_data is None:
            return False
        target = None
        if self.rally_constraint is not None:
            constraint = self.rally_constraint
        context = self.context.clone_for_sim(sim, insert_strategy=QueueInsertStrategy.NEXT, preferred_carrying_sim=preferred_carrying_sim)
        if not self.rally_data.preserve_preferred_objects:
            context.preferred_objects = set()
        affordance = self._get_rally_affordance()
        context.run_priority = Priority.Low
        static_commodity = self._get_rally_static_commodity()
        if hasattr(self.rally_data, 'preserve_preferred_objects') and affordance is None and static_commodity is None:
            return False
        if static_commodity is None:
            target = self._get_rally_affordance_target()
            if target.is_part:
                target = target.part_owner
        else:
            request = AutonomyRequest(sim, static_commodity_list=(static_commodity,), skipped_static_commodities=None, object_list=self._rally_targets, constraint=constraint, context=context, autonomy_mode=FullAutonomy, autonomy_mode_label_override='RallyBehavior')
            autonomy_result = services.autonomy_service().score_all_interactions(request)
            if self._rally_targets is None:
                self._rally_targets = {}
                for scored_interaction_data in autonomy_result:
                    num_possible_parts = 0
                    possible_target = scored_interaction_data.interaction.target
                    if possible_target is not None and possible_target.parts is not None:
                        for part in possible_target.parts:
                            if part.in_use:
                                pass
                            if part.supports_affordance(scored_interaction_data.interaction.affordance):
                                num_possible_parts = num_possible_parts + 1
                    else:
                        num_possible_parts = 1
                    if self.target == possible_target:
                        num_possible_parts = num_possible_parts - 1
                    if num_possible_parts > 0:
                        self._rally_targets[possible_target] = num_possible_parts
            appropriate_scored_interactons = tuple([scored_interaction_data for scored_interaction_data in autonomy_result if scored_interaction_data.interaction.target in self._rally_targets])
            chosen_interaction = services.autonomy_service().choose_best_interaction(appropriate_scored_interactons, request)
            request.invalidate_created_interactions(excluded_si=chosen_interaction)
            if chosen_interaction is None:
                logger.warn('Unable to find an interaction to satisfy {} in {}', static_commodity, request)
                return False
            else:
                affordance = chosen_interaction.affordance
                target = chosen_interaction.target
                if target is not None:
                    num_parts_remaining = self._rally_targets.get(target, 1) - 1
                    if num_parts_remaining <= 0:
                        del self._rally_targets[target]
                    else:
                        self._rally_targets[target] = num_parts_remaining
                if affordance is not None:
                    affordance = self.generate_continuation_affordance(affordance, rally_constraint=constraint)
                    rallyable_parameters = self.get_rallyable_interaction_parameters()
                    interaction_parameters = self.interaction_parameters
                    if rallyable_parameters is not None:
                        interaction_parameters.update(rallyable_parameters)
                    result = sim.push_super_affordance(affordance, target, context, from_rally_interaction=self, push_social=self.rally_push_social, **interaction_parameters)
                    if result and preferred_carrying_sim is not None:
                        self.preferred_carrying_sims.add(preferred_carrying_sim)
                    return result
        if affordance is not None:
            affordance = self.generate_continuation_affordance(affordance, rally_constraint=constraint)
            rallyable_parameters = self.get_rallyable_interaction_parameters()
            interaction_parameters = self.interaction_parameters
            if rallyable_parameters is not None:
                interaction_parameters.update(rallyable_parameters)
            result = sim.push_super_affordance(affordance, target, context, from_rally_interaction=self, push_social=self.rally_push_social, **interaction_parameters)
            if result and preferred_carrying_sim is not None:
                self.preferred_carrying_sims.add(preferred_carrying_sim)
            return result
        return False

    def _process_for_carry(self, group_sims_list):
        if self.rally_carry_rule is None:
            return
        carryable_sim_eligibility_tests = self.rally_carry_rule.carryable_sim_eligibility_tests
        carrying_sim_eligibility_tests = self.rally_carry_rule.carrying_sim_eligibility_tests
        for sim in group_sims_list:
            resolver = SingleSimResolver(sim.sim_info)
            if carryable_sim_eligibility_tests.run_tests(resolver):
                self._eligible_carryable_sims.add(sim)
            elif carrying_sim_eligibility_tests.run_tests(resolver):
                self._eligible_carrying_sims.add(sim)
        if self.sim in self._eligible_carryable_sims and self.context.preferred_carrying_sim is None:
            preferred_carrying_sim = self._get_preferred_carrying_sim()
            if preferred_carrying_sim is not None:
                self.context.preferred_carrying_sim = preferred_carrying_sim
                self.preferred_carrying_sims.add(preferred_carrying_sim)
        group_sims_list.sort(key=lambda s: s in self._eligible_carryable_sims, reverse=True)

    def _get_preferred_carrying_sim(self):
        carrying_sim_list = list(self._eligible_carrying_sims)
        preferred_carrying_sim = next(iter(sim for sim in carrying_sim_list if sim not in self.preferred_carrying_sims), None)
        if preferred_carrying_sim is None:
            return next(iter(carrying_sim_list), None)
        return preferred_carrying_sim

    def maybe_bring_group_along(self, **kwargs):
        if not self.should_rally:
            return
        anchor_object = self.target
        if anchor_object.is_part:
            anchor_object = anchor_object.part_owner
        if anchor_object is not None and RallySource.SOCIAL_GROUP in self.rally_sources:
            main_group = self.sim.get_visible_group()
            if main_group:
                main_group.try_relocate_around_focus(self.sim, priority=self.priority)
                main_group_sims_list = list(main_group)
                self._process_for_carry(main_group_sims_list)
                for sim in main_group_sims_list:
                    self._do_rally_behavior(sim, main_group.get_constraint(sim))
        else:
            main_group = None
        if RallySource.ENSEMBLE in self.rally_sources:
            ensemble_sims = services.ensemble_service().get_ensemble_sims_for_rally(self.sim)
            if ensemble_sims:
                main_group_sims = set(main_group) if main_group else singletons.EMPTY_SET
                ensemble_sims -= main_group_sims
                ensemble_sims_list = list(ensemble_sims)
                self._process_for_carry(ensemble_sims_list)
                for sim in ensemble_sims_list:
                    self._do_rally_behavior(sim, None)

    @property
    def should_rally(self):
        if self._pushed_waiting_line:
            return False
        if self._from_rally_interaction is None:
            if RallySource.SOCIAL_GROUP in self.rally_sources:
                main_group = self.sim.get_visible_group()
                if main_group is not None and not main_group.is_solo:
                    return True
                elif RallySource.ENSEMBLE in self.rally_sources:
                    ensemble_sims = services.ensemble_service().get_ensemble_sims_for_rally(self.sim)
                    if ensemble_sims:
                        return True
            elif RallySource.ENSEMBLE in self.rally_sources:
                ensemble_sims = services.ensemble_service().get_ensemble_sims_for_rally(self.sim)
                if ensemble_sims:
                    return True
        return False
