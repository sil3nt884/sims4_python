from __future__ import annotationsfrom typing import TYPE_CHECKINGif TYPE_CHECKING:
    from typing import *
    from objects import base_interactions
    from objects.definition import Definitionfrom _collections import defaultdictimport functoolsimport randomfrom autonomy.autonomy_preference import ObjectPreferenceTagfrom build_buy import get_object_in_household_inventory, find_objects_in_household_inventoryfrom event_testing.resolver import SingleObjectResolver, InteractionResolver, SingleSimResolver, DoubleSimAndObjectResolverfrom event_testing.tests import TunableTestSetfrom filters.tunable import TunableSimFilterfrom fishing.fishing_tuning import FishingTuningfrom interactions import ParticipantType, ParticipantTypeSinglefrom interactions.aop import AffordanceObjectPairfrom interactions.base.immediate_interaction import ImmediateSuperInteractionfrom interactions.base.picker_strategy import SimPickerEnumerationStrategy, LotPickerEnumerationStrategy, ObjectPickerEnumerationStrategyfrom interactions.base.object_picker_mixins import GigObjectsPickerMixin, TunableObjectTaggedObjectFilterTestSet, StyleTagObjectPickerMixinfrom interactions.base.super_interaction import SuperInteractionfrom interactions.context import InteractionContext, QueueInsertStrategy, InteractionSourcefrom interactions.picker.picker_pie_menu_interaction import _PickerPieMenuProxyInteractionfrom interactions.picker.purchase_picker_service import PurchasePickerGroupfrom interactions.utils.destruction_liability import DeleteObjectLiability, DELETE_OBJECT_LIABILITYfrom interactions.utils.localization_tokens import LocalizationTokensfrom interactions.utils.loot import LootActionsfrom interactions.utils.loot_ops import SlotObjectsfrom interactions.utils.object_definition_or_tags import ObjectDefinitonsOrTagsVariantfrom interactions.utils.outcome import InteractionOutcome, TunableOutcomefrom interactions.utils.outcome_enums import OutcomeResultfrom interactions.utils.tunable import TunableContinuationfrom objects.auto_pick import AutoPick, AutoPickRandomfrom objects.base_object import BaseObjectfrom objects.components.inventory_enums import InventoryTypefrom objects.components.state import TimedStateChangeOpfrom objects.components.statistic_types import StatisticComponentGlobalTuningfrom objects.components.types import STATE_COMPONENTfrom objects.hovertip import TooltipFieldsfrom objects.object_tests import ObjectTypeFactory, ObjectTagFactory, InventoryTestfrom objects.script_object import ScriptObjectfrom objects.terrain import get_venue_instance_from_pick_locationfrom plex.plex_enums import PlexBuildingTypefrom protocolbuffers import SimObjectAttributes_pb2 as protocolsfrom sims.sim_info_types import Agefrom sims4 import mathfrom sims4.localization import TunableLocalizedStringFactory, LocalizationHelperTuning, TunableLocalizedStringFactoryVariantfrom sims4.random import pop_weightedfrom sims4.tuning.instances import lock_instance_tunablesfrom sims4.tuning.tunable import TunableEnumEntry, OptionalTunable, TunableVariant, Tunable, TunableTuple, TunableReference, TunableSet, TunableList, TunableFactory, TunableThreshold, TunableMapping, TunableRange, HasTunableSingletonFactory, AutoFactoryInit, TunableEnumWithFilter, TunableSimMinutefrom sims4.tuning.tunable_base import GroupNamesfrom sims4.tuning.tunable_hash import TunableStringHash32from sims4.utils import flexmethod, classpropertyfrom singletons import DEFAULTfrom snippets import TunableVenueListReferencefrom tunable_multiplier import TunableMultiplierfrom ui.ui_dialog import PhoneRingTypefrom ui.ui_dialog_notification import TunableUiDialogNotificationSnippetfrom ui.ui_dialog_picker import logger, TunablePickerDialogVariant, SimPickerRow, ObjectPickerRow, ObjectPickerTuningFlags, PurchasePickerRow, LotPickerRowfrom world import regionimport build_buyimport element_utilsimport enumimport event_testing.resultsimport gsi_handlersimport servicesimport simsimport sims4.resourcesimport tagimport telemetry_helperTELEMETRY_GROUP_PICKERINTERACTION = 'PINT'TELEMETRY_HOOK_INTERACTION_START = 'ACTV'TELEMETRY_FIELD_INTERACTION_ID = 'actv'TELEMETRY_FIELD_PICKED_COUNT = 'snum'pickerinteraction_telemetry_writer = sims4.telemetry.TelemetryWriter(TELEMETRY_GROUP_PICKERINTERACTION)
class PickerInteractionDeliveryMethod(enum.Int):
    INVENTORY = 0
    MAILMAN = 1
    SLOT_TO_PARENT = 2
    DELIVERY_SERVICE_NPC = 3
    export = False

class _TunablePieMenuOptionTuple(TunableTuple):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, show_disabled_item=Tunable(description='\n                If checked, the disabled item will show as disabled in the Pie\n                Menu with a greyed-out tooltip. Otherwise the disabled item will\n                not show up in the pie menu.\n                ', tunable_type=bool, default=False), pie_menu_category=TunableReference(description="\n                If set, then the generated Pie Menu interaction will be\n                categorized under this Pie Menu category, as opposed to using\n                the interaction's Pie Menu category.\n                ", manager=services.get_instance_manager(sims4.resources.Types.PIE_MENU_CATEGORY), allow_none=True, tuning_group=GroupNames.UI), force_pie_menu_category=Tunable(description='\n                If enabled, we will use the pie_menu_category tuned here even if the row_data (for instance, recipes) \n                of this picker normally specify their own picker categories. This can be useful when re-using row data\n                in a new pie menu picker with a different intended category.\n                ', tunable_type=bool, default=False), pie_menu_name=TunableLocalizedStringFactory(description="\n                The localized name for the pie menu item. The content should\n                always have {2.String} to wrap picker row data's name.\n                "), **kwargs)

class PickerSuperInteractionMixin:
    INSTANCE_TUNABLES = {'picker_dialog': TunablePickerDialogVariant(description='\n            The object picker dialog.\n            ', tuning_group=GroupNames.PICKERTUNING), 'pie_menu_option': OptionalTunable(description='\n            Whether use Pie Menu to show choices other than picker dialog.\n            ', tunable=_TunablePieMenuOptionTuple(), disabled_name='use_picker', enabled_name='use_pie_menu', tuning_group=GroupNames.PICKERTUNING), 'pie_menu_test_tooltip': OptionalTunable(description='\n            If enabled, then a greyed-out tooltip will be displayed if there\n            are no valid choices. When disabled, the test to check for valid\n            choices will run first and if it fail any other tuned test in the\n            interaction will not get run. When enabled, the tooltip will be the\n            last fallback tooltip, and if other tuned interaction tests have\n            tooltip, those tooltip will show first. [cjiang/scottd]\n            ', tunable=TunableLocalizedStringFactory(description='\n                The tooltip text to show in the greyed-out tooltip when no valid\n                choices exist.\n                '), tuning_group=GroupNames.PICKERTUNING)}

    @classmethod
    def _test(cls, *args, picked_row=None, **kwargs):
        result = super()._test(*args, **kwargs)
        if not result:
            return result
        if picked_row is not None and not picked_row.is_enable:
            return event_testing.results.TestResult(False, 'This picker SI has no valid choices.', tooltip=picked_row.row_tooltip)
        if not cls.has_valid_choice(*args, **kwargs):
            disabled_tooltip = cls.get_disabled_tooltip(*args, **kwargs)
            return event_testing.results.TestResult(False, 'This picker SI has no valid choices.', tooltip=disabled_tooltip)
        return event_testing.results.TestResult.TRUE

    @flexmethod
    def _get_name(cls, inst, *args, **kwargs):
        inst_or_cls = inst if inst is not None else cls
        text = super(__class__, inst_or_cls)._get_name(*args, **kwargs)
        if inst_or_cls._use_ellipsized_name():
            text = LocalizationHelperTuning.get_ellipsized_text(text)
        return text

    @flexmethod
    def _use_ellipsized_name(cls, inst):
        return True

    @classmethod
    def has_valid_choice(cls, target, context, **kwargs):
        return True

    @classmethod
    def get_disabled_tooltip(cls, *args, **kwargs):
        return cls.pie_menu_test_tooltip

    @classmethod
    def use_pie_menu(cls):
        if cls.pie_menu_option is not None:
            return True
        return False

    def _show_picker_dialog(self, owner, **kwargs):
        if self.use_pie_menu():
            return
        dialog = self._create_dialog(owner, **kwargs)
        dialog.show_dialog()

    def _create_dialog(self, owner, target_sim=None, target=None, **kwargs):
        if self.picker_dialog.title is None:
            title = lambda *_, **__: self.get_name(apply_name_modifiers=False)
        else:
            title = self.picker_dialog.title
        dialog = self.picker_dialog(owner, title=title, resolver=self.get_resolver())
        self._setup_dialog(dialog, **kwargs)
        dialog.set_target_sim(target_sim)
        dialog.set_target(target)
        dialog.current_selected = self._get_current_selected_count()
        dialog.add_listener(self._on_picker_selected)
        return dialog

    @classmethod
    def potential_interactions(cls, target, context, **kwargs):
        if cls.use_pie_menu():
            if context.source == InteractionSource.AUTONOMY and not cls.allow_autonomous:
                return
            recipe_ingredients_map = {}
            funds_source = cls.funds_source if hasattr(cls, 'funds_source') else None
            for row_data in cls.picker_rows_gen(target, context, funds_source=funds_source, recipe_ingredients_map=recipe_ingredients_map, **kwargs):
                if not row_data.available_as_pie_menu:
                    pass
                else:
                    affordance = _PickerPieMenuProxyInteraction.generate(cls, picker_row_data=row_data)
                    for aop in affordance.potential_interactions(target, context, recipe_ingredients_map=recipe_ingredients_map, **kwargs):
                        yield aop
        else:
            yield from super().potential_interactions(target, context, **kwargs)

    @flexmethod
    def picker_rows_gen(cls, inst, target, context, **kwargs):
        raise NotImplementedError

    def _setup_dialog(self, dialog, **kwargs):
        for row in self.picker_rows_gen(self.target, self.context, **kwargs):
            dialog.add_row(row)

    def _on_picker_selected(self, dialog):
        if dialog.multi_select:
            tag_objs = dialog.get_result_tags()
            self.on_multi_choice_selected(tag_objs, ingredient_check=dialog.ingredient_check)
        else:
            tag_obj = dialog.get_single_result_tag()
            self.on_choice_selected(tag_obj, ingredient_check=dialog.ingredient_check)

    def on_multi_choice_selected(self, picked_choice, **kwargs):
        raise NotImplementedError

    def on_choice_selected(self, picked_choice, **kwargs):
        raise NotImplementedError

    def _get_current_selected_count(self):
        return 0

class PickerSuperInteraction(PickerSuperInteractionMixin, ImmediateSuperInteraction):
    INSTANCE_SUBCLASSES_ONLY = True

    @classmethod
    def _verify_tuning_callback(cls):
        if cls.allow_user_directed or cls.pie_menu_option is not None:
            logger.error('{} is tuned to be disallowed user directed but has Pie Menu options. Suggestion: allow the interaction to be user directed.', cls.__name__)
        return super()._verify_tuning_callback()

    def __init__(self, *args, choice_enumeration_strategy=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._choice_enumeration_strategy = choice_enumeration_strategy
        if self.allow_autonomous and self._choice_enumeration_strategy is None:
            logger.error('{} is a new PickerSuperInteraction that was added without also adding an appropriate ChoiceEnumerationStrategy.  The owner of this SI should set up a new strategy or use an existing one.  See me if you have any questions.'.format(self), owner='rez')
lock_instance_tunables(PickerSuperInteraction, outcome=InteractionOutcome())
class PickerSingleChoiceSuperInteraction(PickerSuperInteraction):
    INSTANCE_SUBCLASSES_ONLY = True
    INSTANCE_TUNABLES = {'single_choice_display_name': OptionalTunable(tunable=TunableLocalizedStringFactory(description="\n                The name of the interaction if only one option is available. There\n                should be a single token for the item that's used. The token will\n                be replaced with the name of a Sim in Sim Pickers, or an object\n                for recipes, etc.\n                 \n                Picked Sim/Picked Object participants can be used as display\n                name tokens.\n                ", default=None), tuning_group=GroupNames.UI)}

    @classmethod
    def potential_interactions(cls, target, context, **kwargs):
        if context.source == InteractionSource.AUTONOMY and not cls.allow_autonomous:
            return
        single_row = None
        (_, single_row) = cls.get_single_choice_and_row(context=context, target=target, **kwargs)
        if cls.single_choice_display_name is not None and single_row is None:
            yield from super().potential_interactions(target, context, **kwargs)
        else:
            picked_id = cls._get_id_from_row_tag(single_row.tag)
            picked_item_ids = () if single_row is None else (picked_id,)
            yield AffordanceObjectPair(cls, target, cls, None, picked_item_ids=picked_item_ids, picked_row=single_row, **kwargs)

    @flexmethod
    def _get_name(cls, inst, target=DEFAULT, context=DEFAULT, picked_row=None, **interaction_parameters):
        inst_or_cls = inst if inst is not None else cls
        context = inst_or_cls.context if context is DEFAULT else context
        target = inst_or_cls.target if target is DEFAULT else target
        if inst_or_cls.single_choice_display_name is not None and picked_row is not None:
            (override_tunable, _) = inst_or_cls.get_name_override_and_test_result(target=target, context=context, **interaction_parameters)
            loc_string = override_tunable.new_display_name if override_tunable is not None else None
            if loc_string is None:
                loc_string = inst_or_cls.single_choice_display_name
            display_name = inst_or_cls.create_localized_string(loc_string, picked_row.name, target=target, context=context, **interaction_parameters)
            return display_name
        return super(PickerSingleChoiceSuperInteraction, inst_or_cls)._get_name(target=target, context=context, **interaction_parameters)

    @flexmethod
    def get_single_choice_and_row(cls, inst, context=None, target=None, **kwargs):
        return (None, None)

    def _get_id_from_choice(self, choice):
        return choice

    @classmethod
    def _get_id_from_row_tag(cls, tag):
        return tag

    def _show_picker_dialog(self, owner, target_sim=None, target=None, choices=(), **kwargs):
        if self.use_pie_menu():
            return
        picked_item_ids = self.interaction_parameters.get('picked_item_ids')
        picked_item_ids = list(picked_item_ids) if picked_item_ids is not None else None
        if len(choices) == 1 and picked_item_ids:
            picked_id = picked_item_ids[0]
            choice_id = self._get_id_from_choice(choices[0])
            if choice_id == picked_id:
                self.on_choice_selected(picked_id)
                return
        dialog = self._create_dialog(owner, target_sim=None, target=target, **kwargs)
        dialog.show_dialog()

class AutonomousPickerSuperInteraction(SuperInteraction):

    def __init__(self, *args, choice_enumeration_strategy=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._choice_enumeration_strategy = choice_enumeration_strategy
lock_instance_tunables(AutonomousPickerSuperInteraction, allow_user_directed=False, basic_reserve_object=None, disable_transitions=True)
class SimPickerLinkContinuation(enum.Int):
    NEITHER = 0
    ACTOR = 1
    PICKED = 2
    ALL = 3
    TARGET = 4

class SimPickerMixin:
    INSTANCE_TUNABLES = {'actor_continuation': TunableContinuation(description='\n            If specified, a continuation to push on the actor when a picker\n            selection has been made.\n            ', locked_args={'actor': ParticipantType.Actor}, tuning_group=GroupNames.PICKERTUNING), 'target_continuation': TunableContinuation(description='\n            If specified, a continuation to push on the target sim when a picker\n            selection has been made.\n            ', locked_args={'actor': ParticipantType.TargetSim}, tuning_group=GroupNames.PICKERTUNING), 'picked_continuation': TunableContinuation(description='\n            If specified, a continuation to push on each sim selected in the\n            picker.\n            ', locked_args={'actor': ParticipantType.Actor}, tuning_group=GroupNames.PICKERTUNING), 'continuations_are_sequential': Tunable(description='\n            This specifies that the continuations tuned in picked_continuation\n            are applied sequentially to the list of picked sims.\n            \n            e.g. The first continuation will be pushed on the first picked sim.\n            The second continuation will be pushed on the second picked sim,\n            etc. Note: There should never be more picked sims than\n            continuations, however, there can be less picked sims than\n            continuations, to allow for cases where the number of sims is a\n            range.\n            ', tunable_type=bool, default=False, tuning_group=GroupNames.PICKERTUNING), 'continuations_are_multi_push': Tunable(description='\n            If true, will attempt to push all the continuations on each of the respective sims in order.\n            If False will stop pushing for each sim after an interaction has been successfully pushed.\n            \n            For picked continuations, this is ignored if continuations are sequential.\n            ', tunable_type=bool, default=True, tuning_group=GroupNames.PICKERTUNING), 'continuation_linking': TunableTuple(description='\n            How/if to link the continuations pushed by this picker. Specify \n            which continuations should be cancelled if any of the other \n            continuations are cancelled.\n            ', continuations_to_cancel=TunableEnumEntry(description='\n                Whose, if any, continuations pushed by this picker should cancel\n                if any of the other continuations pushed by this picker are\n                canceled. \n                \n                e.g. if "ACTOR" is selected, then if the target continuation or\n                any of the picked continuations are canceled the actor \n                continuation will also be canceled.\n                \n                Note:  Currently, if there is no actor or target continuation\n                then no link occurs.\n                ', tunable_type=SimPickerLinkContinuation, default=SimPickerLinkContinuation.NEITHER), cancel_entire_chain=Tunable(description='\n                By default (False) only the specific continuation pushed on the\n                target specified by continuation to cancel will be cancelled \n                if any other continuation (or it\'s continuations) are cancelled.\n                If true, that continuation as well as any continuations of that \n                continuation will be cancelled.\n                \n                e.g. \n                actorA continuation continues to actorB or actorC\n                targetA continuation continues to targetB or targetC\n                \n                if "continuations to cancel" is TARGET or ALL then if this\n                is false, canceling actorA, actorB, or actorC will cancel\n                targetA ONLY.  If the target has already continued to targetB\n                or targetC they will remain untouched.  However if this true, \n                canceling actorA, actorB, or actorC will cancel targetA, \n                targetB, or targetC if the target has already continued on to\n                either of them.\n                ', tunable_type=bool, default=False), tuning_group=GroupNames.PICKERTUNING), 'sim_filter': OptionalTunable(description='\n            Optional Sim Filter to run Sims through. Otherwise we will just get\n            all Sims that pass the tests.\n            ', tunable=TunableSimFilter.TunablePackSafeReference(description='\n                Sim Filter to run all Sims through before tests.\n                '), disabled_name='no_filter', enabled_name='sim_filter_selected', tuning_group=GroupNames.PICKERTUNING), 'sim_filter_household_override': OptionalTunable(description="\n            Sim filter by default uses the actor's household for household-\n            related filter terms, such as the In Family filter term. If this is\n            enabled, a different participant's household will be used. If the\n            participant is an object instead of a Sim, the object's owner\n            household will be used.\n            ", tunable=TunableEnumEntry(tunable_type=ParticipantTypeSingle, default=ParticipantTypeSingle.TargetSim, invalid_enums=(ParticipantTypeSingle.Actor,)), tuning_group=GroupNames.PICKERTUNING), 'sim_filter_requesting_sim': TunableEnumEntry(description='\n            Determine which Sim filter requests are relative to. For example, if\n            you want all Sims in a romantic relationship with the target, tune\n            TargetSim here, and then a relationship filter.\n            \n            NOTE: Tuning filters is, performance-wise, preferable to tests.\n            ', tunable_type=ParticipantTypeSingle, default=ParticipantTypeSingle.Actor, tuning_group=GroupNames.PICKERTUNING), 'create_sim_if_no_valid_choices': Tunable(description='\n            If checked, this picker will generate a sim that matches the tuned\n            filter if no other matching sims are available. This sim will match\n            the tuned filter, but not necessarily respect other rules of this \n            picker (like radius, tests, or instantiation). If you need one of\n            those things, see a GPE about improving this option.\n            ', tunable_type=bool, default=False, tuning_group=GroupNames.PICKERTUNING), 'sim_tests': event_testing.tests.TunableTestSet(description='\n            A set of tests that are run against the prospective sims. At least\n            one test must pass in order for the prospective sim to show. All\n            sims will pass if there are no tests. Picked_sim is the participant\n            type for the prospective sim.\n            ', tuning_group=GroupNames.PICKERTUNING), 'include_uninstantiated_sims': Tunable(description='\n            If unchecked, uninstantiated sims will never be available in the\n            picker. if checked, they must still pass the filters and tests This\n            is an optimization tunable.\n            ', tunable_type=bool, default=True, tuning_group=GroupNames.PICKERTUNING), 'include_instantiated_sims': Tunable(description='\n            If unchecked, instantiated sims will never be available in the\n            picker. if checked, they must still pass the filters and tests.\n            ', tunable_type=bool, default=True, tuning_group=GroupNames.PICKERTUNING), 'include_actor_sim': Tunable(description='\n            If checked then the actor sim can be included in the picker options\n            and will not be blacklisted.\n            ', tunable_type=bool, default=False, tuning_group=GroupNames.PICKERTUNING), 'include_target_sim': Tunable(description='\n            If checked then the target sim can be included in the picker options\n            and will not be blacklisted.\n            ', tunable_type=bool, default=False, tuning_group=GroupNames.PICKERTUNING), 'include_rabbithole_sims': Tunable(description='\n            If unchecked, rabbithole sims will never be available in the\n            picker. if checked, they must still pass the filters and tests.\n            ', tunable_type=bool, default=False, tuning_group=GroupNames.PICKERTUNING), 'include_missing_pets': Tunable(description='\n            If unchecked, missing pet sims will never be available in the\n            picker. if checked, they must still pass the filters and tests.\n            ', tunable_type=bool, default=False, tuning_group=GroupNames.PICKERTUNING), 'radius': OptionalTunable(description='\n            If enabled then Sim must be in a certain range for consideration.\n            This should only be enabled when include_instantiated_sims is True\n            and include_uninstantiated_sims is False.\n            ', tunable=TunableRange(description='\n                Sim must be in a certain range for consideration.\n                ', tunable_type=int, default=5, minimum=1, maximum=50), tuning_group=GroupNames.PICKERTUNING), 'success_loot_actions': TunableList(description='\n            List of loot actions to apply on successful picker selection.\n            ', tunable=LootActions.TunableReference(), tuning_group=GroupNames.PICKERTUNING), 'order_by_proximity': OptionalTunable(description='\n            If order_by_proximity is enabled, we find the nearest sim to this tuned participant.\n            ', tunable=TunableEnumEntry(tunable_type=ParticipantTypeSingle, default=ParticipantTypeSingle.Actor), tuning_group=GroupNames.PICKERTUNING)}

    @classmethod
    def _verify_tuning_callback(cls):
        super()._verify_tuning_callback()
        if cls.include_instantiated_sims and cls.include_uninstantiated_sims and cls.radius is not None:
            logger.error('Tuning: If include_instantiated_sims is False or include_uninstantiated_sims is True, radius should be disabled: {}', cls)

    @flexmethod
    def _get_requesting_sim_info_for_picker(cls, inst, context, *, target, **kwargs):
        inst_or_cls = inst if inst is not None else cls
        return inst_or_cls.get_participant(inst_or_cls.sim_filter_requesting_sim, sim=context.sim, target=target, **kwargs)

    @flexmethod
    def _get_actor_for_picker(cls, inst, context, *, target, **kwargs):
        sim = inst.sim if inst is not None else context.sim
        if sim is not None:
            return sim.sim_info

    @flexmethod
    def get_sim_filter_gsi_name(cls, inst):
        inst_or_cls = inst if inst is not None else cls
        return str(inst_or_cls)

    @flexmethod
    def _get_valid_sim_choices_gen(cls, inst, target, context, test_function=None, min_required=1, included_override=set(), excluded_override=set(), **kwargs):
        sim_info_manager = services.sim_info_manager()
        if included_override:
            for sim_id in included_override:
                sim_info = sim_info_manager.get(sim_id)
                if sim_info is not None:
                    yield sim_info
            return
        inst_or_cls = inst if inst is not None else cls
        requesting_sim_info = inst_or_cls._get_requesting_sim_info_for_picker(context, target=target, carry_target=context.carry_target, **kwargs)
        if requesting_sim_info is None:
            return
        actor_sim_info = inst_or_cls._get_actor_for_picker(context, target=target, **kwargs)
        household_id = None
        resolver = inst_or_cls.get_resolver(target=target, context=context)
        participant = resolver.get_participant(inst_or_cls.sim_filter_household_override)
        if participant.is_sim:
            household_id = participant.household_id
        else:
            household_id = participant.get_household_owner_id()
            household_id = 0
        sim_infos = sim_info_manager.get_all()
        pre_filtered_sim_infos = inst_or_cls.sim_filter.get_pre_filtered_sim_infos(requesting_sim_info=requesting_sim_info)
        sim_infos = pre_filtered_sim_infos
        valid_sims_found = 0
        for sim_info in sim_infos:
            if not sim_info.can_instantiate_sim:
                pass
            elif sim_info.sim_id in excluded_override:
                pass
            elif inst_or_cls.include_actor_sim or sim_info is actor_sim_info:
                pass
            elif inst_or_cls.include_target_sim or (not target is not None or not target.is_sim) or sim_info is target.sim_info:
                pass
            elif inst_or_cls.include_uninstantiated_sims or not sim_info.is_instanced():
                pass
            elif inst_or_cls.include_instantiated_sims or sim_info.is_instanced():
                pass
            elif inst_or_cls.radius is not None:
                sim = sim_info.get_sim_instance()
                if not sim is None:
                    if actor_sim_info is None:
                        pass
                    else:
                        actor_sim = actor_sim_info.get_sim_instance()
                        if actor_sim is None:
                            pass
                        else:
                            delta = actor_sim.intended_position - sim.intended_position
                            if delta.magnitude() > inst_or_cls.radius:
                                pass
                            else:
                                results = services.sim_filter_service().submit_filter(inst_or_cls.sim_filter, None, sim_constraints=(sim_info.sim_id,), requesting_sim_info=requesting_sim_info.sim_info, allow_yielding=False, household_id=household_id, gsi_source_fn=inst_or_cls.get_sim_filter_gsi_name, include_rabbithole_sims=inst_or_cls.include_rabbithole_sims, include_missing_pets=inst_or_cls.include_missing_pets)
                                if not results:
                                    pass
                                else:
                                    if inst:
                                        interaction_parameters = inst.interaction_parameters.copy()
                                    else:
                                        interaction_parameters = kwargs.copy()
                                    interaction_parameters['picked_item_ids'] = {sim_info.sim_id}
                                    resolver = InteractionResolver(cls, inst, target=target, context=context, **interaction_parameters)
                                    if not inst_or_cls.sim_tests or not inst_or_cls.sim_tests.run_tests(resolver):
                                        pass
                                    elif test_function is not None:
                                        sim = sim_info.get_sim_instance()
                                        if not sim is None:
                                            if not test_function(sim):
                                                pass
                                            else:
                                                valid_sims_found += 1
                                                yield results[0]
                                    else:
                                        valid_sims_found += 1
                                        yield results[0]
            else:
                results = services.sim_filter_service().submit_filter(inst_or_cls.sim_filter, None, sim_constraints=(sim_info.sim_id,), requesting_sim_info=requesting_sim_info.sim_info, allow_yielding=False, household_id=household_id, gsi_source_fn=inst_or_cls.get_sim_filter_gsi_name, include_rabbithole_sims=inst_or_cls.include_rabbithole_sims, include_missing_pets=inst_or_cls.include_missing_pets)
                if not results:
                    pass
                else:
                    if inst:
                        interaction_parameters = inst.interaction_parameters.copy()
                    else:
                        interaction_parameters = kwargs.copy()
                    interaction_parameters['picked_item_ids'] = {sim_info.sim_id}
                    resolver = InteractionResolver(cls, inst, target=target, context=context, **interaction_parameters)
                    if not inst_or_cls.sim_tests or not inst_or_cls.sim_tests.run_tests(resolver):
                        pass
                    elif test_function is not None:
                        sim = sim_info.get_sim_instance()
                        if not sim is None:
                            if not test_function(sim):
                                pass
                            else:
                                valid_sims_found += 1
                                yield results[0]
                    else:
                        valid_sims_found += 1
                        yield results[0]
        number_required_sims_not_found = min_required - valid_sims_found
        if inst_or_cls.sim_filter_household_override is not None and participant is not None and inst_or_cls.sim_filter is not None and pre_filtered_sim_infos is not None and inst_or_cls.create_sim_if_no_valid_choices and number_required_sims_not_found > 0:
            results = services.sim_filter_service().submit_matching_filter(number_of_sims_to_find=number_required_sims_not_found, sim_filter=inst_or_cls.sim_filter, requesting_sim_info=requesting_sim_info.sim_info, allow_yielding=False, household_id=household_id, gsi_source_fn=inst_or_cls.get_sim_filter_gsi_name)
            if results:
                yield from results

    def _push_continuation(self, sim, tunable_continuation, sim_ids, insert_strategy, picked_zone_set):
        continuation = None
        picked_item_set = {target_sim_id for target_sim_id in sim_ids if target_sim_id is not None}
        self.interaction_parameters['picked_item_ids'] = frozenset(picked_item_set)
        self.push_tunable_continuation(tunable_continuation, insert_strategy=insert_strategy, picked_item_ids=picked_item_set, picked_zone_ids=picked_zone_set, multi_push=self.continuations_are_multi_push)
        new_continuation = sim.queue.find_pushed_interaction_by_id(self.group_id)
        while new_continuation is not None:
            continuation = new_continuation
            new_continuation = sim.queue.find_continuation_by_id(continuation.id)
        return continuation

    def _push_continuations(self, sim_ids, zone_datas=None):
        if not self.picked_continuation:
            insert_strategy = QueueInsertStrategy.LAST
        else:
            insert_strategy = QueueInsertStrategy.NEXT
        picked_zone_set = None
        if zone_datas is not None:
            try:
                picked_zone_set = {zone_data.zone_id for zone_data in zone_datas if zone_data is not None}
            except TypeError:
                picked_zone_set = {zone_datas.zone_id}
            self.interaction_parameters['picked_zone_ids'] = frozenset(picked_zone_set)
        actor_continuation = None
        target_continuation = None
        picked_continuations = []
        if self.actor_continuation:
            actor_continuation = self._push_continuation(self.sim, self.actor_continuation, sim_ids, insert_strategy, picked_zone_set)
        if self.target_continuation:
            target_sim = self.get_participant(ParticipantType.TargetSim)
            if target_sim is not None:
                target_continuation = self._push_continuation(target_sim, self.target_continuation, sim_ids, insert_strategy, picked_zone_set)
        if self.picked_continuation:
            num_continuations = len(self.picked_continuation)
            for (index, target_sim_id) in enumerate(sim_ids):
                if target_sim_id is None:
                    pass
                else:
                    logger.info('SimPicker: picked Sim_id: {}', target_sim_id, owner='jjacobson')
                    target_sim = services.object_manager().get(target_sim_id)
                    if target_sim is None:
                        logger.error("You must pick on lot sims for a tuned 'picked continuation' to function.", owner='jjacobson')
                    else:
                        self.interaction_parameters['picked_item_ids'] = frozenset((target_sim_id,))
                        if self.continuations_are_sequential:
                            if index < num_continuations:
                                continuation = (self.picked_continuation[index],)
                            else:
                                logger.error('There are not enough tuned picked continuations for the interaction {}, so picked sim {} and all others afterwards will be skipped.', self, target_sim, owner='johnwilkinson')
                                break
                        else:
                            continuation = self.picked_continuation
                        self.push_tunable_continuation(continuation, insert_strategy=insert_strategy, actor=target_sim, picked_zone_ids=picked_zone_set, multi_push=self.continuations_are_multi_push)
                        picked_continuation = target_sim.queue.find_pushed_interaction_by_id(self.group_id)
                        if picked_continuation is not None:
                            new_continuation = target_sim.queue.find_continuation_by_id(picked_continuation.id)
                            while new_continuation is not None:
                                picked_continuation = new_continuation
                                new_continuation = target_sim.queue.find_continuation_by_id(picked_continuation.id)
                            picked_continuations.append(picked_continuation)
        link_type = self.continuation_linking.continuations_to_cancel
        if link_type != SimPickerLinkContinuation.NEITHER:
            link_chain = self.continuation_linking.cancel_entire_chain
            if actor_continuation is not None:
                if target_continuation is not None and (link_type == SimPickerLinkContinuation.TARGET or link_type == SimPickerLinkContinuation.ALL):
                    actor_continuation.attach_interaction(target_continuation, cancel_continuations=link_chain)
                for interaction in picked_continuations:
                    if link_type == SimPickerLinkContinuation.ACTOR or link_type == SimPickerLinkContinuation.ALL:
                        interaction.attach_interaction(actor_continuation, cancel_continuations=link_chain)
                    if not link_type == SimPickerLinkContinuation.PICKED:
                        if link_type == SimPickerLinkContinuation.ALL:
                            actor_continuation.attach_interaction(interaction, cancel_continuations=link_chain)
                    actor_continuation.attach_interaction(interaction, cancel_continuations=link_chain)
            if target_continuation is not None:
                if actor_continuation is not None and (link_type == SimPickerLinkContinuation.ACTOR or link_type == SimPickerLinkContinuation.ALL):
                    target_continuation.attach_interaction(actor_continuation, cancel_continuations=link_chain)
                for interaction in picked_continuations:
                    if link_type == SimPickerLinkContinuation.TARGET or link_type == SimPickerLinkContinuation.ALL:
                        interaction.attach_interaction(target_continuation, cancel_continuations=link_chain)
                    if not link_type == SimPickerLinkContinuation.PICKED:
                        if link_type == SimPickerLinkContinuation.ALL:
                            target_continuation.attach_interaction(interaction, cancel_continuations=link_chain)
                    target_continuation.attach_interaction(interaction, cancel_continuations=link_chain)

    def _apply_loot(self, results):
        interaction_parameters = {}
        resolver = self.get_resolver()
        if results is not None:
            interaction_parameters['picked_item_ids'] = results
        resolver.interaction_parameters = interaction_parameters
        for loot in self.success_loot_actions:
            loot.apply_to_resolver(resolver)

class SimPickerInteraction(SimPickerMixin, PickerSingleChoiceSuperInteraction):
    INSTANCE_TUNABLES = {'picker_dialog': TunablePickerDialogVariant(description='The object picker dialog.', available_picker_flags=ObjectPickerTuningFlags.SIM, tuning_group=GroupNames.PICKERTUNING), 'default_selection_tests': OptionalTunable(description='\n            If enabled, any Sim who passes these tests will be selected by\n            default when the picker pops up.\n            ', tunable=event_testing.tests.TunableTestSet(description='\n                A set of tests that will automatically select Sims that pass\n                when the Sim Picker pops up.\n                '), tuning_group=GroupNames.PICKERTUNING), 'default_selections_sort_to_front': Tunable(description='\n            If checked then any Sim that passes the default selection tests\n            will be sorted to the top of the list.\n            ', tunable_type=bool, default=False), 'carry_item_from_inventory': OptionalTunable(description='\n            If enabled continuations will set the carry target on the \n            interaction context to an object with the specified tag found on\n            the inventory of the Sim running this interaction.\n            ', tunable=tag.TunableTags(description='\n                The set of tags that are used to determine which objects to highlight.\n                ')), 'cell_enabled_tests': OptionalTunable(description='\n            Test to see if the cell should be enabled or not.\n            If it does not pass, it will disable the cell and optionally\n            override the tooltip.\n            ', tunable=event_testing.tests.TunableTestSetWithTooltip(tuning_group=GroupNames.TESTS), tuning_group=GroupNames.PICKERTUNING), 'requires_age_romance_check': Tunable(description='\n            If this is checked then we will check to see if the Sims ages allow romance (basically\n            t->yae and yae-> not allowed). If it is disallowed we will pass that piece of\n            information on to the ui via the tags list and it can use it to filter other filters\n            in a multi-picker situation. This should only be checked for use with picker\n            interactions inside of a multi-picker.\n            ', tunable_type=bool, default=False), 'report_picked_count': Tunable(description='\n            If checked, this interaction will send off telemetry data when sims are chosen for the interaction,\n            reporting the interaction ID, the initiating Sim ID, the number of picked sims, and the zone id.\n            ', tunable_type=bool, default=False, tuning_group=GroupNames.TELEMETRY)}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, choice_enumeration_strategy=SimPickerEnumerationStrategy(), **kwargs)

    def _run_interaction_gen(self, timeline):
        choices = tuple(self._get_valid_sim_choices_gen(self.target, self.context, min_required=self.picker_dialog.min_selectable))
        if len(choices) < self.picker_dialog.min_choices:
            return False
        if self.picker_dialog.min_selectable == 0 and not choices:
            self._on_successful_picker_selection()
            return True
        if len(choices) == 1:
            self._kwargs['picked_item_ids'] = (choices[0].sim_info.sim_id,)
        self._show_picker_dialog(self.sim, target_sim=self.sim, target=self.target, choices=choices)
        return True

    def _setup_dialog(self, dialog, **kwargs):
        super()._setup_dialog(dialog, **kwargs)
        if self.default_selections_sort_to_front:
            dialog.sort_selected_items_to_front()

    def _get_id_from_choice(self, choice):
        return choice.sim_info.id

    @flexmethod
    def create_row(cls, inst, tag, select_default=False):
        second_tag_list = None
        inst_or_cls = inst if inst is not None else cls
        if inst_or_cls.requires_age_romance_check:
            allow_romance = True
            if inst is not None:
                actor_sim_info = inst.sim.sim_info
                target_id = tag
                target_sim_info = services.sim_info_manager().get(target_id)
                if target_sim_info.age <= Age.TEEN:
                    allow_romance = False
                second_tag_list = (1,) if not ((actor_sim_info.age <= Age.TEEN and target_sim_info.age >= Age.YOUNGADULT or actor_sim_info.age >= Age.YOUNGADULT) and allow_romance) else None
        return SimPickerRow(sim_id=tag, tag=tag, select_default=select_default, second_tag_list=second_tag_list)

    @flexmethod
    def get_single_choice_and_row(cls, inst, context=None, target=None, **kwargs):
        inst_or_cls = inst if inst is not None else cls
        if context is None:
            return (None, None)
        single_choice = None
        for choice in inst_or_cls._get_valid_sim_choices_gen(target, context, **kwargs):
            if single_choice is not None:
                return (None, None)
            else:
                single_choice = choice
                if single_choice is not None:
                    sim_id = single_choice.sim_info.sim_id
                    row = inst_or_cls.create_row(sim_id)
                    if inst_or_cls.cell_enabled_tests is not None:
                        if inst:
                            interaction_parameters = inst.interaction_parameters.copy()
                        else:
                            interaction_parameters = kwargs.copy()
                        interaction_parameters['picked_item_ids'] = {sim_id}
                        resolver = InteractionResolver(cls, inst, target=target, context=context, **interaction_parameters)
                        result = inst_or_cls.cell_enabled_tests.run_tests(resolver)
                        if not result:
                            row.is_enable = False
                            if result.tooltip is not None:
                                row.row_tooltip = result.tooltip
                    return (single_choice.sim_info, row)
        if single_choice is not None:
            sim_id = single_choice.sim_info.sim_id
            row = inst_or_cls.create_row(sim_id)
            if inst_or_cls.cell_enabled_tests is not None:
                if inst:
                    interaction_parameters = inst.interaction_parameters.copy()
                else:
                    interaction_parameters = kwargs.copy()
                interaction_parameters['picked_item_ids'] = {sim_id}
                resolver = InteractionResolver(cls, inst, target=target, context=context, **interaction_parameters)
                result = inst_or_cls.cell_enabled_tests.run_tests(resolver)
                if not result:
                    row.is_enable = False
                    if result.tooltip is not None:
                        row.row_tooltip = result.tooltip
            return (single_choice.sim_info, row)
        return (None, None)

    @classmethod
    def has_valid_choice(cls, target, context, **kwargs):
        if cls.picker_dialog is not None and cls.picker_dialog.min_selectable == 0 and cls.picker_dialog.min_choices == 0:
            return True
        choice_count = 0
        if cls.create_sim_if_no_valid_choices:
            return True
        for _ in cls._get_valid_sim_choices_gen(target, context, **kwargs):
            if cls.picker_dialog is None:
                return True
            choice_count += 1
            if choice_count >= cls.picker_dialog.min_selectable and choice_count >= cls.picker_dialog.min_choices:
                return True
        return False

    @flexmethod
    def picker_rows_gen(cls, inst, target, context, default_selection=set(), **kwargs):
        inst_or_cls = inst if inst is not None else cls
        interaction_parameters = {}
        resolver = InteractionResolver(cls, inst, target=target, context=context, **interaction_parameters)
        for filter_result in inst_or_cls._get_valid_sim_choices_gen(target, context, **kwargs):
            sim_id = filter_result.sim_info.id
            logger.info('SimPicker: add sim_id:{}', sim_id)
            interaction_parameters['picked_item_ids'] = {sim_id}
            resolver.interaction_parameters = interaction_parameters
            if not inst_or_cls.default_selection_tests is not None or inst_or_cls.default_selection_tests.run_tests(resolver) or sim_id in default_selection:
                select_default = True
            else:
                select_default = False
            row = inst_or_cls.create_row(sim_id, select_default=select_default)
            result = inst_or_cls.cell_enabled_tests.run_tests(resolver)
            row.is_enable = False
            localization_tokens = inst_or_cls.get_localization_tokens(**interaction_parameters)
            row.row_tooltip = lambda *_, result_tooltip=result.tooltip, tokens=localization_tokens: result_tooltip(*tokens)
            yield row

    def _on_picker_selected(self, dialog):
        if dialog.accepted:
            results = dialog.get_result_tags()
            if len(results) >= dialog.min_selectable:
                self._on_successful_picker_selection(results)

    def _on_successful_picker_selection(self, results=()):
        self._apply_loot(results)
        self._push_continuations(results)
        if self.report_picked_count:
            with telemetry_helper.begin_hook(pickerinteraction_telemetry_writer, TELEMETRY_HOOK_INTERACTION_START, sim=self.sim) as hook:
                hook.write_int(TELEMETRY_FIELD_INTERACTION_ID, self.guid64)
                hook.write_int(TELEMETRY_FIELD_PICKED_COUNT, len(results))

    def _set_inventory_carry_target(self):
        if self.carry_item_from_inventory is not None:
            for obj in self.sim.inventory_component:
                if any(obj.definition.has_build_buy_tag(tag) for tag in self.carry_item_from_inventory):
                    self.context.carry_target = obj
                    break

    def _push_continuations(self, *args, **kwargs):
        self._set_inventory_carry_target()
        super()._push_continuations(*args, **kwargs)

    def on_choice_selected(self, choice_tag, **kwargs):
        sim = choice_tag
        if sim is not None:
            self._on_successful_picker_selection(results=(sim,))

class PickerTravelHereSuperInteraction(SimPickerInteraction):
    INSTANCE_TUNABLES = {'get_display_name_from_destination': Tunable(description='\n            If checked then we will attempt to get the Travel With Interaction\n            Name from the venue we are trying to travel to and use that instead\n            of display name.\n            ', tunable_type=bool, default=True, tuning_group=GroupNames.PICKERTUNING)}

    @flexmethod
    def _get_name(cls, inst, target=DEFAULT, context=DEFAULT, **interaction_parameters):
        inst_or_cls = inst if inst is not None else cls
        target = inst_or_cls.target if target is DEFAULT else target
        context = inst_or_cls.context if context is DEFAULT else context
        zone_id = context.pick.get_zone_id_from_pick_location()
        if inst is not None:
            inst.interaction_parameters['picked_zone_ids'] = frozenset({zone_id})
        if inst_or_cls.get_display_name_from_destination:
            venue_instance = get_venue_instance_from_pick_location(context.pick)
            if venue_instance is not None and venue_instance.travel_with_interaction_name is not None:
                return venue_instance.travel_with_interaction_name(target, context)
        return super(__class__, inst_or_cls)._get_name(target=target, context=context, **interaction_parameters)

    @flexmethod
    def _get_valid_sim_choices_gen(cls, inst, target, context, **kwargs):
        zone_id = context.pick.get_zone_id_from_pick_location()
        for filter_result in super()._get_valid_sim_choices_gen(target, context, **kwargs):
            if filter_result.sim_info.zone_id != zone_id:
                yield filter_result

    @flexmethod
    def get_single_choice_and_row(cls, inst, context=None, target=None, **kwargs):
        return (None, None)

    def _on_picker_selected(self, dialog):
        if dialog.accepted:
            results = dialog.get_result_tags()
            self._on_successful_picker_selection(results)

    def _on_successful_picker_selection(self, results=()):
        zone_ids = self.interaction_parameters.get('picked_zone_ids', None)
        if zone_ids is None:
            zone_id = self.context.pick.get_zone_id_from_pick_location()
            zone_ids = frozenset({zone_id})
        zone_datas = []
        for zone_id in zone_ids:
            zone_data = services.get_persistence_service().get_zone_proto_buff(zone_id)
            if zone_data is not None:
                zone_datas.append(zone_data)
        self._push_continuations(results, zone_datas=zone_datas)
lock_instance_tunables(PickerTravelHereSuperInteraction, single_choice_display_name=None)
class AutonomousSimPickerSuperInteraction(SimPickerMixin, AutonomousPickerSuperInteraction):
    INSTANCE_TUNABLES = {'test_compatibility': Tunable(description='\n            If checked then the actor continuation will be tested for\n            interaction compatibility.\n            ', tunable_type=bool, default=False, tuning_group=GroupNames.PICKERTUNING)}

    def __init__(self, *args, choice_enumeration_strategy=None, **kwargs):
        if choice_enumeration_strategy is None:
            choice_enumeration_strategy = SimPickerEnumerationStrategy()
        super().__init__(*args, choice_enumeration_strategy=choice_enumeration_strategy, **kwargs)

    @classmethod
    def _test(cls, target, context, **interaction_parameters):
        if not cls.has_valid_choice(target, context, **interaction_parameters):
            return event_testing.results.TestResult(False, 'This picker SI has no valid choices.')
        return super()._test(target, context, **interaction_parameters)

    def _run_interaction_gen(self, timeline):
        continuation = self.actor_continuation[0]
        affordance = continuation.si_affordance_override if continuation.si_affordance_override is not None else continuation.affordance
        compatibility_func = functools.partial(self.are_affordances_linked, affordance, self.context) if self.test_compatibility else None
        self._choice_enumeration_strategy.build_choice_list(self, self.sim, test_function=compatibility_func)
        chosen_sim = self._choice_enumeration_strategy.find_best_choice(self)
        if chosen_sim is not None:
            chosen_sim = (chosen_sim,)
            self._apply_loot(chosen_sim)
            self._push_continuations(chosen_sim)
        return True

    @classmethod
    def has_valid_choice(cls, target, context, **kwargs):
        continuation = cls.actor_continuation[0]
        affordance = continuation.si_affordance_override if continuation.si_affordance_override is not None else continuation.affordance
        compatibility_func = functools.partial(cls.are_affordances_linked, affordance, context) if cls.test_compatibility else None
        if cls.create_sim_if_no_valid_choices:
            return True
        for _ in cls._get_valid_sim_choices_gen(target, context, test_function=compatibility_func, **kwargs):
            return True
        return False

    @classmethod
    def are_affordances_linked(cls, affordance, context, chosen_sim):
        aop = AffordanceObjectPair(affordance, chosen_sim, affordance, None)
        chosen_sim_si_state = chosen_sim.si_state
        for existing_si in chosen_sim_si_state.all_guaranteed_si_gen(context.priority, group_id=context.group_id):
            if not aop.affordance.is_linked_to(existing_si.affordance):
                return False
        return True

class LotPickerMixin:
    INSTANCE_TUNABLES = {'default_inclusion': TunableVariant(description='\n            This defines which venue types are valid for this picker.\n            ', include_all=TunableTuple(description='\n                This will allow all venue types to be valid, except those blacklisted.\n                ', include_all_by_default=Tunable(bool, True), exclude_venues=TunableList(tunable=TunableReference(manager=services.get_instance_manager(sims4.resources.Types.VENUE), tuning_group=GroupNames.VENUES, pack_safe=True), display_name='Blacklist Items'), exclude_lists=TunableList(TunableVenueListReference(), display_name='Blacklist Lists'), locked_args={'include_all_by_default': True}), exclude_all=TunableTuple(description='\n                This will prevent all venue types from being valid, except those whitelisted.\n                ', include_all_by_default=Tunable(bool, False), include_venues=TunableList(tunable=TunableReference(manager=services.get_instance_manager(sims4.resources.Types.VENUE), tuning_group=GroupNames.VENUES, pack_safe=True), display_name='Whitelist Items'), include_lists=TunableList(TunableVenueListReference(), display_name='Whitelist Lists'), locked_args={'include_all_by_default': False}), default='include_all', tuning_group=GroupNames.PICKERTUNING), 'building_types_excluded': TunableSet(description='\n            A set of building types to exclude for this map view picker. This\n            allows us to do things like exclude apartments or penthouses.\n            ', tunable=TunableEnumEntry(description='\n                The Plex Building Type we want to exclude. Default is standard\n                lots. Fully Contained Plexes are apartments, and Penthouses are\n                regular lots that sit on top of apartment buildings and have a\n                common area.\n                ', tunable_type=PlexBuildingType, default=PlexBuildingType.FULLY_CONTAINED_PLEX, invalid_enums=(PlexBuildingType.INVALID,)), tuning_group=GroupNames.PICKERTUNING), 'include_actor_home_lot': Tunable(description='\n            If checked, the actors home lot will always be included regardless\n            of venue tuning.  If unchecked, it will NEVER be included.\n            ', tunable_type=bool, default=False, tuning_group=GroupNames.PICKERTUNING), 'include_target_home_lot': Tunable(description='\n            If checked, the target(s) home lot will always be included regardless\n            of venue tuning.  If unchecked, it will NEVER be included.\n            ', tunable_type=bool, default=False, tuning_group=GroupNames.PICKERTUNING), 'include_active_lot': Tunable(description='\n            If checked, the active lot may or may not appear based on \n            venue/situation tuning. If not checked, the active lot will always \n            be excluded.\n            ', tunable_type=bool, default=False, tuning_group=GroupNames.PICKERTUNING), 'test_region_compatibility': Tunable(description="\n            If enabled, this picker will filter out regions that are\n            inaccessible from the actor sim's current region.\n            ", tunable_type=bool, default=True, tuning_group=GroupNames.PICKERTUNING), 'exclude_rented_zones': Tunable(description='\n            If enabled, this picker will filter out zones that have already\n            been rented. This should likely be restricted to interactions that\n            are attempting to rent a zone or join a vacation.\n            ', tunable_type=bool, default=False, tuning_group=GroupNames.PICKERTUNING), 'testable_region_inclusion': TunableMapping(description='\n            Mapping of region to tests that should be run to verify if region\n            should be added.\n            ', key_type=TunableReference(manager=services.get_instance_manager(sims4.resources.Types.VENUE), pack_safe=True), value_type=TunableTestSet(description='\n                A series of tests that must pass in order for the region to be\n                available for picking.\n                '), tuning_group=GroupNames.PICKERTUNING)}

    @flexmethod
    def _get_valid_lot_choices(cls, inst, target, context, target_list=None):
        inst_or_cls = inst if inst is not None else cls
        actor = context.sim
        if actor is None:
            return []
        target_zone_ids = []
        actor_zone_id = actor.household.home_zone_id
        results = []
        if target_list is None:
            if target.household is not None:
                target_zone_ids.append(target.household.home_zone_id)
        else:
            sim_info_manager = services.sim_info_manager()
            for target_sim_id in target_list:
                target_sim_info = sim_info_manager.get(target_sim_id)
                if target_sim_info is not None and target_sim_info.household is not None:
                    target_zone_ids.append(target_sim_info.household.home_zone_id)
        venue_manager = services.get_instance_manager(sims4.resources.Types.VENUE)
        active_zone_id = services.current_zone().id
        travel_group_manager = services.travel_group_manager()
        current_region = region.get_region_instance_from_zone_id(actor.zone_id)
        if current_region is None and inst_or_cls.test_region_compatibility:
            logger.error('Could not find region for Sim {}'.format(actor), owner='rmccord')
            return []
        plex_service = services.get_plex_service()
        persistence_service = services.get_persistence_service()
        for zone_data in persistence_service.zone_proto_buffs_gen():
            zone_id = zone_data.zone_id
            if inst_or_cls.include_active_lot or zone_id == active_zone_id:
                pass
            elif inst_or_cls.test_region_compatibility:
                dest_region = region.get_region_instance_from_zone_id(zone_id)
                if not current_region.is_region_compatible(dest_region):
                    pass
                elif inst_or_cls.building_types_excluded and plex_service.get_plex_building_type(zone_id) in inst_or_cls.building_types_excluded:
                    pass
                elif zone_id == actor_zone_id:
                    if inst_or_cls.include_actor_home_lot:
                        results.append(zone_data)
                        if zone_id in target_zone_ids:
                            if inst_or_cls.include_target_home_lot:
                                results.append(zone_data)
                                venue_tuning_id = build_buy.get_current_venue(zone_id)
                                if venue_tuning_id is None:
                                    pass
                                else:
                                    venue_tuning = venue_manager.get(venue_tuning_id)
                                    if venue_tuning is None:
                                        pass
                                    elif inst_or_cls.exclude_rented_zones and venue_tuning.is_vacation_venue and not travel_group_manager.is_zone_rentable(zone_id, venue_tuning):
                                        pass
                                    else:
                                        region_tests = inst_or_cls.testable_region_inclusion.get(venue_tuning)
                                        if region_tests is not None:
                                            resolver = SingleSimResolver(actor.sim_info)
                                            if region_tests.run_tests(resolver):
                                                results.append(zone_data)
                                            else:
                                                default_inclusion = inst_or_cls.default_inclusion
                                                if inst_or_cls.default_inclusion.include_all_by_default:
                                                    if venue_tuning in default_inclusion.exclude_venues:
                                                        pass
                                                    elif any(venue_tuning in venue_list for venue_list in default_inclusion.exclude_lists):
                                                        pass
                                                    else:
                                                        results.append(zone_data)
                                                elif venue_tuning in default_inclusion.include_venues:
                                                    results.append(zone_data)
                                                elif any(venue_tuning in venue_list for venue_list in default_inclusion.include_lists):
                                                    results.append(zone_data)
                                        else:
                                            default_inclusion = inst_or_cls.default_inclusion
                                            if inst_or_cls.default_inclusion.include_all_by_default:
                                                if venue_tuning in default_inclusion.exclude_venues:
                                                    pass
                                                elif any(venue_tuning in venue_list for venue_list in default_inclusion.exclude_lists):
                                                    pass
                                                else:
                                                    results.append(zone_data)
                                            elif venue_tuning in default_inclusion.include_venues:
                                                results.append(zone_data)
                                            elif any(venue_tuning in venue_list for venue_list in default_inclusion.include_lists):
                                                results.append(zone_data)
                        else:
                            venue_tuning_id = build_buy.get_current_venue(zone_id)
                            if venue_tuning_id is None:
                                pass
                            else:
                                venue_tuning = venue_manager.get(venue_tuning_id)
                                if venue_tuning is None:
                                    pass
                                elif inst_or_cls.exclude_rented_zones and venue_tuning.is_vacation_venue and not travel_group_manager.is_zone_rentable(zone_id, venue_tuning):
                                    pass
                                else:
                                    region_tests = inst_or_cls.testable_region_inclusion.get(venue_tuning)
                                    if region_tests is not None:
                                        resolver = SingleSimResolver(actor.sim_info)
                                        if region_tests.run_tests(resolver):
                                            results.append(zone_data)
                                        else:
                                            default_inclusion = inst_or_cls.default_inclusion
                                            if inst_or_cls.default_inclusion.include_all_by_default:
                                                if venue_tuning in default_inclusion.exclude_venues:
                                                    pass
                                                elif any(venue_tuning in venue_list for venue_list in default_inclusion.exclude_lists):
                                                    pass
                                                else:
                                                    results.append(zone_data)
                                            elif venue_tuning in default_inclusion.include_venues:
                                                results.append(zone_data)
                                            elif any(venue_tuning in venue_list for venue_list in default_inclusion.include_lists):
                                                results.append(zone_data)
                                    else:
                                        default_inclusion = inst_or_cls.default_inclusion
                                        if inst_or_cls.default_inclusion.include_all_by_default:
                                            if venue_tuning in default_inclusion.exclude_venues:
                                                pass
                                            elif any(venue_tuning in venue_list for venue_list in default_inclusion.exclude_lists):
                                                pass
                                            else:
                                                results.append(zone_data)
                                        elif venue_tuning in default_inclusion.include_venues:
                                            results.append(zone_data)
                                        elif any(venue_tuning in venue_list for venue_list in default_inclusion.include_lists):
                                            results.append(zone_data)
                elif zone_id in target_zone_ids:
                    if inst_or_cls.include_target_home_lot:
                        results.append(zone_data)
                        venue_tuning_id = build_buy.get_current_venue(zone_id)
                        if venue_tuning_id is None:
                            pass
                        else:
                            venue_tuning = venue_manager.get(venue_tuning_id)
                            if venue_tuning is None:
                                pass
                            elif inst_or_cls.exclude_rented_zones and venue_tuning.is_vacation_venue and not travel_group_manager.is_zone_rentable(zone_id, venue_tuning):
                                pass
                            else:
                                region_tests = inst_or_cls.testable_region_inclusion.get(venue_tuning)
                                if region_tests is not None:
                                    resolver = SingleSimResolver(actor.sim_info)
                                    if region_tests.run_tests(resolver):
                                        results.append(zone_data)
                                    else:
                                        default_inclusion = inst_or_cls.default_inclusion
                                        if inst_or_cls.default_inclusion.include_all_by_default:
                                            if venue_tuning in default_inclusion.exclude_venues:
                                                pass
                                            elif any(venue_tuning in venue_list for venue_list in default_inclusion.exclude_lists):
                                                pass
                                            else:
                                                results.append(zone_data)
                                        elif venue_tuning in default_inclusion.include_venues:
                                            results.append(zone_data)
                                        elif any(venue_tuning in venue_list for venue_list in default_inclusion.include_lists):
                                            results.append(zone_data)
                                else:
                                    default_inclusion = inst_or_cls.default_inclusion
                                    if inst_or_cls.default_inclusion.include_all_by_default:
                                        if venue_tuning in default_inclusion.exclude_venues:
                                            pass
                                        elif any(venue_tuning in venue_list for venue_list in default_inclusion.exclude_lists):
                                            pass
                                        else:
                                            results.append(zone_data)
                                    elif venue_tuning in default_inclusion.include_venues:
                                        results.append(zone_data)
                                    elif any(venue_tuning in venue_list for venue_list in default_inclusion.include_lists):
                                        results.append(zone_data)
                else:
                    venue_tuning_id = build_buy.get_current_venue(zone_id)
                    if venue_tuning_id is None:
                        pass
                    else:
                        venue_tuning = venue_manager.get(venue_tuning_id)
                        if venue_tuning is None:
                            pass
                        elif inst_or_cls.exclude_rented_zones and venue_tuning.is_vacation_venue and not travel_group_manager.is_zone_rentable(zone_id, venue_tuning):
                            pass
                        else:
                            region_tests = inst_or_cls.testable_region_inclusion.get(venue_tuning)
                            if region_tests is not None:
                                resolver = SingleSimResolver(actor.sim_info)
                                if region_tests.run_tests(resolver):
                                    results.append(zone_data)
                                else:
                                    default_inclusion = inst_or_cls.default_inclusion
                                    if inst_or_cls.default_inclusion.include_all_by_default:
                                        if venue_tuning in default_inclusion.exclude_venues:
                                            pass
                                        elif any(venue_tuning in venue_list for venue_list in default_inclusion.exclude_lists):
                                            pass
                                        else:
                                            results.append(zone_data)
                                    elif venue_tuning in default_inclusion.include_venues:
                                        results.append(zone_data)
                                    elif any(venue_tuning in venue_list for venue_list in default_inclusion.include_lists):
                                        results.append(zone_data)
                            else:
                                default_inclusion = inst_or_cls.default_inclusion
                                if inst_or_cls.default_inclusion.include_all_by_default:
                                    if venue_tuning in default_inclusion.exclude_venues:
                                        pass
                                    elif any(venue_tuning in venue_list for venue_list in default_inclusion.exclude_lists):
                                        pass
                                    else:
                                        results.append(zone_data)
                                elif venue_tuning in default_inclusion.include_venues:
                                    results.append(zone_data)
                                elif any(venue_tuning in venue_list for venue_list in default_inclusion.include_lists):
                                    results.append(zone_data)
            elif inst_or_cls.building_types_excluded and plex_service.get_plex_building_type(zone_id) in inst_or_cls.building_types_excluded:
                pass
            elif zone_id == actor_zone_id:
                if inst_or_cls.include_actor_home_lot:
                    results.append(zone_data)
                    if zone_id in target_zone_ids:
                        if inst_or_cls.include_target_home_lot:
                            results.append(zone_data)
                            venue_tuning_id = build_buy.get_current_venue(zone_id)
                            if venue_tuning_id is None:
                                pass
                            else:
                                venue_tuning = venue_manager.get(venue_tuning_id)
                                if venue_tuning is None:
                                    pass
                                elif inst_or_cls.exclude_rented_zones and venue_tuning.is_vacation_venue and not travel_group_manager.is_zone_rentable(zone_id, venue_tuning):
                                    pass
                                else:
                                    region_tests = inst_or_cls.testable_region_inclusion.get(venue_tuning)
                                    if region_tests is not None:
                                        resolver = SingleSimResolver(actor.sim_info)
                                        if region_tests.run_tests(resolver):
                                            results.append(zone_data)
                                        else:
                                            default_inclusion = inst_or_cls.default_inclusion
                                            if inst_or_cls.default_inclusion.include_all_by_default:
                                                if venue_tuning in default_inclusion.exclude_venues:
                                                    pass
                                                elif any(venue_tuning in venue_list for venue_list in default_inclusion.exclude_lists):
                                                    pass
                                                else:
                                                    results.append(zone_data)
                                            elif venue_tuning in default_inclusion.include_venues:
                                                results.append(zone_data)
                                            elif any(venue_tuning in venue_list for venue_list in default_inclusion.include_lists):
                                                results.append(zone_data)
                                    else:
                                        default_inclusion = inst_or_cls.default_inclusion
                                        if inst_or_cls.default_inclusion.include_all_by_default:
                                            if venue_tuning in default_inclusion.exclude_venues:
                                                pass
                                            elif any(venue_tuning in venue_list for venue_list in default_inclusion.exclude_lists):
                                                pass
                                            else:
                                                results.append(zone_data)
                                        elif venue_tuning in default_inclusion.include_venues:
                                            results.append(zone_data)
                                        elif any(venue_tuning in venue_list for venue_list in default_inclusion.include_lists):
                                            results.append(zone_data)
                    else:
                        venue_tuning_id = build_buy.get_current_venue(zone_id)
                        if venue_tuning_id is None:
                            pass
                        else:
                            venue_tuning = venue_manager.get(venue_tuning_id)
                            if venue_tuning is None:
                                pass
                            elif inst_or_cls.exclude_rented_zones and venue_tuning.is_vacation_venue and not travel_group_manager.is_zone_rentable(zone_id, venue_tuning):
                                pass
                            else:
                                region_tests = inst_or_cls.testable_region_inclusion.get(venue_tuning)
                                if region_tests is not None:
                                    resolver = SingleSimResolver(actor.sim_info)
                                    if region_tests.run_tests(resolver):
                                        results.append(zone_data)
                                    else:
                                        default_inclusion = inst_or_cls.default_inclusion
                                        if inst_or_cls.default_inclusion.include_all_by_default:
                                            if venue_tuning in default_inclusion.exclude_venues:
                                                pass
                                            elif any(venue_tuning in venue_list for venue_list in default_inclusion.exclude_lists):
                                                pass
                                            else:
                                                results.append(zone_data)
                                        elif venue_tuning in default_inclusion.include_venues:
                                            results.append(zone_data)
                                        elif any(venue_tuning in venue_list for venue_list in default_inclusion.include_lists):
                                            results.append(zone_data)
                                else:
                                    default_inclusion = inst_or_cls.default_inclusion
                                    if inst_or_cls.default_inclusion.include_all_by_default:
                                        if venue_tuning in default_inclusion.exclude_venues:
                                            pass
                                        elif any(venue_tuning in venue_list for venue_list in default_inclusion.exclude_lists):
                                            pass
                                        else:
                                            results.append(zone_data)
                                    elif venue_tuning in default_inclusion.include_venues:
                                        results.append(zone_data)
                                    elif any(venue_tuning in venue_list for venue_list in default_inclusion.include_lists):
                                        results.append(zone_data)
            elif zone_id in target_zone_ids:
                if inst_or_cls.include_target_home_lot:
                    results.append(zone_data)
                    venue_tuning_id = build_buy.get_current_venue(zone_id)
                    if venue_tuning_id is None:
                        pass
                    else:
                        venue_tuning = venue_manager.get(venue_tuning_id)
                        if venue_tuning is None:
                            pass
                        elif inst_or_cls.exclude_rented_zones and venue_tuning.is_vacation_venue and not travel_group_manager.is_zone_rentable(zone_id, venue_tuning):
                            pass
                        else:
                            region_tests = inst_or_cls.testable_region_inclusion.get(venue_tuning)
                            if region_tests is not None:
                                resolver = SingleSimResolver(actor.sim_info)
                                if region_tests.run_tests(resolver):
                                    results.append(zone_data)
                                else:
                                    default_inclusion = inst_or_cls.default_inclusion
                                    if inst_or_cls.default_inclusion.include_all_by_default:
                                        if venue_tuning in default_inclusion.exclude_venues:
                                            pass
                                        elif any(venue_tuning in venue_list for venue_list in default_inclusion.exclude_lists):
                                            pass
                                        else:
                                            results.append(zone_data)
                                    elif venue_tuning in default_inclusion.include_venues:
                                        results.append(zone_data)
                                    elif any(venue_tuning in venue_list for venue_list in default_inclusion.include_lists):
                                        results.append(zone_data)
                            else:
                                default_inclusion = inst_or_cls.default_inclusion
                                if inst_or_cls.default_inclusion.include_all_by_default:
                                    if venue_tuning in default_inclusion.exclude_venues:
                                        pass
                                    elif any(venue_tuning in venue_list for venue_list in default_inclusion.exclude_lists):
                                        pass
                                    else:
                                        results.append(zone_data)
                                elif venue_tuning in default_inclusion.include_venues:
                                    results.append(zone_data)
                                elif any(venue_tuning in venue_list for venue_list in default_inclusion.include_lists):
                                    results.append(zone_data)
            else:
                venue_tuning_id = build_buy.get_current_venue(zone_id)
                if venue_tuning_id is None:
                    pass
                else:
                    venue_tuning = venue_manager.get(venue_tuning_id)
                    if venue_tuning is None:
                        pass
                    elif inst_or_cls.exclude_rented_zones and venue_tuning.is_vacation_venue and not travel_group_manager.is_zone_rentable(zone_id, venue_tuning):
                        pass
                    else:
                        region_tests = inst_or_cls.testable_region_inclusion.get(venue_tuning)
                        if region_tests is not None:
                            resolver = SingleSimResolver(actor.sim_info)
                            if region_tests.run_tests(resolver):
                                results.append(zone_data)
                            else:
                                default_inclusion = inst_or_cls.default_inclusion
                                if inst_or_cls.default_inclusion.include_all_by_default:
                                    if venue_tuning in default_inclusion.exclude_venues:
                                        pass
                                    elif any(venue_tuning in venue_list for venue_list in default_inclusion.exclude_lists):
                                        pass
                                    else:
                                        results.append(zone_data)
                                elif venue_tuning in default_inclusion.include_venues:
                                    results.append(zone_data)
                                elif any(venue_tuning in venue_list for venue_list in default_inclusion.include_lists):
                                    results.append(zone_data)
                        else:
                            default_inclusion = inst_or_cls.default_inclusion
                            if inst_or_cls.default_inclusion.include_all_by_default:
                                if venue_tuning in default_inclusion.exclude_venues:
                                    pass
                                elif any(venue_tuning in venue_list for venue_list in default_inclusion.exclude_lists):
                                    pass
                                else:
                                    results.append(zone_data)
                            elif venue_tuning in default_inclusion.include_venues:
                                results.append(zone_data)
                            elif any(venue_tuning in venue_list for venue_list in default_inclusion.include_lists):
                                results.append(zone_data)
        return results

class MapViewPickerInteraction(LotPickerMixin, PickerSuperInteraction):
    INSTANCE_TUNABLES = {'picker_dialog': TunablePickerDialogVariant(description='\n            The object picker dialog.\n            ', available_picker_flags=ObjectPickerTuningFlags.MAP_VIEW, tuning_group=GroupNames.PICKERTUNING, dialog_locked_args={'text_cancel': None, 'text_ok': None, 'title': None, 'text': None, 'text_tokens': DEFAULT, 'icon': None, 'secondary_icon': None, 'phone_ring_type': PhoneRingType.NO_RING}), 'actor_continuation': TunableContinuation(description='\n            If specified, a continuation to push on the actor when a picker \n            selection has been made.\n            ', locked_args={'actor': ParticipantType.Actor}, tuning_group=GroupNames.PICKERTUNING), 'target_continuation': TunableContinuation(description='\n            If specified, a continuation to push on the sim targetted', tuning_group=GroupNames.PICKERTUNING), 'bypass_picker_on_single_choice': Tunable(description='\n            If this is checked, bypass the picker if only one option is available.\n            ', tunable_type=bool, default=False, tuning_group=GroupNames.PICKERTUNING)}

    def _push_continuations(self, zone_datas):
        if not self.target_continuation:
            insert_strategy = QueueInsertStrategy.LAST
        else:
            insert_strategy = QueueInsertStrategy.NEXT
        try:
            picked_zone_set = {zone_data.zone_id for zone_data in zone_datas if zone_data is not None}
        except TypeError:
            picked_zone_set = {zone_datas.zone_id}
        self.interaction_parameters['picked_zone_ids'] = frozenset(picked_zone_set)
        if self.actor_continuation:
            self.push_tunable_continuation(self.actor_continuation, insert_strategy=insert_strategy, picked_zone_ids=picked_zone_set)
        if self.target_continuation:
            self.push_tunable_continuation(self.target_continuation, insert_strategy=insert_strategy, actor=self.target, picked_zone_ids=picked_zone_set)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, choice_enumeration_strategy=LotPickerEnumerationStrategy(), **kwargs)

    def _create_dialog(self, owner, target_sim=None, target=None, **kwargs):
        traveling_sims = []
        picked_sims = self.get_participants(ParticipantType.PickedSim)
        if picked_sims:
            traveling_sims = list(picked_sims)
        elif target is not None and target.is_sim and target is not self.sim:
            traveling_sims.append(target)
        dialog = self.picker_dialog(owner, title=lambda *_, **__: self.get_name(), resolver=self.get_resolver(), traveling_sims=traveling_sims)
        self._setup_dialog(dialog, **kwargs)
        dialog.set_target_sim(target_sim)
        dialog.set_target(target)
        dialog.add_listener(self._on_picker_selected)
        return dialog

    def _run_interaction_gen(self, timeline):
        choices = self._get_valid_lot_choices(self.target, self.context)
        if self.bypass_picker_on_single_choice and len(choices) == 1:
            self._push_continuations(choices[0])
            return True
        self._show_picker_dialog(self.sim, target_sim=self.sim, target=self.target)
        return True

    @flexmethod
    def create_row(cls, inst, tag):
        return LotPickerRow(zone_data=tag, option_id=tag.zone_id, tag=tag)

    @classmethod
    def has_valid_choice(cls, target, context, **kwargs):
        if cls._get_valid_lot_choices(target, context):
            return True
        return False

    @flexmethod
    def picker_rows_gen(cls, inst, target, context, **kwargs):
        inst_or_cls = inst if inst is not None else cls
        for filter_result in inst_or_cls._get_valid_lot_choices(target, context):
            logger.info('LotPicker: add zone_data:{}', filter_result)
            yield LotPickerRow(zone_data=filter_result, option_id=filter_result.zone_id, tag=filter_result)

    def _on_picker_selected(self, dialog):
        results = dialog.get_result_tags()
        if results:
            self._push_continuations(results)

    def on_choice_selected(self, choice_tag, **kwargs):
        result = choice_tag
        if result is not None:
            self._push_continuations(result)

class ObjectPickerMixin:
    INSTANCE_TUNABLES = {'continuation': OptionalTunable(description='\n            If enabled, you can tune a continuation to be pushed.\n            PickedObject will be the object that was selected\n            ', tunable=TunableContinuation(description='\n                If specified, a continuation to push on the chosen object.'), tuning_group=GroupNames.PICKERTUNING), 'single_push_continuation': Tunable(description='\n            If enabled, only the first continuation that can be successfully\n            pushed will run. Otherwise, all continuations are pushed such that\n            they run in order.\n            ', tunable_type=bool, default=False, tuning_group=GroupNames.PICKERTUNING), 'order_by_proximity': OptionalTunable(description='\n            If order_by_proximity is enabled, we find the nearest object to this tuned participant.\n            ', tunable=TunableEnumEntry(tunable_type=ParticipantTypeSingle, default=ParticipantTypeSingle.Actor), tuning_group=GroupNames.PICKERTUNING)}

    @flexmethod
    def _get_objects_gen(cls, inst, target, context, **kwargs):
        raise NotImplementedError

    @classmethod
    def has_valid_choice(cls, target, context, **kwargs):
        for _ in cls._get_objects_gen(target, context):
            return True
        return False

    def _push_continuation(self, obj):
        if obj is not None and self.continuation is not None:
            picked_item_set = set()
            if isinstance(obj, int):
                picked_item_set.add(obj)
            else:
                picked_item_set.add(obj.id)
            self._push_picked_continuation(picked_item_set)

    def _push_continuations(self, objs):
        if objs is not None and self.continuation is not None:
            picked_item_set = set()
            for obj in objs:
                picked_item_set.add(obj.id)
            self._push_picked_continuation(picked_item_set)

    def _push_picked_continuation(self, picked_items):
        self.interaction_parameters['picked_item_ids'] = picked_items
        self.push_tunable_continuation(self.continuation, multi_push=not self.single_push_continuation, picked_item_ids=picked_items, insert_strategy=QueueInsertStrategy.LAST)

    @flexmethod
    def _test_continuation_for_object(cls, inst, object_id, gsi_affordance_results=None, context=DEFAULT, target=DEFAULT):
        inst_or_cls = inst if inst is not None else cls
        picked_item_set = {object_id}
        result = event_testing.results.TestResult.TRUE
        resolver = inst_or_cls.get_resolver(target=target, context=context, picked_object=target, picked_item_ids=picked_item_set)
        for continuation in inst_or_cls.continuation:
            local_actors = resolver.get_participants(continuation.actor)
            for local_actor in local_actors:
                if isinstance(local_actor, sims.sim_info.SimInfo):
                    local_actor = local_actor.get_sim_instance()
                    if local_actor is None:
                        result = event_testing.results.TestResult(False, "Actor isn't instantiated")
                    else:
                        local_context = context.clone_for_sim(local_actor)
                        if continuation.carry_target is not None:
                            local_context.carry_target = resolver.get_participant(continuation.carry_target)
                        if continuation.target != ParticipantType.Invalid:
                            local_targets = resolver.get_participants(continuation.target)
                            local_target = next(iter(local_targets), None)
                        else:
                            local_target = None
                        if local_target.is_sim:
                            if isinstance(local_target, sims.sim_info.SimInfo):
                                local_target = local_target.get_sim_instance()
                        elif local_target.is_part:
                            local_target = local_target.part_owner
                        affordance = continuation.affordance
                        if local_target is not None and affordance.is_super:
                            result = local_actor.test_super_affordance(affordance, local_target, local_context, picked_object=target, picked_item_ids=picked_item_set)
                        else:
                            if continuation.si_affordance_override is not None:
                                super_affordance = continuation.si_affordance_override
                                super_interaction = None
                                push_super_on_prepare = True
                            else:
                                logger.error("Picker interaction doesn't have affordance override set for continuation", owner='nbaker')
                            aop = AffordanceObjectPair(affordance, local_target, super_affordance, super_interaction, picked_object=target, push_super_on_prepare=push_super_on_prepare, picked_item_ids=picked_item_set)
                            result = aop.test(local_context)
                        if gsi_affordance_results is not None:
                            gsi_affordance_results.append((result, affordance.get_name))
                        if result:
                            return result
                else:
                    local_context = context.clone_for_sim(local_actor)
                    if continuation.carry_target is not None:
                        local_context.carry_target = resolver.get_participant(continuation.carry_target)
                    if continuation.target != ParticipantType.Invalid:
                        local_targets = resolver.get_participants(continuation.target)
                        local_target = next(iter(local_targets), None)
                    else:
                        local_target = None
                    if local_target.is_sim:
                        if isinstance(local_target, sims.sim_info.SimInfo):
                            local_target = local_target.get_sim_instance()
                    elif local_target.is_part:
                        local_target = local_target.part_owner
                    affordance = continuation.affordance
                    if local_target is not None and affordance.is_super:
                        result = local_actor.test_super_affordance(affordance, local_target, local_context, picked_object=target, picked_item_ids=picked_item_set)
                    else:
                        if continuation.si_affordance_override is not None:
                            super_affordance = continuation.si_affordance_override
                            super_interaction = None
                            push_super_on_prepare = True
                        else:
                            logger.error("Picker interaction doesn't have affordance override set for continuation", owner='nbaker')
                        aop = AffordanceObjectPair(affordance, local_target, super_affordance, super_interaction, picked_object=target, push_super_on_prepare=push_super_on_prepare, picked_item_ids=picked_item_set)
                        result = aop.test(local_context)
                    if gsi_affordance_results is not None:
                        gsi_affordance_results.append((result, affordance.get_name))
                    if result:
                        return result
        return result

    @flexmethod
    def _test_continuation(cls, inst, row_data, **kwargs):
        inst_or_cls = inst if inst is not None else cls
        if inst_or_cls.continuation is None:
            return
        if not row_data.object_id:
            return
        result = inst_or_cls._test_continuation_for_object(row_data.object_id, **kwargs)
        if not result:
            row_data.is_enable = False
            row_data.row_tooltip = result.tooltip

class ObjectPickerInteraction(ObjectPickerMixin, PickerSingleChoiceSuperInteraction):
    INSTANCE_SUBCLASSES_ONLY = True

    class _DescriptionFromTooltip(HasTunableSingletonFactory, AutoFactoryInit):
        FACTORY_TUNABLES = {'field': TunableEnumEntry(description='\n                Use an existing field from the tooltip component\n                ', tunable_type=TooltipFields, default=TooltipFields.recipe_description)}

        def get_description(self, row_object, context=None, target=None, **kwargs):
            return row_object.get_tooltip_field(self.field, context=context, target=target)

    class _DescriptionFromText(HasTunableSingletonFactory, AutoFactoryInit):
        FACTORY_TUNABLES = {'text': TunableLocalizedStringFactoryVariant(description='\n                Text that will be displayed as the objects description.\n                '), 'text_tokens': OptionalTunable(description="\n                If enabled, localization tokens to be passed into 'text' can be\n                explicitly defined. For example, you could use a participant that is\n                not normally used, such as a owned sim. Or you could also\n                pass in statistic and commodity values.\n                \n                Participants tuned here should only be relevant to objects.  If \n                you try to tune a participant which only exist when you run an \n                interaction (e.g. carry_target) tooltip wont show anything.\n                ", tunable=LocalizationTokens.TunableFactory())}

        def get_description(self, row_object, **kwargs):
            resolver = SingleObjectResolver(row_object)
            if self.text_tokens is not None:
                tokens = self.text_tokens.get_tokens(resolver)
            else:
                tokens = ()
            return self.text(*tokens)

    class _DescriptionFromGameplayObjectPreferenceType(HasTunableSingletonFactory, AutoFactoryInit):
        FACTORY_TUNABLES = {'participant_type': TunableEnumEntry(description='\n                What kind of participant we expect the gameplay object preference to come from.\n                ', tunable_type=ParticipantType, default=ParticipantType.Object)}

        def get_description(self, row_object:'Definition', interaction:'base_interactions'=None, **kwargs):
            object_name = LocalizationHelperTuning.get_object_name(row_object)
            if interaction is not None:
                target = interaction.get_participant(participant_type=self.participant_type)
                if target is not None and target.sim_info is not None:
                    trait_tracker = target.sim_info.trait_tracker
                    if trait_tracker is not None:
                        object_name = LocalizationHelperTuning.NAME_VALUE_PARENTHESIS_PAIR_STRUCTURE(object_name, trait_tracker.get_gameplay_object_preference_type_from_object_as_string(row_object))
            else:
                logger.error('{} does not have proper tuning. Please check Object Name Override.', object_name)
            return object_name

    class _DescriptionFromFishingBait(HasTunableSingletonFactory, AutoFactoryInit):

        def get_description(self, row_object, context=None, target=None, **kwargs):
            return FishingTuning.get_fishing_bait_description(row_object)

    INSTANCE_TUNABLES = {'picker_dialog': TunablePickerDialogVariant(description='\n            The object picker dialog.\n            ', available_picker_flags=ObjectPickerTuningFlags.OBJECT, tuning_group=GroupNames.PICKERTUNING), 'auto_pick': AutoPick(description='\n            If enabled, this interaction will pick one of the choices\n            available and push the continuation on it. It will be like the\n            interaction was run autonomously - no picker dialog will show up.\n            ', tuning_group=GroupNames.PICKERTUNING), 'fallback_description': OptionalTunable(description='\n            The fallback description if there is no recipe or custom description.\n            If disabled, (or referencing an unused tooltip field) The final\n            fallback is the catalog description.\n            ', tunable=TunableVariant(description='\n                Types of fallback descriptions\n                ', from_tooltip=_DescriptionFromTooltip.TunableFactory(), from_text=_DescriptionFromText.TunableFactory(), from_fishing_bait=_DescriptionFromFishingBait.TunableFactory(), default='from_tooltip'), tuning_group=GroupNames.PICKERTUNING, enabled_by_default=True), 'object_name_override': OptionalTunable(description='\n            If enabled, we override object name (row name) from either tooltip field or Loc text\n            ', tunable=TunableVariant(description='\n                Sources of object name override.\n                ', from_tooltip=_DescriptionFromTooltip.TunableFactory(), from_text=_DescriptionFromText.TunableFactory(), from_gameplay_object_preference_type=_DescriptionFromGameplayObjectPreferenceType.TunableFactory(), default='from_tooltip'), tuning_group=GroupNames.PICKERTUNING), 'show_rarity': Tunable(description='\n            If checked, the rarity will also be shown in the object picker. If\n            there is no object rarity for this object, nothing will be shown.\n            ', tunable_type=bool, default=False, tuning_group=GroupNames.PICKERTUNING)}

    @flexmethod
    def _use_ellipsized_name(cls, inst):
        inst_or_cls = inst if inst is not None else cls
        return not inst_or_cls.auto_pick

    @flexmethod
    def create_row(cls, inst, row_obj, context=DEFAULT, target=DEFAULT, is_selected=False):
        name = None
        row_description = None
        icon = None
        icon_info = row_obj.get_icon_info_data()
        inst_or_cls = inst if inst is not None else cls
        object_name_override = inst_or_cls.object_name_override
        if row_obj.has_custom_name() and row_obj.animalobject_component is None:
            name = LocalizationHelperTuning.get_raw_text(row_obj.custom_name)
        elif row_obj.crafting_component is not None:
            crafting_process = row_obj.get_crafting_process()
            recipe = crafting_process.recipe
            name = recipe.get_recipe_name(crafting_process.crafter) if object_name_override is None else object_name_override.get_description(row_obj, context=context, target=target)
            row_description = recipe.recipe_description(crafting_process.crafter)
            icon = recipe.icon_override
        elif row_obj.animalobject_component is not None:
            if row_obj.has_custom_name():
                name = LocalizationHelperTuning.get_raw_text(row_obj.custom_name)
            else:
                name = LocalizationHelperTuning.get_object_name(row_obj)
            animal_service = services.animal_service()
            animal_home = animal_service.get_animal_home_obj(row_obj)
            if animal_home is not None:
                if animal_home.has_custom_name():
                    row_description = LocalizationHelperTuning.get_raw_text(animal_home.custom_name)
                else:
                    row_description = LocalizationHelperTuning.get_object_name(animal_home)
        elif object_name_override is not None:
            name = object_name_override.get_description(row_obj, context=context, target=target, interaction=inst_or_cls)
        if row_description is None:
            if row_obj.has_custom_description():
                row_description = LocalizationHelperTuning.get_raw_text(row_obj.custom_description)
            elif inst_or_cls.fallback_description is not None:
                row_description = inst_or_cls.fallback_description.get_description(row_obj, context=context, target=target)
        rarity_text = row_obj.get_object_rarity_string() if inst_or_cls.show_rarity else None
        tag_list = build_buy.get_object_all_tags(row_obj.definition.id)
        row = ObjectPickerRow(object_id=row_obj.id, name=name, row_description=row_description, icon=icon, def_id=row_obj.definition.id, count=inst_or_cls.get_stack_count(row_obj), icon_info=icon_info, tag_list=tag_list, tag=row_obj, rarity_text=rarity_text, is_selected=is_selected)
        inst_or_cls._test_continuation(row, context=context, target=target)
        return row

    @flexmethod
    def get_single_choice_and_row(cls, inst, context=DEFAULT, target=DEFAULT, **kwargs):
        inst_or_cls = inst if inst is not None else cls
        first_obj = None
        first_row = None
        for obj in inst_or_cls._get_objects_gen(target, context):
            if first_obj is not None and first_row is not None:
                return (None, None)
            row = inst_or_cls.create_row(obj, context=context, target=target)
            first_obj = obj
            first_row = row
        return (first_obj, first_row)

    @flexmethod
    def get_stack_count(cls, inst, obj):
        return obj.stack_count()

    def _run_interaction_gen(self, timeline):
        if self.context.source != InteractionContext.SOURCE_PIE_MENU or self.auto_pick:
            choices = list(self._get_objects_gen(self.target, self.context))
            if choices:
                if self.auto_pick:
                    obj = self.auto_pick.perform_auto_pick(choices)
                else:
                    obj = AutoPickRandom.perform_auto_pick(choices)
                self._push_continuation(obj)
                return True
            return False
        picked_row = self.interaction_parameters.get('picked_row')
        choices = () if picked_row is None else (picked_row.tag,)
        self._show_picker_dialog(self.sim, target_sim=self.sim, target=self.target, choices=choices)
        return True

    def _get_id_from_choice(self, choice):
        return choice.id

    @classmethod
    def _get_id_from_row_tag(cls, tag):
        return tag.id

    @classmethod
    def has_valid_choice(cls, target, context, **kwargs):
        obj_count = 0
        for _ in cls._get_objects_gen(target, context):
            obj_count += 1
            if cls.picker_dialog:
                if obj_count >= cls.picker_dialog.min_selectable:
                    return True
            return True
        return False

    @flexmethod
    def picker_rows_gen(cls, inst, target, context, **kwargs):
        inst_or_cls = inst if inst is not None else cls
        for obj in inst_or_cls._get_objects_gen(target, context):
            row = inst_or_cls.create_row(obj, context=context, target=target)
            yield row

    def on_choice_selected(self, choice_tag, **kwargs):
        obj = choice_tag
        if obj is not None:
            self._push_continuation(obj)

    def on_multi_choice_selected(self, choice_tags, **kwargs):
        if choice_tags is not None:
            self._push_continuations(choice_tags)

    def _get_current_selected_count(self):
        target = self.target
        animal_service = services.animal_service()
        if target is not None and animal_service is not None and animal_service.is_registered_home(target.id):
            return animal_service.get_current_occupancy(target.id)
        else:
            return super()._get_current_selected_count()

class AutonomousObjectPickerInteraction(ObjectPickerMixin, AutonomousPickerSuperInteraction):
    INSTANCE_SUBCLASSES_ONLY = True
    LOCKOUT_STR = 'lockout'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, choice_enumeration_strategy=ObjectPickerEnumerationStrategy(), **kwargs)

    @classmethod
    def _test(cls, target, context, **interaction_parameters):
        if not cls.has_valid_choice(target, context, **interaction_parameters):
            return event_testing.results.TestResult(False, 'This picker SI has no valid choices.')
        return super()._test(target, context, **interaction_parameters)

    @flexmethod
    def _get_objects_gen(cls, inst, target, context, **kwargs):
        inst_or_cls = inst if inst is not None else cls
        sim = inst.sim if inst is not None else context.sim
        for obj in inst_or_cls._get_objects_internal_gen(target, context, **kwargs):
            if sim.has_lockout(obj):
                pass
            elif not inst_or_cls._test_continuation_for_object(obj.id, context=context, target=target, **kwargs):
                pass
            else:
                yield obj

    @flexmethod
    def _get_objects_with_results_gen(cls, inst, target, context, **kwargs):
        inst_or_cls = inst if inst is not None else cls
        sim = inst.sim if inst is not None else context.sim
        for obj in inst_or_cls._get_objects_internal_gen(target, context, **kwargs):
            if sim.has_lockout(obj):
                yield (obj, cls.LOCKOUT_STR)
            gsi_results = []
            inst_or_cls._test_continuation_for_object(obj.id, gsi_affordance_results=gsi_results, context=context, target=target, **kwargs)
            yield (obj, gsi_results)

    @flexmethod
    def _get_objects_internal_gen(cls, inst, *args, **kwargs):
        raise NotImplementedError

    def _run_interaction_gen(self, timeline):
        gsi_enabled = gsi_handlers.picker_handler.picker_log_archiver.enabled
        self._choice_enumeration_strategy.build_choice_list(self, self.sim, get_all=gsi_enabled)
        chosen_obj = self._choice_enumeration_strategy.find_best_choice(self)
        if chosen_obj is not None:
            self._push_continuation(chosen_obj)
            if gsi_enabled:
                gen_objects = self._choice_enumeration_strategy.get_gen_objects()
                gsi_handlers.picker_handler.archive_picker_message(self.interaction, self._sim, self._target, chosen_obj, gen_objects)
        return True

class ActorsUrnstonePickerMixin:

    @flexmethod
    def _get_objects_gen(cls, inst, target, context, **kwargs):
        yield sims.ghost.Ghost.get_urnstone_for_sim_id(context.sim.sim_id)

class DuplicateObjectsSuppressionType(enum.Int):
    BY_DEFINITION_ID = 0
    BY_STACK_ID = 1
    BY_DEFINITION_ID_AND_STACK_ID = 2

class ObjectInInventoryPickerMixin:
    INSTANCE_TUNABLES = {'inventory_subject': TunableEnumEntry(description='\n            Subject on which the inventory exists.\n            ', tunable_type=ParticipantType, default=ParticipantType.Actor, tuning_group=GroupNames.PICKERTUNING), 'inventory_item_test': TunableVariant(default='object', description='\n                A test to run on the objects in the inventory to determine\n                which objects will show up in the picker. An object test type\n                left un-tuned is considered any object.\n                ', object=ObjectTypeFactory.TunableFactory(), tag_set=ObjectTagFactory.TunableFactory(), tuning_group=GroupNames.PICKERTUNING), 'additional_item_test': TunableTestSet(description='\n            A set of tests to run on each object in the inventory that passes the\n            inventory_item_test. Each object must pass first the inventory_item_test\n            and then the additional_item_test before it will be shown in the picker dialog.\n            Only tests with ParticipantType.Object will work\n            ', tuning_group=GroupNames.PICKERTUNING), 'suppress_duplicate_objects': OptionalTunable(description='\n            If checked, only a single copy of objects with the same definition/stack id\n            will be shown.\n            ', tunable=TunableEnumEntry(description='\n                Objects can be suppressed by different ways.\n                ', tunable_type=DuplicateObjectsSuppressionType, default=DuplicateObjectsSuppressionType.BY_DEFINITION_ID), tuning_group=GroupNames.PICKERTUNING), 'hidden_inventory_test': TunableEnumEntry(description='\n            Optionally restrict picker objects to only hidden or non-hidden \n            inventories.\n            \n            If set to "Any", objects in both the hidden inventory and non\n            hidden inventory will be considered when populating the picker. \n            ', tunable_type=InventoryTest.TestHiddenInventories, default=InventoryTest.TestHiddenInventories.ANY, tuning_group=GroupNames.PICKERTUNING)}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._stack_key_stack_counts = None
        self._stack_key_objects = None
        self._non_stacked_objects = None

    def _setup_dialog(self, dialog, **kwargs):
        super()._setup_dialog(dialog, **kwargs)

    @classmethod
    def _get_stack_key_for_object(cls, obj):
        key = None
        if obj.inventoryitem_component is not None:
            if cls.suppress_duplicate_objects == DuplicateObjectsSuppressionType.BY_STACK_ID:
                key = obj.inventoryitem_component.get_stack_id()
            elif cls.suppress_duplicate_objects == DuplicateObjectsSuppressionType.BY_DEFINITION_ID_AND_STACK_ID:
                key = (obj.inventoryitem_component.get_stack_id(), obj.definition.id)
        if cls.suppress_duplicate_objects is not None and key is None:
            key = obj.definition.id
        return key

    @flexmethod
    def _get_objects_internal_gen(cls, inst, target, context, **kwargs):
        inst_or_cls = inst if inst is not None else cls
        subject = inst_or_cls.get_participant(participant_type=inst_or_cls.inventory_subject, sim=context.sim, target=target, **kwargs)
        if subject is None:
            return
        actor_sim = inst_or_cls.get_participant(participant_type=ParticipantType.Actor, sim=context.sim, target=target, **kwargs)
        actor_sim_info = actor_sim.sim_info if actor_sim is not None else None
        target_sim = inst_or_cls.get_participant(participant_type=ParticipantType.TargetSim, sim=context.sim, target=target, **kwargs)
        target_sim_info = target_sim.sim_info if target_sim is not None else None
        stack_key_stack_counts = defaultdict(int)
        stack_key_objects = defaultdict(list)
        non_stacked_objects = list()
        inst._stack_key_stack_counts = stack_key_stack_counts
        inst._stack_key_objects = stack_key_objects
        inst._non_stacked_objects = non_stacked_objects
        inventory_component = subject.inventory_component
        for obj in inventory_component:
            if inst_or_cls.hidden_inventory_test != InventoryTest.TestHiddenInventories.ANY:
                hidden_only = inst_or_cls.hidden_inventory_test == InventoryTest.TestHiddenInventories.HIDDEN_ONLY
                if inventory_component.is_object_hidden(obj) != hidden_only:
                    pass
                elif not inst_or_cls.inventory_item_test(obj):
                    pass
                elif inst_or_cls.additional_item_test:
                    resolver = DoubleSimAndObjectResolver(actor_sim_info, target_sim_info, obj, inst_or_cls)
                    if not inst_or_cls.additional_item_test.run_tests(resolver):
                        pass
                    elif inst_or_cls.suppress_duplicate_objects is not None:
                        key = inst_or_cls._get_stack_key_for_object(obj=obj)
                        stack_key_stack_counts[key] += obj.stack_count()
                        stack_key_objects[key].append(obj)
                    else:
                        non_stacked_objects.append(obj)
                elif inst_or_cls.suppress_duplicate_objects is not None:
                    key = inst_or_cls._get_stack_key_for_object(obj=obj)
                    stack_key_stack_counts[key] += obj.stack_count()
                    stack_key_objects[key].append(obj)
                else:
                    non_stacked_objects.append(obj)
            elif not inst_or_cls.inventory_item_test(obj):
                pass
            elif inst_or_cls.additional_item_test:
                resolver = DoubleSimAndObjectResolver(actor_sim_info, target_sim_info, obj, inst_or_cls)
                if not inst_or_cls.additional_item_test.run_tests(resolver):
                    pass
                elif inst_or_cls.suppress_duplicate_objects is not None:
                    key = inst_or_cls._get_stack_key_for_object(obj=obj)
                    stack_key_stack_counts[key] += obj.stack_count()
                    stack_key_objects[key].append(obj)
                else:
                    non_stacked_objects.append(obj)
            elif inst_or_cls.suppress_duplicate_objects is not None:
                key = inst_or_cls._get_stack_key_for_object(obj=obj)
                stack_key_stack_counts[key] += obj.stack_count()
                stack_key_objects[key].append(obj)
            else:
                non_stacked_objects.append(obj)
        if inst is not None and inst_or_cls.suppress_duplicate_objects is not None:
            for objs in stack_key_objects.values():
                if objs:
                    yield objs[0]
        else:
            yield from non_stacked_objects

    @flexmethod
    def get_stack_count(cls, inst, obj):
        if cls.suppress_duplicate_objects is not None:
            key = cls._get_stack_key_for_object(obj=obj)
            return inst._stack_key_stack_counts[key]
        else:
            return super().get_stack_count(obj)

class ObjectInInventoryPickerInteraction(ObjectInInventoryPickerMixin, ObjectPickerInteraction):

    @flexmethod
    def _get_objects_gen(cls, inst, *args, **kwargs):
        inst_or_cls = inst if inst is not None else cls
        yield from super(__class__, inst_or_cls)._get_objects_internal_gen(*args, **kwargs)

    def _on_picker_selected(self, dialog):
        if dialog.accepted:
            super()._on_picker_selected(dialog)

class AutonomousObjectInInventoryPickerInteraction(ObjectInInventoryPickerMixin, AutonomousObjectPickerInteraction):
    pass

class AutonomousGigObjectPickerInteraction(GigObjectsPickerMixin, AutonomousObjectPickerInteraction):
    pass

class AutonomousStyleTagObjectPickerInteraction(StyleTagObjectPickerMixin, AutonomousObjectPickerInteraction):
    pass

class ObjectInHouseholdInventoryPickerMixin:
    INSTANCE_TUNABLES = {'inventory_subject': TunableEnumEntry(description='\n            Subject on which the household inventory exists.\n            ', tunable_type=ParticipantType, default=ParticipantType.Actor, tuning_group=GroupNames.PICKERTUNING), 'valid_tags': TunableSet(description='\n                If object defintion has any tags in the list then it is a valid object to consider for picker.\n                ', tunable=TunableEnumWithFilter(tunable_type=tag.Tag, filter_prefixes=['Func'], default=tag.Tag.INVALID, invalid_enums=(tag.Tag.INVALID,), pack_safe=True), tuning_group=GroupNames.PICKERTUNING)}

    @classmethod
    def _is_definition_valid_for_picker(cls, definition_manager, object_id, household_id):
        (def_id, object_data) = build_buy.get_definition_id_in_household_inventory(object_id, household_id)
        if def_id is None:
            return False
        definition = definition_manager.get(def_id, obj_state=object_data.state_index)
        if definition is None:
            return False
        definition_tags = set(definition.get_tags())
        if definition_tags & cls.valid_tags:
            return True
        save_data = protocols.PersistenceMaster()
        save_data.ParseFromString(object_data.attributes)
        for persistable_data in save_data.data:
            if persistable_data.type != protocols.PersistenceMaster.PersistableData.CraftingComponent:
                pass
            else:
                crafting_component_data = persistable_data.Extensions[protocols.PersistableCraftingComponent.persistable_data]
                recipe_manager = services.get_instance_manager(sims4.resources.Types.RECIPE)
                recipe = recipe_manager.get(crafting_component_data.process.recipe_id)
                if recipe is None:
                    break
                if definition is not recipe.final_product.definition:
                    for linked_recipe in recipe.linked_recipes_map.values():
                        if definition is linked_recipe.final_product.definition:
                            recipe = linked_recipe
                            break
                    return False
                recipe_tags = set(recipe.apply_tags)
                if recipe_tags & cls.valid_tags:
                    return True
        return False

    @flexmethod
    def _has_valid_choices_internal(cls, inst, target, context, **kwargs):
        inst_or_cls = inst if inst is not None else cls
        (object_ids, household_id) = inst_or_cls._get_object_ids_from_household_inventory(target, context, **kwargs)
        if not object_ids:
            return False
        if not cls.valid_tags:
            return True
        definition_manager = services.definition_manager()
        for object_id in object_ids:
            if inst_or_cls._is_definition_valid_for_picker(definition_manager, object_id, household_id):
                return True
        return False

    @flexmethod
    def _get_object_ids_from_household_inventory(cls, inst, target, context, **kwargs):
        inst_or_cls = inst if inst is not None else cls
        inventory_subject = inst_or_cls.get_participant(participant_type=inst_or_cls.inventory_subject, sim=context.sim, target=target, **kwargs)
        if inventory_subject is None:
            return (None, None)
        household_id = None
        if isinstance(inventory_subject, sims.household.Household):
            household_id = inventory_subject.id
        elif isinstance(inventory_subject, ScriptObject):
            if inventory_subject.is_sim:
                household_id = inventory_subject.sim_info.household_id
            else:
                household_id = inventory_subject.get_household_owner_id()
        if household_id is None:
            return (None, None)
        household = services.household_manager().get(household_id)
        if household.home_zone_id == 0:
            return (None, None)
        return (build_buy.get_object_ids_in_household_inventory(household_id), household_id)

    @flexmethod
    def _get_objects_internal_gen(cls, inst, target, context, **kwargs):
        inst_or_cls = inst if inst is not None else cls
        (object_ids, household_id) = inst_or_cls._get_object_ids_from_household_inventory(target, context, **kwargs)
        if not object_ids:
            return
        objects = []
        definition_manager = services.definition_manager()
        for object_id in object_ids:
            if not inst_or_cls._is_definition_valid_for_picker(definition_manager, object_id, household_id):
                pass
            else:
                obj = build_buy.get_object_in_household_inventory(object_id, household_id)
                if not obj is None:
                    if obj.is_sim:
                        pass
                    else:
                        objects.append(obj)
                        yield obj
        if inst:
            inst.add_liability(DELETE_OBJECT_LIABILITY, DeleteObjectLiability(objects))

class ObjectInHouseholdInventoryPickerInteraction(ObjectInHouseholdInventoryPickerMixin, ObjectPickerInteraction):

    @classmethod
    def has_valid_choice(cls, target, context, **kwargs):
        if cls._has_valid_choices_internal(target, context, **kwargs):
            return True
        return False

    @flexmethod
    def _get_objects_gen(cls, inst, *args, **kwargs):
        inst_or_cls = inst if inst is not None else cls
        yield from super(__class__, inst_or_cls)._get_objects_internal_gen(*args, **kwargs)

    def _on_picker_selected(self, dialog):
        if dialog.accepted:
            super()._on_picker_selected(dialog)

class ObjectInSlotPickerMixin:
    INSTANCE_TUNABLES = {'subject_with_slots': TunableEnumEntry(description='\n            Subject on which the slots exist.\n            ', tunable_type=ParticipantType, default=ParticipantType.Object, tuning_group=GroupNames.PICKERTUNING), 'slot_obj_test': TunableTestSet(description='\n            A set of tests to run on each object in the parents slots before\n            it will be shown in the picker dialog. Only tests with\n            ParticipantType.Object will work.\n            ', tuning_group=GroupNames.PICKERTUNING), 'required_slot_types': OptionalTunable(description='\n            If enabled, the child object must be in one of these slot types in\n            order to show up in the picker.\n            ', tunable=TunableSet(description='\n                The child object must be parented to one of these slots in\n                order to show up in the picker.\n                ', tunable=TunableStringHash32(description='\n                    The hashed name of the slot.\n                    ', default='_ctnm_SimInteraction_'), minlength=1), tuning_group=GroupNames.PICKERTUNING)}

    @flexmethod
    def _get_objects_internal_gen(cls, inst, target, context, **kwargs):
        inst_or_cls = inst if inst is not None else cls
        slot_subject = inst_or_cls.get_participant(participant_type=inst_or_cls.subject_with_slots, sim=context.sim, target=target, **kwargs)
        if slot_subject.children:
            for child in slot_subject.children:
                if not inst_or_cls.required_slot_types is not None or child.location.slot_hash or child.location.joint_name_hash not in inst_or_cls.required_slot_types:
                    pass
                elif inst_or_cls.slot_obj_test:
                    resolver = SingleObjectResolver(child)
                    if not inst_or_cls.slot_obj_test.run_tests(resolver):
                        pass
                    else:
                        yield child
                else:
                    yield child

class ObjectInSlotPickerInteraction(ObjectInSlotPickerMixin, ObjectPickerInteraction):

    @flexmethod
    def _get_objects_gen(cls, inst, *args, **kwargs):
        inst_or_cls = inst if inst is not None else cls
        yield from super(__class__, inst_or_cls)._get_objects_internal_gen(*args, **kwargs)

class AutonomousObjectInSlotPickerInteraction(ObjectInSlotPickerMixin, AutonomousObjectPickerInteraction):
    pass

class AutonomousObjectTaggedPickerInteraction(AutonomousObjectPickerInteraction):
    INSTANCE_TUNABLES = {'whitelist_filter': ObjectDefinitonsOrTagsVariant(description='\n            Either a list of tags or definitions that objects can be considered.\n            ', tuning_group=GroupNames.PICKERTUNING), 'blacklist_filter': OptionalTunable(ObjectDefinitonsOrTagsVariant(description='\n            Either a list of tags or definitions that objects should be ignored.\n            '), tuning_group=GroupNames.PICKERTUNING), 'radius': OptionalTunable(description='\n            Ensures objects are within a tuned radius.\n            \n            NOTE: THIS SHOULD ONLY BE DISABLED IF APPROVED BY A GPE.\n            Disabling this can have a serious performance impact since most \n            pickers will end up with way too many objects in them.\n            ', tunable=TunableRange(description='\n                Object must be in a certain range for consideration.\n                ', tunable_type=int, default=5, minimum=1, maximum=50), tuning_group=GroupNames.PICKERTUNING, enabled_by_default=True), 'object_filter_test': TunableObjectTaggedObjectFilterTestSet(description='\n            A list of test to verify object is valid to be selected for autonomous use.\n            ', tuning_group=GroupNames.PICKERTUNING), 'require_on_offlot_parity': Tunable(description='\n            If checked then we will not consider objects that are off the lot\n            unless the Sim running this interaction is also off.  We will\n            always consider objects on the lot.\n            ', tunable_type=bool, default=False, tuning_group=GroupNames.PICKERTUNING), 'supress_outside_if_modifier': Tunable(description='\n            If checked then we will not considered objects that are outside\n            if an outside autonomy modifier is in effect.\n            \n            If unchecked then in addition to considering objects that are outside\n            we will always score the interaction as if all objects are outside, \n            however we will still prefer objects that are inside, if any.\n            ', tunable_type=bool, default=True, tuning_group=GroupNames.PICKERTUNING), 'allow_different_level': Tunable(description='\n            If checked then the picked object can be on a different level (floor)\n            from the Sim doing the interaction.\n            ', tunable_type=bool, default=False, tuning_group=GroupNames.PICKERTUNING)}

    @classproperty
    def is_autonomous_picker_interaction(cls):
        return True

    def get_outside_score_multiplier_override(self):
        if self.counts_as_inside or self.supress_outside_if_modifier:
            return
        (_, outside_multiplier) = self.sim.sim_info.get_outside_object_score_modification()
        return outside_multiplier

    @flexmethod
    def _get_objects_internal_gen(cls, inst, target, context, **kwargs):
        inst_or_cls = inst if inst is not None else cls
        object_manager = services.object_manager()
        sim = context.sim
        sim_intended_postion = sim.intended_position
        sim_level = sim.level
        prevent_outside = False
        handle_outside = False
        skipped = []
        (prevent_outside, outside_multiplier) = sim.sim_info.get_outside_object_score_modification()
        handle_outside = outside_multiplier != 1.0 or prevent_outside
        should_do_outside_later = (inst_or_cls.counts_as_inside or not inst_or_cls.supress_outside_if_modifier) and not prevent_outside
        for obj in object_manager.get_objects_with_filter_gen(inst_or_cls.whitelist_filter):
            if not sim_level != obj.level or not inst_or_cls.allow_different_level:
                pass
            elif not inst_or_cls.blacklist_filter is not None or inst_or_cls.blacklist_filter.matches(obj):
                pass
            elif inst_or_cls.radius is not None:
                delta = obj.intended_position - sim_intended_postion
                if delta.magnitude() > inst_or_cls.radius:
                    pass
                elif not handle_outside or obj.is_in_sim_inventory(sim) or obj.is_outside:
                    if should_do_outside_later:
                        skipped.append(obj)
                        if inst_or_cls._passes_post_skip_tests(sim, obj):
                            should_do_outside_later = False
                            skipped.clear()
                            yield obj
                elif inst_or_cls._passes_post_skip_tests(sim, obj):
                    should_do_outside_later = False
                    skipped.clear()
                    yield obj
            elif not handle_outside or obj.is_in_sim_inventory(sim) or obj.is_outside:
                if should_do_outside_later:
                    skipped.append(obj)
                    if inst_or_cls._passes_post_skip_tests(sim, obj):
                        should_do_outside_later = False
                        skipped.clear()
                        yield obj
            elif inst_or_cls._passes_post_skip_tests(sim, obj):
                should_do_outside_later = False
                skipped.clear()
                yield obj
        for obj in skipped:
            if inst_or_cls._passes_post_skip_tests(sim, obj):
                yield obj

    @flexmethod
    def _passes_post_skip_tests(cls, inst, sim, obj):
        inst_or_cls = inst if inst is not None else cls
        if inst_or_cls.require_on_offlot_parity and sim.is_on_active_lot(tolerance=StatisticComponentGlobalTuning.DEFAULT_OFF_LOT_TOLERANCE) and not obj.is_on_active_lot(tolerance=StatisticComponentGlobalTuning.DEFAULT_OFF_LOT_TOLERANCE):
            return False
        if inst_or_cls.object_filter_test:
            resolver = event_testing.resolver.SingleActorAndObjectResolver(sim.sim_info, obj, source='AutonomousObjectTaggedPickerInteraction')
            result = inst_or_cls.object_filter_test.run_tests(resolver)
            if not result:
                return False
        if obj.parts is not None:
            for part in obj.parts:
                if part.is_connected(sim):
                    return True
        if not obj.is_connected(sim):
            return False
        return True
lock_instance_tunables(AutonomousObjectTaggedPickerInteraction, pre_add_autonomy_commodities=None, pre_run_autonomy_commodities=None, post_guaranteed_autonomy_commodities=None, post_run_autonomy_commodities=None, basic_content=None, outfit_change=None, outfit_priority=None, joinable=None, object_reservation_tests=TunableTestSet.DEFAULT_LIST, ignore_group_socials=False)
class AutonomousPreferredObjectPickerInteraction(AutonomousObjectPickerInteraction):
    INSTANCE_TUNABLES = {'preference_tag': TunableEnumEntry(description='\n            The preference tag to use.\n            ', tunable_type=ObjectPreferenceTag, default=ObjectPreferenceTag.INVALID, invalid_enums=(ObjectPreferenceTag.INVALID,), tuning_group=GroupNames.PICKERTUNING)}

    @classproperty
    def is_autonomous_picker_interaction(cls):
        return True

    def get_outside_score_multiplier_override(self):
        if self.counts_as_inside:
            return
        else:
            target_object = self.sim.get_use_only_object(self.preference_tag)
            if target_object is not None and target_object.is_outside():
                (_, outside_multiplier) = self.sim.sim_info.get_outside_object_score_modification()
                return outside_multiplier

    @classmethod
    def _get_objects_internal_gen(cls, target, context, **kwargs):
        sim = context.sim
        target_object = sim.get_use_only_object(cls.preference_tag)
        if target_object is not None:
            yield target_object
lock_instance_tunables(AutonomousPreferredObjectPickerInteraction, pre_add_autonomy_commodities=None, pre_run_autonomy_commodities=None, post_guaranteed_autonomy_commodities=None, post_run_autonomy_commodities=None, basic_content=None, outfit_change=None, outfit_priority=None, joinable=None, object_reservation_tests=TunableTestSet.DEFAULT_LIST, ignore_group_socials=False)
class ActorUrnstonePickerInteraction(ActorsUrnstonePickerMixin, ObjectPickerInteraction):
    pass

class _PurchasePickerItemData:

    def __init__(self):
        self.objects = set()
        self.num_available = None
        self.fashion_trend = None

class PurchasePickerData:

    def __init__(self):
        self.inventory_owner_id_to_purchase_to = 0
        self.inventory_owner_id_to_purchase_from = 0
        self.items_to_purchase = defaultdict(_PurchasePickerItemData)
        self.use_obj_ids_in_response = False
        self.delivery_method = PickerInteractionDeliveryMethod.INVENTORY

    def add_definition_to_purchase(self, definition, custom_price=None, obj=None, num_available=None, fashion_trend=None):
        purchase_picker_item_data = self.items_to_purchase[(definition, custom_price)]
        purchase_picker_item_data.objects.add(obj)
        purchase_picker_item_data.num_available = num_available
        purchase_picker_item_data.fashion_trend = fashion_trend

class PurchaseListOption(HasTunableSingletonFactory, AutoFactoryInit):

    def has_choices(self, inst_or_cls, **kwargs):
        return False

    def on_picker_selected(self, dialog):
        pass

    def add_objects_to_purchase_picker(self, inst_or_cls, purchase_picker_data, **kwargs):
        pass

class DefinitionsFromTags(PurchaseListOption):
    FACTORY_TUNABLES = {'filter_tags': OptionalTunable(description='\n            An optional filter that if enabled will filter out the allowed items\n            based on the filter.\n            ', tunable=TunableSet(description='\n                A list of category tags to to search to build object picker\n                list.\n                ', tunable=TunableEnumEntry(description='\n                    What tag to test for\n                    ', tunable_type=tag.Tag, default=tag.Tag.INVALID), minlength=1), disabled_name='all_definitions', enabled_name='specific_definitions')}

    def get_items_gen(self, *args):
        yield from self._get_items_internal_gen()

    def _get_items_internal_gen(self):
        definition_manager = services.definition_manager()
        if self.filter_tags is None:
            yield from definition_manager.loaded_definitions
        else:
            yield from definition_manager.get_definitions_for_tags_gen(self.filter_tags)

    def has_choices(self, inst_or_cls, **kwargs):
        for _ in self._get_items_internal_gen():
            return True
        return False

    def add_objects_to_purchase_picker(self, inst_or_cls, purchase_picker_data, **kwargs):
        for obj in self._get_items_internal_gen():
            purchase_picker_data.add_definition_to_purchase(obj)

class DefinitionsExplicit(PurchaseListOption):
    FACTORY_TUNABLES = {'item_list': TunableSet(description='\n            The list of items available for purchase.\n            ', tunable=TunableReference(manager=services.definition_manager(), pack_safe=True), minlength=1)}

    def get_items_gen(self, *args):
        yield from self._get_items_internal_gen()

    def _get_items_internal_gen(self):
        yield from self.item_list

    def has_choices(self, inst_or_cls, **kwargs):
        for _ in self._get_items_internal_gen():
            return True
        return False

    def add_objects_to_purchase_picker(self, inst_or_cls, purchase_picker_data, **kwargs):
        for obj in self._get_items_internal_gen():
            purchase_picker_data.add_definition_to_purchase(obj)

class DefinitionsRandom(PurchaseListOption):
    FACTORY_TUNABLES = {'item_list': TunableList(description='\n            The list of items available for purchase.\n            ', tunable=TunableTuple(description='\n                A weighted list of items to be available.\n                ', item=TunableReference(description='\n                    An item that is potentially available.\n                    ', manager=services.definition_manager(), pack_safe=True), weight=TunableRange(description='\n                    How likely this item to be picked.\n                    ', tunable_type=int, minimum=1, default=1)), minlength=1), 'items_avaiable': TunableRange(description='\n            The number of items available.\n            ', tunable_type=int, minimum=1, default=1)}

    def get_items_gen(self, *args):
        yield from self._get_items_internal_gen()

    def _get_items_internal_gen(self):
        now = services.time_service().sim_now
        rand = random.Random(int(now.absolute_days()))
        possible_items = [(item.weight, item.item) for item in self.item_list]
        for _ in range(self.items_avaiable):
            chosen_item = pop_weighted(possible_items, random=rand)
            yield chosen_item

    def has_choices(self, inst_or_cls, **kwargs):
        return True

    def add_objects_to_purchase_picker(self, inst_or_cls, purchase_picker_data, **kwargs):
        for obj in self._get_items_internal_gen():
            purchase_picker_data.add_definition_to_purchase(obj)

class DefinitionsTested(PurchaseListOption):
    FACTORY_TUNABLES = {'item_list': TunableList(description='\n            The list of items available for purchase.\n            ', tunable=TunableTuple(description='\n                A pair of items and tests to run in order to see if those items would be available.\n                ', item=TunableReference(description='\n                    An item that is potentially available.\n                    ', manager=services.definition_manager(), pack_safe=True), tests=TunableTestSet(description='\n                    A set of tests to run to see if this item would be available.\n                    ')), minlength=1)}

    def get_items_gen(self, inst_or_cls, *args):
        yield from self._get_items_internal_gen(inst_or_cls)

    def _get_items_internal_gen(self, inst_or_cls, **interaction_kwargs):
        resolver = inst_or_cls.get_resolver(**interaction_kwargs)
        for potential_item in self.item_list:
            if potential_item.tests.run_tests(resolver):
                yield potential_item.item

    def has_choices(self, inst_or_cls, **interaction_kwargs):
        for _ in self._get_items_internal_gen(inst_or_cls, **interaction_kwargs):
            return True
        return False

    def add_objects_to_purchase_picker(self, inst_or_cls, purchase_picker_data, **interaction_kwargs):
        for obj in self._get_items_internal_gen(inst_or_cls, **interaction_kwargs):
            purchase_picker_data.add_definition_to_purchase(obj)
OBJ_REQUIREMENT_PURCHASABLE = 0OBJ_REQUIREMENT_STATE_THRESHOLD = 1PURCHASE_BY_DEFINITION = 0PURCHASE_BY_ITEM_COPY = 1
class PriceOption(enum.Int):
    USE_CURRENT_VALUE = 0
    USE_RETAIL_VALUE = 1

class InventoryItems(PurchaseListOption):
    FACTORY_TUNABLES = {'participant_type': TunableEnumEntry(description="\n            The participant type who's inventory will be used to list objects.\n            ", tunable_type=ParticipantType, default=ParticipantType.Object), 'object_requirement': OptionalTunable(description='\n            The requirements the object must meet to be added to the picker. If\n            this is disabled, all inventory items will be displayed.\n            ', tunable=TunableVariant(description='\n                The requirements for being added to the picker.\n                ', purchasable=TunableTuple(description='\n                    Only show items that are in the Purchasable Objects list for\n                    the targets inventory component.\n                    ', locked_args={'requirement_type': OBJ_REQUIREMENT_PURCHASABLE}), state_threshold=TunableTuple(description='\n                    Only show items that meet this state threshold.\n                    ', threshold=TunableThreshold(description='\n                        The state threshold the object must meet.\n                        ', value=TunableReference(manager=services.get_instance_manager(sims4.resources.Types.OBJECT_STATE), class_restrictions='ObjectStateValue')), locked_args={'requirement_type': OBJ_REQUIREMENT_STATE_THRESHOLD}))), 'purchase_option': TunableVariant(description='\n            Options for how we we want to purchase the items we found in the\n            inventory.\n            ', by_definition=TunableTuple(description="\n                Purchase the item by the definition id.  A new item will be\n                generated using the object's definition.  This will just use the\n                catalog price of the item to purchase it.\n                ", locked_args={'purchase_type': PURCHASE_BY_DEFINITION}), by_copy=TunableTuple(description='\n                Purchase the item by actually copying one of the instances of\n                the items in the inventory.  Objects will be grouped by price\n                within the picker.\n                ', price_option=TunableEnumEntry(description='\n                    The option for determining the price of the item.\n                    ', tunable_type=PriceOption, default=PriceOption.USE_CURRENT_VALUE), locked_args={'purchase_type': PURCHASE_BY_ITEM_COPY}), default='by_definition')}

    def _get_items_internal_gen(self, inst_or_cls, **interaction_kwargs):
        participant = inst_or_cls.get_participant(participant_type=self.participant_type, **interaction_kwargs)
        inventory_component = participant.inventory_component
        if inventory_component is not None:
            if self.object_requirement is None:
                yield from inventory_component
            elif self.object_requirement.requirement_type == OBJ_REQUIREMENT_PURCHASABLE:
                yield from inventory_component.purchasable_objects.objects
            elif self.object_requirement.requirement_type == OBJ_REQUIREMENT_STATE_THRESHOLD:
                desired_state = self.object_requirement.threshold.value.state
                for obj in inventory_component:
                    if obj.has_state(desired_state) and self.object_requirement.threshold.compare_value(obj.get_state(desired_state)):
                        yield obj

    def has_choices(self, inst_or_cls, **kwargs):
        for _ in self._get_items_internal_gen(inst_or_cls, **kwargs):
            return True
        return False

    def add_objects_to_purchase_picker(self, inst_or_cls, purchase_picker_data, **interaction_kwargs):
        objects_to_purchase = tuple(self._get_items_internal_gen(inst_or_cls, **interaction_kwargs))
        if self.purchase_option.purchase_type == PURCHASE_BY_DEFINITION:
            for obj in objects_to_purchase:
                purchase_picker_data.add_definition_to_purchase(obj.definition)
        elif self.purchase_option.purchase_type == PURCHASE_BY_ITEM_COPY:
            participant = inst_or_cls.get_participant(participant_type=self.participant_type, **interaction_kwargs)
            purchase_picker_data.inventory_owner_id_to_purchase_from = participant.id
            purchase_picker_data.use_obj_ids_in_response = True
            for obj in objects_to_purchase:
                if self.purchase_option.price_option == PriceOption.USE_CURRENT_VALUE:
                    price = int(obj.current_value)
                elif self.purchase_option.price_option == PriceOption.USE_RETAIL_VALUE:
                    price = int(obj.retail_component.get_sell_price())
                else:
                    logger.error('Trying to add items to the purchase picker with invalid price option.')
                    break
                purchase_picker_data.add_definition_to_purchase(obj.definition, custom_price=price, obj=obj)
        else:
            logger.error('Trying to fill purchase picker from inventory with invalid purchase option.', owner='jjacobson')
            return

class LimitedItemList(PurchaseListOption):
    FACTORY_TUNABLES = {'purchase_picker_groups': TunableList(description='\n            The groups of limited items to grab from the purchase picker service.\n            These items will have a randomly selected limited stock to be sold from the service.\n            Stock is persisted across lots and refreshed on a per day basis based on the service.\n            ', tunable=TunableEnumEntry(description='\n                A purchase picker group to grab the items from.\n                ', tunable_type=PurchasePickerGroup, default=PurchasePickerGroup.INVALID))}

    def has_choices(self, inst_or_cls, **interaction_kwargs):
        purchase_picker_service = services.purchase_picker_service()
        for purchase_picker_group in self.purchase_picker_groups:
            if purchase_picker_service.has_available_items_for_group(purchase_picker_group):
                return True
        return False

    def on_picker_selected(self, dialog):
        purchase_picker_service = services.purchase_picker_service()
        (def_ids, counts) = dialog.get_result_definitions_and_counts()
        purchased_item_count_pairs = dict(zip(def_ids, counts))
        for purchase_picker_group in self.purchase_picker_groups:
            purchase_picker_service.update_item_count_pairs(purchase_picker_group, purchased_item_count_pairs)

    def add_objects_to_purchase_picker(self, inst_or_cls, purchase_picker_data, **interaction_kwargs):
        purchase_picker_service = services.purchase_picker_service()
        definition_manager = services.definition_manager()
        for purchase_picker_group in self.purchase_picker_groups:
            purchase_list = purchase_picker_service.get_items_for_group(purchase_picker_group)
            for (def_id, num_available) in purchase_list.items():
                definition = definition_manager.get(def_id)
                purchase_picker_data.add_definition_to_purchase(definition=definition, num_available=num_available)

class ParticipantInventoryCount(TunableFactory):

    @staticmethod
    def factory(interaction, definition, participant_type=ParticipantType.Object):
        participant = interaction.get_participant(participant_type)
        inventory_component = participant.inventory_component
        if inventory_component is None:
            return 0
        return inventory_component.get_count(definition)

    FACTORY_TYPE = factory

    def __init__(self, *args, **kwargs):
        super().__init__(participant_type=TunableEnumEntry(description="\n                The participant type who's inventory will be used to count the\n                number of objects owned of a specific definition.\n                ", tunable_type=ParticipantType, default=ParticipantType.Object), **kwargs)

class InventoryTypeCount(TunableFactory):

    @staticmethod
    def factory(_, definition, inventory_type=InventoryType.UNDEFINED):
        inventories = services.active_lot().get_object_inventories(inventory_type)
        return sum(inventory.get_count(definition) for inventory in inventories)

    FACTORY_TYPE = factory

    def __init__(self, *args, **kwargs):
        super().__init__(inventory_type=TunableEnumEntry(description='\n                The type of inventory that is used to count the number of\n                objects owned of a specific definition.\n                ', tunable_type=InventoryType, default=InventoryType.UNDEFINED), **kwargs)

class PurchaseToInventory(TunableFactory):

    @staticmethod
    def factory(interaction, purchase_picker_data, participant_type=ParticipantType.Object):
        participant = interaction.get_participant(participant_type)
        purchase_picker_data.inventory_owner_id_to_purchase_to = participant.id
        purchase_picker_data.delivery_method = PickerInteractionDeliveryMethod.INVENTORY

    FACTORY_TYPE = factory

    def __init__(self, *args, **kwargs):
        super().__init__(participant_type=TunableEnumEntry(description="\n                The participant who's inventory we will put the purchased items\n                into.\n                ", tunable_type=ParticipantType, default=ParticipantType.Object), **kwargs)

class MailmanDelivery(TunableFactory):

    @staticmethod
    def factory(_, purchase_picker_data):
        purchase_picker_data.delivery_method = PickerInteractionDeliveryMethod.MAILMAN

    FACTORY_TYPE = factory

class SlotToParent(TunableFactory):

    @staticmethod
    def factory(interaction, purchase_picker_data, participant_type=ParticipantType.Object, **kwargs):
        participant = interaction.get_participant(participant_type)
        purchase_picker_data.inventory_owner_id_to_purchase_to = participant.id
        purchase_picker_data.delivery_method = PickerInteractionDeliveryMethod.SLOT_TO_PARENT

    FACTORY_TYPE = factory

    def __init__(self, *args, **kwargs):
        super().__init__(participant_type=TunableEnumEntry(description='\n                The participant who we will slot each of the objects created to.\n                ', tunable_type=ParticipantType, default=ParticipantType.Object), slot_objects=SlotObjects.TunableFactory(description='\n                How to slot each of the created objects. All of the objects will use the same tuning.\n                '), **kwargs)

class DeliveryServiceNPC(TunableFactory):

    @staticmethod
    def factory(_, purchase_picker_data):
        purchase_picker_data.delivery_method = PickerInteractionDeliveryMethod.DELIVERY_SERVICE_NPC

    FACTORY_TYPE = factory

class TransactionPickerMixin:
    INSTANCE_TUNABLES = {'purchase_notification': OptionalTunable(description='\n            If enabled, a notification is displayed should the purchase picker\n            dialog be accepted.\n            ', tunable=TunableUiDialogNotificationSnippet(description='\n                The notification to show when the purchase picker dialog is\n                accepted.\n                '), tuning_group=GroupNames.PICKERTUNING), 'price_multiplier': TunableMultiplier.TunableFactory(description='\n            Tested multipliers to apply to the price of the item.\n            ', tuning_group=GroupNames.PICKERTUNING, multiplier_options={'use_tooltip': True}), 'show_descriptions': Tunable(description='\n            If True then we will show descriptions of the objects in the picker.\n            ', tunable_type=bool, default=True, tuning_group=GroupNames.PICKERTUNING), 'show_discount': Tunable(description="\n            If enabled, the UI for the purchase/sell picker will show a\n            strikethrough of the original price if it's different than the\n            final price.\n            ", tunable_type=bool, default=False, tuning_group=GroupNames.PICKERTUNING), 'show_description_tooltip': Tunable(description='\n            If True then we will show description tooltips of the objects in the picker.\n            ', tunable_type=bool, default=True, tuning_group=GroupNames.PICKERTUNING)}

    def _run_interaction_gen(self, timeline):
        self._show_picker_dialog(self.sim)
        return True

    def _on_picker_selected(self, dialog):
        if dialog.accepted and self.purchase_notification is not None:
            notification_dialog = self.purchase_notification(self.sim, resolver=self.get_resolver())
            notification_dialog.show_dialog()

class SellPickerInteraction(ObjectInInventoryPickerMixin, TransactionPickerMixin, PickerSuperInteraction):

    @classmethod
    def has_valid_choice(cls, target, context, **kwargs):
        for _ in cls._get_objects_internal_gen(target, context, **kwargs):
            return True
        return False

    def _setup_dialog(self, dialog, **kwargs):
        participant = self.get_participant(participant_type=self.inventory_subject)
        dialog.inventory_object_id = participant.id
        dialog.show_description = self.show_descriptions
        dialog.show_description_tooltip = self.show_description_tooltip
        dialog.use_dialog_pick_response = False
        resolver = self.get_resolver()
        (multiplier, tooltip) = self.price_multiplier.get_multiplier_and_tooltip(resolver)
        for obj in self._get_objects_internal_gen(self.target, self.context, **kwargs):
            definition = obj.definition
            custom_price = int(obj.current_value)
            if multiplier != 1:
                custom_price = math.ceil(custom_price*multiplier)
                tooltip = None
            row = PurchasePickerRow(def_id=definition.id, is_enable=True, num_available=self.get_stack_count(obj), tags=definition.build_buy_tags, custom_price=custom_price, objects={obj}, row_tooltip=tooltip, show_discount=self.show_discount and multiplier != 1, prediscounted_price=obj.current_value)
            dialog.add_row(row)

    def _remove_sold_objects_from_inventory(self, dialog):
        ids_and_amounts_and_price = dialog.ids_and_amounts_and_price
        source_inventory = dialog.source_inventory
        inventory_manager = services.inventory_manager()
        for (obj_id, amount, price) in zip(ids_and_amounts_and_price[::3], ids_and_amounts_and_price[1::3], ids_and_amounts_and_price[2::3]):
            row_obj = inventory_manager.get(obj_id)
            if row_obj is None:
                logger.error('Object sold are not in inventory or already destroyed. Interaction: {}, Object ID: {}', self, obj_id)
            else:
                key = self._get_stack_key_for_object(row_obj)
                potential_objects = self._stack_key_objects[key] if self.suppress_duplicate_objects is not None else [row_obj]
                for obj in potential_objects:
                    if amount <= 0:
                        break
                    amount_to_remove = min(amount, obj.stack_count())
                    amount -= amount_to_remove
                    source_inventory.try_destroy_object(obj, amount_to_remove)

    def _on_picker_selected(self, dialog):
        super()._on_picker_selected(dialog)
        if dialog.accepted:
            self._remove_sold_objects_from_inventory(dialog)

class PurchasePickerMixin(TransactionPickerMixin):
    INSTANCE_TUNABLES = {'purchase_list_option': TunableList(description='\n            A list of methods that will be used to generate the list of objects that are available in the picker.\n            ', tunable=TunableVariant(description='\n                The method that will be used to generate the list of objects that\n                will populate the picker.\n                ', all_items=DefinitionsFromTags.TunableFactory(description='\n                    Look through all the items that are possible to purchase.\n                    \n                    This should be accompanied with specific filtering tags in\n                    Object Populate Filter to get a good result.\n                    '), specific_items=DefinitionsExplicit.TunableFactory(description='\n                    A list of specific items that will be purchasable through this\n                    dialog.\n                    '), inventory_items=InventoryItems.TunableFactory(description='\n                    Looks at the objects that are in the inventory of the desired\n                    participant and returns them based on some criteria.\n                    '), random_items=DefinitionsRandom.TunableFactory(description='\n                    Randomly selects items based on a weighted list.\n                    '), tested_items=DefinitionsTested.TunableFactory(description='\n                    Test items that are able to be displayed within the picker.\n                    '), limited_items=LimitedItemList.TunableFactory(description='\n                    Items provided by the Purchase Picker Service. \n                    '), default='all_items'), tuning_group=GroupNames.PICKERTUNING), 'object_count_option': OptionalTunable(description='\n            If enabled then we will display a count next to each item of the\n            number owned.\n            ', tunable=TunableList(description='\n                A list of methods to used to count the number of instances of\n                specific objects.\n                ', tunable=TunableVariant(description='\n                    The method that will be used to determine the object count\n                    that is displayed in the UI next to each item.\n                    ', participant_inventory_count=ParticipantInventoryCount(description="\n                        We will count through the number of objects that are in\n                        the target's inventory and display that as the number\n                        owned in the UI.\n                        "), inventory_type_count=InventoryTypeCount(description='\n                        We will count through the number of objects that are in\n                        a specific inventory type (for example fridges) and\n                        display that as the number owned in the UI.\n                        '), default='participant_inventory_count')), tuning_group=GroupNames.PICKERTUNING), 'delivery_method': TunableVariant(description='\n            Where the objects purchased will be delivered.\n            ', purchase_to_inventory=PurchaseToInventory(description="\n                Purchase the objects directly into a participant's inventory.\n                "), mailman_delivery=MailmanDelivery(description='\n                Deliver the objects by the mailman.\n                '), slot_to_parent=SlotToParent(description='\n                Deliver the objects by slotting them to a parent object.\n                '), delivery_service_npc=DeliveryServiceNPC(description='\n                Purchased objects will be delivered by the delivery service npc.\n                '), default='purchase_to_inventory', tuning_group=GroupNames.PICKERTUNING)}

    @flexmethod
    def _setup_dialog(cls, inst, dialog, **kwargs):
        inst_or_cls = inst if inst is not None else cls
        purchase_picker_data = inst_or_cls.purchase_picker_data = PurchasePickerData()
        inst_or_cls._setup_delivery_method(purchase_picker_data)
        inst_or_cls._populate_items(purchase_picker_data)
        dialog.inventory_object_id = purchase_picker_data.inventory_owner_id_to_purchase_from
        dialog.object_id = purchase_picker_data.inventory_owner_id_to_purchase_to
        dialog.delivery_method = purchase_picker_data.delivery_method
        dialog.purchase_by_object_ids = purchase_picker_data.use_obj_ids_in_response
        dialog.show_description = inst_or_cls.show_descriptions
        dialog.show_description_tooltip = inst_or_cls.show_description_tooltip
        dialog.use_dialog_pick_response = inst_or_cls._supports_pick_response()
        right_custom_text = inst_or_cls._get_right_custom_text()
        if right_custom_text is not None:
            dialog.right_custom_text = right_custom_text
        if dialog._resolver:
            resolver = dialog._resolver
        else:
            resolver = inst_or_cls.get_resolver()
        (multiplier, tooltip) = inst_or_cls.price_multiplier.get_multiplier_and_tooltip(resolver)
        for ((definition, custom_price), item_data) in purchase_picker_data.items_to_purchase.items():
            if multiplier != 1:
                original_price = custom_price if custom_price is not None else definition.price
                custom_price = int(original_price*multiplier)
                tooltip = None
            row = PurchasePickerRow(def_id=definition.id, is_enable=inst_or_cls._get_enabled_option(definition), num_owned=inst_or_cls._get_count_option(definition), num_available=item_data.num_available or inst_or_cls._get_availability_option(definition), tags=definition.build_buy_tags, custom_price=custom_price, fashion_trend=item_data.fashion_trend, objects=item_data.objects, row_tooltip=tooltip, show_discount=inst_or_cls.show_discount, icon_info_data_override=inst_or_cls._get_icon_info_data_override_option(definition), row_description=inst_or_cls._get_description_override_option(definition))
            dialog.add_row(row)

    @flexmethod
    def _setup_delivery_method(cls, inst, purchase_picker_data):
        inst_or_cls = inst if inst is not None else cls
        inst_or_cls.delivery_method(inst_or_cls, purchase_picker_data)

    @flexmethod
    def _populate_items(cls, inst, purchase_picker_data):
        inst_or_cls = inst if inst is not None else cls
        if inst_or_cls.purchase_list_option is None:
            return
        for purchase_method in inst_or_cls.purchase_list_option:
            purchase_method.add_objects_to_purchase_picker(inst_or_cls, purchase_picker_data)

    @flexmethod
    def _get_enabled_option(cls, inst, item):
        return True

    @flexmethod
    def _get_right_custom_text(cls, inst):
        pass

    @flexmethod
    def _supports_pick_response(cls, inst):
        return False

    @flexmethod
    def _get_count_option(cls, inst, item):
        inst_or_cls = inst if inst is not None else cls
        if inst_or_cls.object_count_option is None:
            return 0
        return sum(count_method(inst_or_cls, item) for count_method in inst_or_cls.object_count_option)

    @flexmethod
    def _get_availability_option(cls, inst, item):
        pass

    @flexmethod
    def _get_icon_info_data_override_option(cls, inst, item):
        pass

    @flexmethod
    def _get_description_override_option(cls, inst, item):
        pass

    @flexmethod
    def _update_purchased_items(cls, inst, dialog):
        inst_or_cls = inst if inst is not None else cls
        if inst_or_cls.purchase_list_option is None:
            return
        for purchase_method in inst_or_cls.purchase_list_option:
            purchase_method.on_picker_selected(dialog)

    @classmethod
    def has_valid_choice(cls, target, context, **kwargs):
        if cls.purchase_list_option is None:
            return False
        for purchase_method in cls.purchase_list_option:
            if purchase_method.has_choices(cls, target=target, context=context, sim=context.sim, **kwargs):
                return True
        return False

class PurchasePickerInteraction(PurchasePickerMixin, PickerSuperInteraction):
    INSTANCE_TUNABLES = {'loots_on_purchase': TunableList(description='\n            A list of loots to run immediately on each of the items purchased.\n            ', tunable=TunableReference(description='\n                A loot to apply to a purchase.\n                ', manager=services.get_instance_manager(sims4.resources.Types.ACTION)), tuning_group=GroupNames.PICKERTUNING), 'staggered_states_on_purchase': TunableTuple(description='\n            A list of state change ops to run after a tuned delay between each of the\n            items purchased. Item 1 will trigger after 0 minutes, Item 2 after [delay]\n            minutes, Item 3 after another [delay] minutes, etc. The participant purchased\n            object is of the Object participant type.\n            \n            Please note that this timed state trigger does not persist through save/load.\n            ', delay=TunableSimMinute(description='\n                The amount of time between triggering the loots on each purchased item.\n                ', default=0, minimum=0), ops=TunableList(tunable=TimedStateChangeOp.TunableFactory(description='\n                    State change to run after the staggered delay.\n                    ', locked_args={'trigger_time': 0, 'trigger_time_random_offset': 0})), tuning_group=GroupNames.PICKERTUNING)}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.purchase_picker_data = None

    def _run_interaction_gen(self, timeline):
        self._show_picker_dialog(self.sim)
        return True

    def _update_items_providers(self, dialog):
        self._update_purchased_items(dialog)

    def _process_loots(self, obj, resolver, interaction_parameters):
        interaction_parameters['picked_item_ids'] = {obj.id}
        resolver.interaction_parameters = interaction_parameters
        for loot in self.loots_on_purchase:
            loot.apply_to_resolver(resolver)

    def _process_staggered_loot(self, obj, delay):
        if not obj.has_component(STATE_COMPONENT):
            logger.error('Attempting to set state on purchased item {} without a state component.', obj, owner='amwu')
            return
        for state_change in self.staggered_states_on_purchase.ops:
            obj.set_dynamic_timed_state(state_change, delay)

    def _slot_created_objects_to_parent(self, dialog):
        created_obj_ids = dialog.get_created_objects_ids()
        objects = []
        interaction_parameters = {}
        resolver = self.get_resolver(**interaction_parameters)
        object_manager = services.object_manager()
        inventory_manager = services.inventory_manager()
        for obj_id_by_type in created_obj_ids:
            for obj_id in obj_id_by_type:
                obj = object_manager.get(obj_id)
                if obj is None:
                    pass
                else:
                    objects.append(obj)
                    self._process_loots(obj, resolver, interaction_parameters)
                    while obj.stack_count() > 1:
                        split_obj = obj.try_split_object_from_stack(obj.stack_count() - 1)
                        if split_obj is None:
                            split_obj = obj.clone()
                            split_obj.set_stack_count(1)
                            obj.update_stack_count(-1)
                        objects.append(split_obj)
        delay = 0
        for slot_obj in objects:
            interaction_parameters['picked_item_ids'] = {slot_obj.id}
            resolver.interaction_parameters = interaction_parameters
            self.delivery_method.slot_objects.apply_to_resolver(resolver)
            self._process_staggered_loot(slot_obj, delay)
            delay += self.staggered_states_on_purchase.delay

    def handle_loots(self, dialog):
        interaction_parameters = {}
        resolver = self.get_resolver(**interaction_parameters)
        object_manager = services.object_manager()
        inventory_manager = services.inventory_manager()
        if object_manager is None:
            return
        created_obj_ids = dialog.get_created_objects_ids()
        delay = 0
        for obj_id_by_type in created_obj_ids:
            for obj_id in obj_id_by_type:
                obj = object_manager.get(obj_id)
                if obj is None:
                    obj = inventory_manager.get(obj_id)
                    if obj is None:
                        pass
                    else:
                        self._process_loots(obj, resolver, interaction_parameters)
                        self._process_staggered_loot(obj, delay)
                        delay += self.staggered_states_on_purchase.delay
                else:
                    self._process_loots(obj, resolver, interaction_parameters)
                    self._process_staggered_loot(obj, delay)
                    delay += self.staggered_states_on_purchase.delay

    def _on_picker_selected(self, dialog):
        super()._on_picker_selected(dialog)
        if dialog.accepted:
            self._update_items_providers(dialog)
            if self.delivery_method == PickerInteractionDeliveryMethod.SLOT_TO_PARENT:
                self._slot_created_objects_to_parent(dialog)
            elif self.loots_on_purchase:
                self.handle_loots(dialog)

    def _get_current_selected_count(self):
        target = self.target
        animal_service = services.animal_service()
        if target is not None and animal_service is not None and animal_service.is_registered_home(target.id):
            return animal_service.get_current_occupancy(target.id)
        else:
            return super()._get_current_selected_count()

class PurchasePickerWithContinuationInteraction(PurchasePickerInteraction):
    INSTANCE_TUNABLES = {'continuation': TunableContinuation(description='\n            A continuation to push that provides access to the newly purchased\n            items as a participant to the interaction. PurchasedObject will be\n            the items that were purcahsed. If no object is purchased or objects\n            are not delivered to an inventory, the continuation will not be run. \n            ', tuning_group=GroupNames.PICKERTUNING)}

    def _on_picker_selected(self, dialog):
        super()._on_picker_selected(dialog)
        if dialog.accepted:
            self._push_purchase_continuation(dialog)

    def _push_purchase_continuation(self, dialog):
        purchased_item_ids = list()
        created_obj_ids_by_type = dialog.get_created_objects_ids()
        for obj_id_by_type in created_obj_ids_by_type:
            for obj_id in obj_id_by_type:
                purchased_item_ids.append(obj_id)
        if purchased_item_ids is not None:
            self.interaction_parameters['purchased_item_ids'] = purchased_item_ids
            self.push_tunable_continuation(self.continuation, purchased_item_ids=purchased_item_ids, insert_strategy=QueueInsertStrategy.LAST)

class ObjectsInMultipleInventoriesMixin:
    INSTANCE_TUNABLES = {'use_sim_inventory': OptionalTunable(description="\n            If enabled, the actor for who's inventory to look for items that pass \n            the test.\n            ", tunable=TunableEnumEntry(description='\n                Subject on which the sim inventory exists.\n                ', tunable_type=ParticipantType, default=ParticipantType.Actor), tuning_group=GroupNames.PICKERTUNING), 'use_household_inventory': OptionalTunable(description="\n                If enabled, the actor who's household inventory to look for \n                items that pass the test.\n               ", tunable=TunableEnumEntry(description='\n                    Subject on which the household inventory exists.\n                    ', tunable_type=ParticipantType, default=ParticipantType.Actor), tuning_group=GroupNames.PICKERTUNING), 'inventory_item_test': TunableVariant(default='object', description='\n                A test to run on the objects in the inventory to determine\n                which objects will show up in the picker. An object test type\n                left un-tuned is considered any object.\n                ', object=ObjectTypeFactory.TunableFactory(), tag_set=ObjectTagFactory.TunableFactory(), tuning_group=GroupNames.PICKERTUNING)}

    @flexmethod
    def _get_objects_internal_gen(cls, inst, target, context, **kwargs):
        inst_or_cls = inst if inst is not None else cls
        if inst_or_cls.use_household_inventory is not None:
            yield from inst_or_cls._get_objects_from_household_inventory(inst_or_cls.use_household_inventory, target, context, **kwargs)
        if inst_or_cls.use_sim_inventory is not None:
            yield from inst_or_cls._get_objects_from_sim_inventory(inst_or_cls.use_sim_inventory, target, context, **kwargs)

    @flexmethod
    def _get_objects_from_household_inventory(cls, inst, participant_type, target, context, **kwargs):
        inst_or_cls = inst if inst is not None else cls
        inventory_subject = inst_or_cls.get_participant(participant_type=participant_type, sim=context.sim, target=target, **kwargs)
        if inventory_subject is None:
            return
        household_id = None
        if isinstance(inventory_subject, sims.household.Household):
            household_id = inventory_subject.id
        elif inventory_subject.is_sim:
            household_id = inventory_subject.sim_info.household_id
        else:
            household_id = inventory_subject.get_household_owner_id()
        if household_id is None:
            return
        household = services.household_manager().get(household_id)
        if household.home_zone_id == 0:
            return
        zone = services.current_zone()
        object_ids = build_buy.get_object_ids_in_household_inventory(household_id)
        objects = []
        for object_id in object_ids:
            obj = zone.find_object(object_id, include_household=True)
            obj = get_object_in_household_inventory(object_id, household_id)
            if not obj is None or not obj is None:
                if obj.is_sim:
                    pass
                elif not inst_or_cls.inventory_item_test or not inst_or_cls.inventory_item_test(obj):
                    pass
                else:
                    objects.append(obj)
                    yield obj

    @flexmethod
    def _get_objects_from_sim_inventory(cls, inst, participant_type, target, context, **kwargs):
        inst_or_cls = inst if inst is not None else cls
        inventory_subject = inst_or_cls.get_participant(participant_type=participant_type, sim=context.sim, target=target, **kwargs)
        if inventory_subject.inventory_component is not None:
            actor_sim = inst_or_cls.get_participant(participant_type=ParticipantType.Actor, sim=context.sim, target=target, **kwargs)
            actor_sim_info = actor_sim.sim_info if actor_sim is not None else None
            target_sim = inst_or_cls.get_participant(participant_type=ParticipantType.TargetSim, sim=context.sim, target=target, **kwargs)
            target_sim_info = target_sim.sim_info if target_sim is not None else None
            for obj in inventory_subject.inventory_component:
                if not inst_or_cls.inventory_item_test(obj):
                    pass
                else:
                    yield obj

    @flexmethod
    def _get_object_count(cls, inst, definition, target, context, **kwargs):
        inst_or_cls = inst if inst is not None else cls
        count = 0
        if inst_or_cls.use_household_inventory is not None:
            household_id = inst_or_cls._get_household_id_for_participant(target, context)
            if household_id is not None:
                count += len(find_objects_in_household_inventory([definition.id], household_id))
        if inst_or_cls.use_sim_inventory is not None:
            inventory_subject = inst_or_cls.get_participant(participant_type=inst_or_cls.use_sim_inventory, sim=context.sim, target=target, **kwargs)
            if inventory_subject.inventory_component is not None:
                count += inventory_subject.inventory_component.get_count(definition)
        return count

    @flexmethod
    def _get_household_id_for_participant(cls, inst, target, context, **kwargs):
        inst_or_cls = inst if inst is not None else cls
        if inst_or_cls.use_household_inventory is not None:
            inventory_subject = inst_or_cls.get_participant(participant_type=inst_or_cls.use_household_inventory, sim=context.sim, target=target, **kwargs)
            if inventory_subject is not None:
                if isinstance(inventory_subject, sims.household.Household):
                    return inventory_subject.id
                if isinstance(inventory_subject, ScriptObject):
                    if inventory_subject.is_sim:
                        return inventory_subject.sim_info.household_id
                    else:
                        return inventory_subject.get_household_owner_id()

class ObjectsInMultipleInventoriesObjectPickerInteraction(ObjectsInMultipleInventoriesMixin, ObjectPickerInteraction):

    @flexmethod
    def _get_objects_gen(cls, inst, *args, **kwargs):
        inst_or_cls = inst if inst is not None else cls
        yield from super(__class__, inst_or_cls)._get_objects_internal_gen(*args, **kwargs)

    def _on_picker_selected(self, dialog):
        if dialog.accepted:
            super()._on_picker_selected(dialog)

class ObjectsInMultipleInventoriesPurchasePickerInteraction(ObjectsInMultipleInventoriesMixin, PurchasePickerInteraction):
    INSTANCE_TUNABLES = {'continuation': OptionalTunable(description='\n            If enabled, you can tune a continuation to be pushed.\n            PickedObject will be the object that was selected\n            ', tunable=TunableContinuation(description='\n                If specified, a continuation to push on the chosen object.'), tuning_group=GroupNames.PICKERTUNING), 'max_selectable_in_rows': Tunable(description='\n            Max number that can be selected in each row, using the smallest of this number and number\n            avalable. If 0 or less, there is no maximum number.\n            ', tunable_type=int, default=0, tuning_group=GroupNames.PICKERTUNING), 'max_selectable_rows': Tunable(description='\n            Max number of rows that can be selected, if at least one item is purchased in a row, that row is considered\n            selected. If 0 or less, there is no maximum number.\n            ', tunable_type=int, default=0, tuning_group=GroupNames.PICKERTUNING), 'use_compressed_multiple_inventory_loot': Tunable(description='\n            If true, selected objects will remain compressed in inventory, and\n            can only be manipulated via compressed muiltiple inventory loots.\n            If false, selected object will be uncompressed into inventory, so \n            they may be accessed as PickedObjects.  This has performance \n            implications for both Gameplay and UI, so should only be used as a\n            stopgap, until an appropriate compressed multiple inventory loot\n            has been added, or if the number of selectable items is quite low.\n            ', tunable_type=bool, default=True, tuning_group=GroupNames.PICKERTUNING)}

    @flexmethod
    def _get_objects_gen(cls, inst, *args, **kwargs):
        inst_or_cls = inst if inst is not None else cls
        yield from super(__class__, inst_or_cls)._get_objects_internal_gen(*args, **kwargs)

    def _setup_dialog(self, dialog, **kwargs):
        purchase_picker_data = PurchasePickerData()
        self.delivery_method(self, purchase_picker_data)
        for obj in self._get_objects_gen(target=self.target, context=self.context, **kwargs):
            purchase_picker_data.add_definition_to_purchase(obj.definition, obj=obj)
        dialog.inventory_object_id = purchase_picker_data.inventory_owner_id_to_purchase_from
        dialog.object_id = purchase_picker_data.inventory_owner_id_to_purchase_to
        dialog.purchase_by_object_ids = False
        dialog.show_description = self.show_descriptions
        dialog.show_cost = False
        dialog.max_selectable_in_row = self.max_selectable_in_rows
        dialog.max_selectable_rows = self.max_selectable_rows
        dialog.show_description_tooltip = self.show_description_tooltip
        resolver = self.get_resolver()
        (multiplier, tooltip) = self.price_multiplier.get_multiplier_and_tooltip(resolver)
        for ((definition, custom_price), item_data) in purchase_picker_data.items_to_purchase.items():
            count = self._get_object_count(definition, self.target, self.context)
            if multiplier != 1:
                original_price = custom_price if custom_price is not None else definition.price
                custom_price = int(original_price*multiplier)
                tooltip = None
            row = PurchasePickerRow(def_id=definition.id, num_available=count, custom_price=custom_price, tags=definition.build_buy_tags, objects=item_data.objects, row_tooltip=tooltip, show_discount=self.show_discount)
            dialog.add_row(row)

    @classmethod
    def has_valid_choice(cls, target, context, **kwargs):
        for _ in cls._get_objects_internal_gen(target, context, **kwargs):
            return True
        return False

    def _on_picker_selected(self, dialog):
        if dialog.accepted:
            (def_ids, counts) = dialog.get_result_definitions_and_counts()
            purchase_picker_data = PurchasePickerData()
            self.delivery_method(self, purchase_picker_data)
            kwargs = {}
            for obj in self._get_objects_gen(target=self.target, context=self.context, **kwargs):
                purchase_picker_data.add_definition_to_purchase(obj.definition, obj=obj)
            picked_items = []
            for ((definition, _), item_data) in purchase_picker_data.items_to_purchase.items():
                objects_iter = iter(item_data.objects)
                obj = next(objects_iter, None)
                if obj.id in def_ids:
                    self._add_picked_items(picked_items, definition, counts[def_ids.index(obj.id)])
            if picked_items:
                self._push_continuations(picked_items)

    def _add_picked_items(self, picked_items, definition, total_count):
        if total_count <= 0:
            return
        items_added = 0
        if self.use_household_inventory is not None:
            household_id = self._get_household_id_for_participant(self.target, self.context)
            if household_id is not None:
                objects = find_objects_in_household_inventory([definition.id], household_id)
                items_added = len(objects)
                if self.use_compressed_multiple_inventory_loot:
                    picked_items.extend((obj_id, 1) for obj_id in objects[:total_count])
                else:
                    picked_items.extend(objects[:total_count])
                if items_added >= total_count:
                    return
        if self.use_sim_inventory is not None:
            inventory_subject = self.get_participant(participant_type=self.use_sim_inventory, sim=self.context.sim, target=self.target)
            inventory_component = inventory_subject.inventory_component
            if self.use_compressed_multiple_inventory_loot:
                for matching_object in inventory_component.get_items_with_definition_gen(definition):
                    count = min(matching_object.stack_count(), total_count - items_added)
                    items_added += count
                    picked_items.append((matching_object.id, count))
                    if items_added == total_count:
                        break
            else:
                objects_removed = []
                while items_added < total_count:
                    object_to_remove = inventory_component.get_item_with_definition(definition)
                    if inventory_component.try_remove_object_by_id(object_to_remove.id):
                        objects_removed.append(object_to_remove)
                        picked_items.append(object_to_remove.id)
                        items_added += 1
                    else:
                        break
                for object_to_readd in objects_removed:
                    inventory_subject.inventory_component.system_add_object(object_to_readd, compact=False)

    def _push_continuations(self, objs):
        if objs is not None and self.continuation is not None:
            self._push_picked_continuation(objs)

    def _push_picked_continuation(self, picked_items):
        if self.use_compressed_multiple_inventory_loot:
            self.interaction_parameters['compressed_multiple_inventory_items'] = picked_items
            self.push_tunable_continuation(self.continuation, compressed_multiple_inventory_items=picked_items, insert_strategy=QueueInsertStrategy.LAST)
        else:
            self.interaction_parameters['picked_item_ids'] = picked_items
            self.push_tunable_continuation(self.continuation, picked_item_ids=picked_items, insert_strategy=QueueInsertStrategy.LAST)

class PurchasePickerWithFailureOptionInteraction(PurchasePickerInteraction):
    INSTANCE_TUNABLES = {'failure_delivery_method': TunableVariant(description='\n            Where the objects purchased will be delivered if the interaction fails.\n            ', purchase_to_inventory=PurchaseToInventory(description="\n                Purchase the objects directly into a participant's inventory.\n                "), mailman_delivery=MailmanDelivery(description='\n                Deliver the objects by the mailman.\n                '), default='purchase_to_inventory', tuning_group=GroupNames.PICKERTUNING), 'purchase_outcome': TunableOutcome(description='\n            Outcome from the purchase. A SUCCESS outcome will deliver purchased items to the normal delivery_method\n            location. A FAILURE outcome will deliver the items to the failure_delivery_method location.\n            ', tuning_group=GroupNames.PICKERTUNING), 'purchase_failed_notification': OptionalTunable(description='\n            If enabled, a notification is displayed should the purchase picker\n            dialog be accepted, but the outcome is a failure.\n            ', tunable=TunableUiDialogNotificationSnippet(description='\n                The notification to show when the purchase picker dialog is\n                accepted, but the outcome is a failure.\n                '), tuning_group=GroupNames.PICKERTUNING)}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _setup_delivery_method(self, purchase_picker_data):
        self.purchase_outcome.decide(self, update_global_outcome_result=True)
        if self.global_outcome_result == OutcomeResult.SUCCESS:
            self.delivery_method(self, purchase_picker_data)
        else:
            self.failure_delivery_method(self, purchase_picker_data)

    def _on_picker_selected(self, dialog):
        if dialog.accepted:
            if self.purchase_notification is not None:
                if self.global_outcome_result == OutcomeResult.SUCCESS or self.purchase_failed_notification is None:
                    notification_dialog = self.purchase_notification(self.sim, resolver=self.get_resolver())
                else:
                    notification_dialog = self.purchase_failed_notification(self.sim, resolver=self.get_resolver())
                notification_dialog.show_dialog()
            sequence = self._build_outcome_sequence()
            services.time_service().sim_timeline.schedule(element_utils.build_element(sequence))
            if self.purchase_picker_data.delivery_method == PickerInteractionDeliveryMethod.SLOT_TO_PARENT:
                self._slot_created_objects_to_parent(dialog)
            elif self.loots_on_purchase:
                self.handle_loots(dialog)

    def build_outcome(self):
        pass

    def _build_outcome_sequence(self):
        target_sequence = None
        if self.target is not None:
            target_outcome = self.target.get_affordance_outcome(self)
            if target_outcome.has_content:
                target_sequence = target_outcome.build_elements(self, interaction_outcome=self.outcome)
        sequence = self.purchase_outcome.build_elements(self, update_global_outcome_result=True, send_telemetry=target_sequence is None)
        if target_sequence is not None:
            sequence = (sequence, target_sequence)
        return sequence
