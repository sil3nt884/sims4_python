import alarmsimport build_buyimport carryimport clockimport distributorimport event_testing.resolverimport event_testing.test_variantsimport randomimport servicesimport sims.sim_info_testsimport sims4.logimport sims4.resourcesimport situations.bouncer.bouncer_typesimport statistics.skill_testsimport travel_group.travel_group_testsimport ui.screen_slamfrom buffs.tunable import TunableBuffReferencefrom clock import ClockSpeedModefrom collections import namedtuplefrom distributor.ops import BuildBuyLockUnlockfrom event_testing.results import TestResultfrom interactions import ParticipantTypeActorTargetSimfrom interactions.base.super_interaction import SuperInteractionfrom interactions.utils.tunable_icon import TunableIconAllPacks, TunableIconfrom relationships.relationship_bit import RelationshipBitfrom sims.sim_info_types import Agefrom sims4.localization import TunableLocalizedString, TunableLocalizedStringFactoryfrom sims4.tuning.instances import HashedTunedInstanceMetaclassfrom sims4.tuning.tunable import TunableList, TunableReference, TunableTuple, Tunable, TunableResourceKey, TunableSimMinute, TunableEnumEntry, OptionalTunable, TunableVariant, HasTunableReference, TunableEntitlement, HasTunableSingletonFactory, AutoFactoryInit, TunableSet, TunableEnumWithFilter, TunableRange, TunableMapping, TunablePackSafeReferencefrom sims4.tuning.tunable_base import GroupNamesfrom sims4.utils import classpropertyfrom situations.situation_goal_tracker_tuning import TunableSituationGoalTrackerVariant, FORCE_USER_FACING_GOAL_TRACKERSfrom situations.base_situation import BaseSituation, EnsembleOptionfrom situations.situation_goal_tuning_mixin import SituationGoalTuningMixinfrom situations.situation_job import SituationJobfrom situations.situation_level_data_tuning_mixin import SituationLevelDataTuningMixinfrom situations.situation_serialization import GoalTrackerTypefrom situations.situation_time_jump import TunableSituationTimeJumpVariantfrom situations.situation_travel_behavior import TunableSituationTravelRequestBehaviorVariantfrom situations.situation_tuning import SituationStyleDatafrom situations.situation_types import SituationCategoryUid, SituationCreationUIOption, SituationDisplayStyle, SituationDisplayTypefrom tag import Tagfrom tunable_multiplier import TunableMultiplierfrom ui.ui_dialog import UiDialogOkCancel, UiEndSituationDialogOkCancelfrom ui.ui_dialog_notification import UiDialogNotificationlogger = sims4.log.Logger('Situations')
class TunableSituationInitiationTestVariant(TunableVariant):

    def __init__(self, description='A single tunable test.', **kwargs):
        super().__init__(test_initiating_sim_against_filter=sims.sim_info_tests.FilterTest.TunableFactory(description='\n            Test the sim attempting to initiate a situation against a specific\n            filter.  Passes as long as that sim matches the filter.\n            ', locked_args={'filter_target': None, 'relative_sim': ParticipantTypeActorTargetSim.Actor}), test_all_sims_against_filter=sims.sim_info_tests.FilterTest.TunableFactory(description='\n            Test all sims to see if there are any sims that match the filter.\n            Passes if any sims match the filter.\n            ', locked_args={'filter_target': None, 'relative_sim': ParticipantTypeActorTargetSim.Actor}), statistic=event_testing.statistic_tests.StatThresholdTest.TunableFactory(participant_type_override=(ParticipantTypeActorTargetSim, ParticipantTypeActorTargetSim.Actor)), skill_tag=statistics.skill_tests.SkillTagThresholdTest.TunableFactory(participant_type_override=(ParticipantTypeActorTargetSim, ParticipantTypeActorTargetSim.Actor)), sim_info=sims.sim_info_tests.SimInfoTest.TunableFactory(participant_type_override=(ParticipantTypeActorTargetSim, ParticipantTypeActorTargetSim.Actor), locked_args={'can_age_up': None}), trait=sims.sim_info_tests.TraitTest.TunableFactory(participant_type_override=(ParticipantTypeActorTargetSim, ParticipantTypeActorTargetSim.Actor)), unlock=event_testing.test_variants.TunableUnlockedTest(unlock_type_override={'allow_achievment': False}), travel_group=travel_group.travel_group_tests.TravelGroupTest.TunableFactory(locked_args={'participant': ParticipantTypeActorTargetSim.Actor}), region=event_testing.test_variants.RegionTest.TunableFactory(), description=description, **kwargs)

class TunableSituationInitiationSet(event_testing.tests.TestListLoadingMixin):
    DEFAULT_LIST = event_testing.tests.TestList()

    def __init__(self, description=None):
        if description is None:
            description = 'A list of tests.  All tests must succeed to pass the TestSet.'
        super().__init__(description=description, tunable=TunableSituationInitiationTestVariant())

class TunableNPCHostedPlayerTestVariant(TunableVariant):

    def __init__(self, description='A single tunable test.', **kwargs):
        super().__init__(statistic=event_testing.statistic_tests.StatThresholdTest.TunableFactory(participant_type_override=(ParticipantTypeActorTargetSim, ParticipantTypeActorTargetSim.Actor), locked_args={'tooltip': None}), skill_tag=statistics.skill_tests.SkillTagThresholdTest.TunableFactory(participant_type_override=(ParticipantTypeActorTargetSim, ParticipantTypeActorTargetSim.Actor), locked_args={'tooltip': None}), sim_info=sims.sim_info_tests.SimInfoTest.TunableFactory(participant_type_override=(ParticipantTypeActorTargetSim, ParticipantTypeActorTargetSim.Actor), locked_args={'tooltip': None, 'can_age_up': None}), trait=sims.sim_info_tests.TraitTest.TunableFactory(participant_type_override=(ParticipantTypeActorTargetSim, ParticipantTypeActorTargetSim.Actor), locked_args={'tooltip': None}), unlock=event_testing.test_variants.TunableUnlockedTest(unlock_type_override={'allow_achievment': False}, locked_args={'tooltip': None}), user_facing_situation_running_test=event_testing.test_variants.TunableUserFacingSituationRunningTest(), region_test=event_testing.test_variants.RegionTest.TunableFactory(), description=description, **kwargs)

class TunableNPCHostedPlayerTestSet(event_testing.tests.TestListLoadingMixin):
    DEFAULT_LIST = event_testing.tests.TestList()

    def __init__(self, description=None, **kwargs):
        if description is None:
            description = 'A list of tests.  All tests must succeed to pass the TestSet.'
        super().__init__(description=description, tunable=TunableNPCHostedPlayerTestVariant(), **kwargs)

class TunableMainGoalVisibilityTestVariant(TunableVariant):

    def __init__(self, description='A single tunable test.', **kwargs):
        super().__init__(situation_running_test=event_testing.test_variants.TunableSituationRunningTest(locked_args={'participant': None, 'check_for_initiating_sim': False}), description=description, default='situation_running_test', **kwargs)

class TargetedSituationSpecific(HasTunableSingletonFactory, AutoFactoryInit):
    FACTORY_TUNABLES = {'target_job': SituationJob.TunableReference(description='\n            This is the job for the target sim, the one being asked.\n            After a player selects a target sim they will\n            be given a list of situations to choose from. Only situations\n            in which their selected sim matches the filter on this job will\n            be included.\n    \n            This field is required for targeted situations.\n            '), 'actor_job': SituationJob.TunableReference(description='\n            This is the job for the actor sim, the one doing the asking.\n            A sim will only be able to initiate this situation\n            if they match the filter in this job and pass the \n            initiating_sim_tests (another tuning field on situations).\n            It will be common for the filter in this job to be None.\n            \n            This field is required for targeted situations.\n            ')}
NPCHostedSituationResult = namedtuple('NPCHostedSituationResult', ('player_sim_info', 'host_sim_info', 'failure_reason'))
class Situation(SituationGoalTuningMixin, SituationLevelDataTuningMixin, BaseSituation, HasTunableReference, metaclass=HashedTunedInstanceMetaclass, manager=services.get_instance_manager(sims4.resources.Types.SITUATION)):
    INSTANCE_SUBCLASSES_ONLY = True
    NPC_HOSTED_SITUATION_AGE_WEIGHTING = TunableMapping(description='\n        A map of ages to weights when determining which sim in the household\n        will be selected to receive an invitation.\n        ', key_name='age', key_type=TunableEnumEntry(description='\n            The age of a possible invitee that will be mapped to a weight.\n            ', tunable_type=Age, default=Age.ADULT), value_name='weight', value_type=TunableRange(description='\n            The weight a sim of this age will be chosen to have an event run\n            on them.\n            ', tunable_type=int, default=1, minimum=1))
    INSTANCE_TUNABLES = {'category': TunableEnumEntry(description='\n            The Category that the Situation belongs to.\n            ', tunable_type=SituationCategoryUid, default=SituationCategoryUid.DEFAULT, tuning_group=GroupNames.UI), 'load_open_street_situation_with_selectable_sim': Tunable(description='\n            If the situation has selectable sims, set to True to ensure the\n            situation can load from the open street, False otherwise.\n            \n            Note: The Serialization Option also determines save/load strategy.\n            Check with GPE to verify the situation save/load behavior.\n            ', tunable_type=bool, default=False), '_display_name': TunableLocalizedString(description='\n            Display name for situation\n            ', allow_none=True, tuning_group=GroupNames.UI), 'situation_description': TunableLocalizedString(description='\n            Situation Description\n            ', allow_none=True, tuning_group=GroupNames.UI), 'entitlement': OptionalTunable(description='\n            If enabled, this situation is locked by an entitlement. Otherwise,\n            this situation is available to all players.\n            ', tunable=TunableEntitlement(description='\n                Entitlement required to plan this event.\n                ', tuning_group=GroupNames.UI)), '_default_job': TunableReference(description='\n            The default job for Sims in this situation\n            ', manager=services.get_instance_manager(sims4.resources.Types.SITUATION_JOB), allow_none=True), '_resident_job': SituationJob.TunableReference(description='\n            The job to assign to members of the host sims household.\n            Make sure to use the in_family filter term in the filter\n            of the job you reference here.\n            It is okay if this tunable is None.\n            ', allow_none=True), '_icon': TunableResourceKey(description='\n            Icon to be displayed in the situation UI.\n            ', resource_types=sims4.resources.CompoundTypes.IMAGE, default=None, allow_none=True, tuning_group=GroupNames.UI), 'calendar_icon': TunableIconAllPacks(description='\n            Icon to be displayed in the calendar UI.\n            ', allow_none=True, tuning_group=GroupNames.UI), 'calendar_alert_description': OptionalTunable(description='\n            If tuned, there will be a calendar alert description.\n            ', tunable=TunableLocalizedString(description='\n                Description that shows up in the calendar alert.\n                ')), 'job_display_ordering': OptionalTunable(description='\n            An optional list of the jobs in the order you want them displayed\n            in the Plan an Event UI.\n            ', tunable=TunableList(tunable=TunableReference(manager=services.get_instance_manager(sims4.resources.Types.SITUATION_JOB))), tuning_group=GroupNames.UI), 'end_situation_dialog': OptionalTunable(description='\n            An optional UI Dialog to use when ending a user facing situation\n            ', tunable=UiEndSituationDialogOkCancel.TunableFactory(description='\n                The message that will be displayed when this situation is\n                requested to end by the player\n\n                Title and Text for end situation dialog can be set\n                as well as Text Cancel and Text Ok for tooltips of\n                OK/Cancel buttons or as the button text when not set\n                as Special Dialog\n                \n                Special Situations such as Career events also require \n                tokens for displaying the time for the situation job.\n                Additionally an alternate option is available to \n                "Stay late" which extends the job sim hours duration tuned\n                in text_alt_action of UiEndSituationDialogOkCancel\n                '), tuning_group=GroupNames.UI), 'medal_icon_override': OptionalTunable(description='\n            If enabled, when the situation is shown in social event UI, the icon \n            will be the tuned icon instead of showing the highest medal icon for \n            the situation.\n            ', tunable=TunableIcon(), tuning_group=GroupNames.UI), 'scoring_lock_reason': OptionalTunable(description="\n            If enabled, when the situation is shown in social event UI, the \n            'Goaled Event' checkbox will be greyed out and can't be changed.\n            This reason text will be shown as a tooltip.\n            ", tunable=TunableLocalizedString(), tuning_group=GroupNames.UI), 'recommended_job_object_notification': UiDialogNotification.TunableFactory(description='\n            The notification that is displayed when one or more recommended objects\n            for a job are missing.\n            ', locked_args={'text': None}), 'recommended_job_object_text': TunableLocalizedStringFactory(description='\n            The text of the notification that is displayed when one or more recommended\n            objects for a job are missing.\n            \n            The localization tokens for the Text field are:\n            {0.String} = bulleted list of strings for the missing objects\n            ', allow_none=True), '_buff': TunableBuffReference(description='\n            Buff that will get added to sim when commodity is at this\n            current state.\n            ', allow_none=True), '_cost': Tunable(description='\n            The cost of this situation\n            ', tunable_type=int, default=0), 'exclusivity': TunableEnumEntry(description='\n            Defines the exclusivity category for the situation which is used to prevent sims assigned\n            to this situation from being assigned to situations from categories excluded by this\n            category and vice versa.\n            ', tunable_type=situations.bouncer.bouncer_types.BouncerExclusivityCategory, default=situations.bouncer.bouncer_types.BouncerExclusivityCategory.NORMAL), '_main_goal_visibility_test': OptionalTunable(description='\n            If enabled then the main goal of the situation will not be\n            visible until this test passes.  If the state of this test no\n            longer becomes true then the main gaol will not become\n            invisible again.\n            \n            Ex. A hospital emergency starting triggers the visiblity of the\n            main goal within the active career event situation.\n            \n            IMPORTANT: The nature of this test can cause performance\n            problems.\n            ', tunable=TunableMainGoalVisibilityTestVariant(), tuning_group=GroupNames.GOALS), 'force_invite_only': Tunable(description='\n            If True, the situation is invite only. Otherwise, it is not.\n            For a date situation, this would be set to True.\n            ', tunable_type=bool, default=False), 'creation_ui_option': TunableEnumEntry(description='\n            Determines if the situation can be created from the Plan Event\n            UI triggered from the phone.\n            \n            NOT_AVAILABLE - situation is not available in the creation UI.\n            \n            AVAILABLE - situation is available in the creation UI.\n            \n            DEBUG_AVAILABLE - situation is only available in the UI if\n            you have used the |situations.allow_debug_situations command\n            \n            SPECIFIED_ONLY - situation is available in the creation UI if\n            that UI is tuned to only look at a subset of situations.\n            ', tunable_type=SituationCreationUIOption, default=SituationCreationUIOption.AVAILABLE, tuning_group=GroupNames.UI), 'activity_selection': OptionalTunable(description='\n            If enabled, allows tuning activities that can be selected in the Situation Creation UI. Those activities\n            will be displayed during the Situation Creation.\n            ', tunable=TunableTuple(description='\n                Activities that can be chosen for this Situation.\n                ', available_activities=TunableSet(description='\n                    A set of available activities from which the player can choose.\n                    ', tunable=TunableReference(description='\n                        An available activity for this Situation.\n                        ', manager=services.get_instance_manager(sims4.resources.Types.HOLIDAY_TRADITION), class_restrictions=('SituationActivity',), pack_safe=True)), required_activities=OptionalTunable(description='\n                    If enabled, allows tuning a set of Situation Activities that are required for this Situation.\n                    ', tunable=TunableSet(description='\n                        A set of activities that will be required for this Situation.\n                        ', tunable=TunableReference(description='\n                            An activity required for this Situation.\n                            ', manager=services.get_instance_manager(sims4.resources.Types.HOLIDAY_TRADITION), class_restrictions=('SituationActivity',), pack_safe=True))))), 'customizable_style': OptionalTunable(description='\n            If enabled, allows the player to customize the guest attire and outfits of certain roles.\n            ', tunable=TunablePackSafeReference(description='\n                A references to SituationStyleData that defines the style options for this Situation.\n                ', manager=services.get_instance_manager(sims4.resources.Types.SNIPPET), class_restrictions=(SituationStyleData,))), 'display_special_object': OptionalTunable(description='\n            If enabled, this will show a special object in the Style portion of the situation creation UI.\n            ', tunable=TunableTuple(description='\n                Information about displaying the special object.\n                ', help_tooltip=TunableLocalizedString(description='\n                   The tooltip on the help icon for the Speical Object Display.\n                   '), no_object_icon=TunableIcon(description='\n                    The icon to show if no Special Object has been selected yet.\n                    '), no_object_label=TunableLocalizedString(description='\n                    The label to show if no Special Object has been selected. This will show where the object name would\n                    otherwise be.\n                    '))), 'audio_sting_on_start': TunableResourceKey(description='\n            The sound to play when the Situation starts.\n            ', default=None, resource_types=(sims4.resources.Types.PROPX,), tuning_group=GroupNames.AUDIO), 'background_audio': OptionalTunable(description='\n            If enabled then we will play audio in the background while this\n            user facing situation is running.\n            ', tunable=TunableResourceKey(description='\n                Audio that will play throughout the situation in the background\n                and will end at the end of the situation.\n                ', default=None, resource_types=(sims4.resources.Types.PROPX,)), tuning_group=GroupNames.AUDIO), 'duration': TunableSimMinute(description='\n            How long the situation will last in sim minutes. 0 means forever.\n            ', default=60), 'duration_randomizer': TunableSimMinute(description="\n            A random time between 0 and this tuned time will be added to the\n            situation's duration.\n            ", default=0, minimum=0), 'max_participants': Tunable(description='\n            Maximum number of Sims the player is allowed to invite to this Situation.\n            ', tunable_type=int, default=16, tuning_group=GroupNames.UI), '_initiating_sim_tests': TunableSituationInitiationSet('\n            A set of tests that will be run on a sim attempting to initiate a\n            situation.  If these tests do not pass than this situation will not\n            be able to be chosen from the UI.\n            '), 'targeted_situation': OptionalTunable(description='\n            If enabled, the situation can be used as a targeted situation,\n            such as a Date.\n            ', tunable=TargetedSituationSpecific.TunableFactory()), 'compatible_venues': TunableList(description='\n            In the Plan an Event UI, lots that are these venues will be\n            added to the list of lots on which the player can throw the\n            event. The player can always choose their own lot and lots of\n            their guests.\n            ', tunable=TunableReference(manager=services.get_instance_manager(sims4.resources.Types.VENUE), pack_safe=True, tuning_group=GroupNames.VENUES)), 'venue_region_must_be_compatible': Tunable(description='\n            If enabled, venues will only be considered if they are in a\n            region that is compatible with the current region (regions with\n            at least one shared tag).\n            ', tunable_type=bool, default=False), 'venue_invitation_message': OptionalTunable(description='\n            If enabled, show a dialog when the situation tries to start on a\n            venue.\n            ', tunable=UiDialogOkCancel.TunableFactory(description="\n                The message that will be displayed when this situation tries to\n                start for the venue.\n                \n                Two additional tokens are passed in: the situation's name and\n                the job's name.\n                "), tuning_group=GroupNames.VENUES), 'venue_situation_player_job': TunableReference(description="\n            The job that the player will be put into when they join in a\n            user_facing special situation at a venue.\n            \n            Note: This must be tuned to allow this situation to be in a\n            venue's special event schedule. The job also must be a part of\n            the Situation.\n            ", manager=services.get_instance_manager(sims4.resources.Types.SITUATION_JOB), allow_none=True, tuning_group=GroupNames.VENUES), 'tags': TunableSet(description='\n            Tags for arbitrary groupings of situation types.\n            ', tunable=TunableEnumWithFilter(tunable_type=Tag, filter_prefixes=['situation'], default=Tag.INVALID, pack_safe=True)), '_relationship_between_job_members': TunableList(description="\n            Whenever a sim joins either job_x or job_y, the sim is granted\n            the tuned relationship bit with every sim in the other job. The\n            relationship bits are added and remain as long as the sims are\n            assigned to the tuned pair of jobs.\n            \n            This creates a relationship between the two sims if one does not exist.\n            \n            E.g. Date situation uses this feature to add bits to the sims'\n            relationship in order to drive autonomous behavior during the\n            lifetime of the date.\n            ", tunable=TunableTuple(job_x=SituationJob.TunableReference(), job_y=SituationJob.TunableReference(), relationship_bits_to_add=TunableSet(description='\n                    A set of RelationshipBits to add to relationship between the sims.\n                    ', tunable=RelationshipBit.TunableReference())), tuning_group=GroupNames.TRIGGERS), '_implies_greeted_status': Tunable(description='\n            If checked then a sim, in this situation, on a residential lot\n            they do not own, is consider greeted on that lot.\n            \n            Greeted status related design documents:\n            //depot/Sims4Projects/docs/Design/Gameplay/HouseholdState/Ungreeted_Lot_Behavior_DD.docx\n            //depot/Sims4Projects/docs/Design/Gameplay/Simulation/Active Lot Changing Edge Cases.docx\n            ', tunable_type=bool, default=False), 'screen_slam_no_medal': OptionalTunable(description='\n            Screen slam to show when this situation is completed and no\n            medal is earned.\n            Localization Tokens: Event Name - {0.String}, Medal Awarded - \n            {1.String}\n            ', tunable=ui.screen_slam.TunableScreenSlamSnippet()), 'screen_slam_bronze': OptionalTunable(description='\n            Screen slam to show when this situation is completed and a\n            bronze medal is earned.\n            Localization Tokens: Event Name - {0.String}, Medal Awarded - \n            {1.String}\n            ', tunable=ui.screen_slam.TunableScreenSlamSnippet()), 'screen_slam_silver': OptionalTunable(description='\n            Screen slam to show when this situation is completed and a\n            silver medal is earned.\n            Localization Tokens: Event Name - {0.String}, Medal Awarded - \n            {1.String}\n            ', tunable=ui.screen_slam.TunableScreenSlamSnippet()), 'screen_slam_gold': OptionalTunable(description='\n            Screen slam to show when this situation is completed and a\n            bronze medal is earned.\n            Localization Tokens: Event Name - {0.String}, Medal Awarded - \n            {1.String}\n            ', tunable=ui.screen_slam.TunableScreenSlamSnippet()), 'time_jump': TunableSituationTimeJumpVariant(description='\n            Determine how the situation handles the zone time being different on\n            load than what it was on save. This is primarily useful for\n            commercial venue background situations and career event situations.\n            ', tuning_group=GroupNames.SPECIAL_CASES), 'can_remove_sims_from_work': Tunable(description='\n            If checked then this situation will cause sims to end work early\n            when they are on the guest list. If unchecked, it will not. This\n            option will not affect active career situations or NPC career\n            situations like tending the bar.\n            ', tunable_type=bool, default=True, tuning_group=GroupNames.SPECIAL_CASES), '_survives_active_household_change': Tunable(description='\n            If checked then this situation will load even if the active\n            household has changed since it was saved. It will attempt to\n            restore Sims to their saved jobs. This is primarily useful for\n            commercial venue background situations.\n            ', tunable_type=bool, default=False, tuning_group=GroupNames.SPECIAL_CASES), '_maintain_sims_consistency': Tunable(description="\n            If checked, Sims in the saved situation that were pushed home \n            because they had been saved in the zone for many Sim hours will \n            be back. Otherwise, we will find replacement.\n            \n            Ex. We don't want to replace Butler with new Sim if previous\n            Butler is no longer in the lot.\n            ", tunable_type=bool, default=False, tuning_group=GroupNames.SPECIAL_CASES), '_hidden_scoring_override': Tunable(description='\n            If checked then even if this situation has its scoring disabled it\n            still will count score and provide rewards to the player.\n            ', tunable_type=bool, default=False, tuning_group=GroupNames.SPECIAL_CASES), '_is_unique': Tunable(description='\n            If set, only a single instance of this situation can exist at once\n            in a given zone.\n            ', tunable_type=bool, default=False, tuning_group=GroupNames.SPECIAL_CASES), '_ensemble': OptionalTunable(description='\n            If enabled then we will keep Sims in a specific ensemble for the\n            duration of the situation.\n            ', tunable=TunableTuple(description='\n                Tunables for putting Sims into ensembles.\n                ', ensemble_type=TunablePackSafeReference(description='\n                    The type of Ensemble to put the sims into.\n                    ', manager=services.get_instance_manager(sims4.resources.Types.ENSEMBLE)), remove_before_add=Tunable(description='\n                    If checked then before we add the Sim to the ensemble we\n                    will remove them from from ensembles of the specified type.\n                    This can be used to force Sims into only an ensemble of\n                    Sims in this situation.\n                    ', tunable_type=bool, default=False), ignore_situation_removal=Tunable(description='\n                    If checked then we will not remove the Sim from the\n                    ensemble of this type when the Sim is removed from the\n                    situation.\n                    ', tunable_type=bool, default=True), ensemble_option=TunableEnumEntry(description='\n                    How we want to add Sims to an ensemble:\n                    ONLY_WITHIN_SITUATION: Put the Sims in this situation into\n                    an ensemble of this type.  Every time a sim is added we\n                    try and do this so if the user destroys the ensemble and\n                    then another Sim is spawned for it the ensemble will be\n                    recreated.\n                    \n                    ADD_TO_ACTIVE_HOUSEHOLD: Every time a Sim is spawned for\n                    this situation they are put into an ensemble with the\n                    instanced active household.  This is useful if you want to\n                    put the Sims in a situation with someone who is not in it. \n                    \n                    ADD_TO_HOST: Every time a Sim is spawned for this situation\n                    they are put into an ensemble with the host of the\n                    situation.  This is useful if you want to put the Sims in\n                    a situation with someone who is not in it.\n                    ', tunable_type=EnsembleOption, default=EnsembleOption.ONLY_WITHIN_SITUATION)), tuning_group=GroupNames.SPECIAL_CASES), 'blocks_super_speed_three': Tunable(description='\n            If enabled, this situation will block any requests to go into super\n            speed 3.\n            ', tunable_type=bool, default=False), 'travel_request_behavior': TunableSituationTravelRequestBehaviorVariant(description='\n            Define how this situation handles incoming travel requests from\n            other situations when running as user-facing.\n            '), 'allowed_in_super_speed_3': Tunable(description="\n            If enabled, this situation will skip the super speed 3 rules and\n            be allowed to trigger at that speed.\n            This will only affect walkby's as they are the only restricted\n            by speed 3.\n            ", tunable_type=bool, default=False), 'should_send_on_lot_home_in_super_speed_3': Tunable(description='\n            If enabled, on_lot sims in this situation will not prevent SS3.  If\n            SS3 is triggered they will be sent home.\n            ', tunable_type=bool, default=False), 'can_be_sent_home_in_super_speed_3': Tunable(description='\n            If disabled, this sim will never be sent home by a transition into SS3, despite being on the lot or not.\n            ', tunable_type=bool, default=True), 'super_speed3_replacement_speed': OptionalTunable(description='\n            If enabled and this situation blocks super speed 3, the situation will attempt to request\n            this speed if it is running when super speed 3 tries to kick in.\n            ', tunable=TunableEnumEntry(tunable_type=ClockSpeedMode, invalid_enums=(ClockSpeedMode.PAUSED, ClockSpeedMode.INTERACTION_STARTUP_SPEED, ClockSpeedMode.SUPER_SPEED3), default=ClockSpeedMode.SPEED3)), 'weight_multipliers': TunableMultiplier.TunableFactory(description="\n            Tunable tested multiplier to apply to any weight this situation\n            might have as part of a Situation Curve. These multipliers will be\n            applied globally anywhere this situation is tuned as part of a\n            situation curve (i.e. Walkby Tuning) so it should only be used in\n            cases where you ALWAYS want this multiplier applied.\n            \n            NOTE: You can still tune more multipliers on the individual walk by\n            instances. The multipliers will all stack together.\n            \n            *IMPORTANT* The only participants that work are ones\n            available globally, such as Lot and ActiveHousehold. Only\n            use these participant types or use tests that don't rely\n            on any, such as testing all objects via Object Criteria\n            test or testing active zone with the Zone test.\n            ", locked_args={'base_value': 1}), 'disallows_curfew_violation': Tunable(description='\n            If this is checked then the Sim is unable to violate curfew while\n            in the situation. If this is not checked then the Sim can vioalte\n            curfew as normal.\n            ', tunable_type=bool, default=False), 'suppress_scoring_progress_bar': Tunable(description='\n            If this is checked, UI will no longer show the scoring progress bar\n            and instead show the situation name in its stead.\n            ', tunable_type=bool, default=False, tuning_group=GroupNames.UI), 'situation_end_time_string': OptionalTunable(description='\n            When disabled the situation end time will not be shown. When enabled the situation end\n            time will be displayed above the score bar. The string displayed will be the tuned\n            string.\n            ', tunable=TunableLocalizedStringFactory(description='\n                The string to display as the situation end time string.\n                '), enabled_by_default=True, enabled_name='show_end_time', disabled_name='suppress_end_time', tuning_group=GroupNames.UI), 'cancel_tooltip_override': OptionalTunable(description='\n            When enabled will override the default tooltip text for the cancel button which is based on the\n            situation display type.\n            ', tunable=TunableLocalizedStringFactory(description='\n                The string to display as the tooltip.\n                '), tuning_group=GroupNames.UI), 'show_timer_in_scored_situation': Tunable(description='\n            If this is checked, then the situation timer will display in scored\n            situations.\n            ', tunable_type=bool, default=False, tuning_group=GroupNames.UI), 'highlight_first_incomplete_minor_goal': Tunable(description='\n            If this is checked, we will tell user-facing Situation UI \n            to highlight the first uncompleted minor goal set.\n            \n            Note that gameplay currently does not guard against being able \n            to complete the other goal sets in the situation currently, \n            so the goalsets should be tuned in such a manner \n            that they do not overlap.\n            ', tunable_type=bool, default=False, tuning_group=GroupNames.UI), 'situation_display_type_override': OptionalTunable(description='\n            Tune to override the value of the situation display type. By default,\n            this is set to be NORMAL on base situations.\n            ', tunable=TunableEnumEntry(description='\n                The display type used by UI to determine the Situation Display format.\n                ', tunable_type=SituationDisplayType, default=SituationDisplayType.NORMAL, tuning_group=GroupNames.UI)), '_use_spawner_tags_on_travel': Tunable(description='\n            If checked the situation will spawn sims according to its job \n            spawner tags instead of always defaulting to the player Arrival\n            spawner.\n            ', tunable_type=bool, default=False), 'disabled_interaction_tooltip': OptionalTunable(description='\n            If enabled, this is the text that will appear as a flyaway when the\n            player attempts to start an interaction while this situation is in\n            active.\n            ', tunable=TunableLocalizedStringFactory(description='\n                The flyaway text for the disabled interaction.\n                ')), 'park_interactions_on_SS3': TunableList(description='\n            If any interaction tuned on this list, we will push a random interaction from \n            this list to all NPC sims in this situation so they are allowed to be on lot\n            running these interactions during SS3.\n            ', tunable=SuperInteraction.TunableReference(pack_safe=True)), 'display_style': TunableEnumEntry(description='\n            The style overlay to apply to this situation.\n            ', tunable_type=SituationDisplayStyle, default=SituationDisplayStyle.DEFAULT, tuning_group=GroupNames.UI), 'build_buy_lock_reason': OptionalTunable(description='\n            If enabled then build buy will be disabled during this situation.\n            ', tunable=TunableLocalizedString(description='\n                The reason build buy is locked. For this case, it is because\n                build buy is not allowed during active career. Used on the disabled\n                buildbuy button in the HUD.\n                ')), 'goal_tracker_type': TunableSituationGoalTrackerVariant(description='\n            Set the goal tracker type used on this situation.\n            ', tuning_group=GroupNames.GOALS), 'run_carry_fixup_on_destroy': Tunable(description='\n            If True, we will run carry fixup commands on all situation sims\n            when the situation is being destroyed.\n            \n            For example, we set this to True on situation_Career_InteriorDecorator_HideClients,\n            so interior decorator clients will come back with their infants being held. \n            ', tunable_type=bool, default=False, tuning_group=GroupNames.SPECIAL_CASES)}
    SITUATION_SCORING_REMOVE_INSTANCE_TUNABLES = ('main_goal', '_main_goal_visibility_test', 'minor_goal_chains', 'main_goal_audio_sting', 'goal_sub_text', 'goal_button_text', 'highlight_first_incomplete_minor_goal', 'suppress_scoring_progress_bar', '_level_data', 'screen_slam_gold', 'screen_slam_silver', 'screen_slam_bronze', 'screen_slam_no_medal')
    SITUATION_START_FROM_UI_REMOVE_INSTANCE_TUNABLES = ('_cost', 'compatible_venues', 'venue_invitation_message', 'venue_situation_player_job', 'category', 'max_participants', '_initiating_sim_tests', '_icon', 'entitlement', 'job_display_ordering')
    SITUATION_USER_FACING_REMOVE_INSTANCE_TUNABLES = ('_display_name', 'end_situation_dialog', 'travel_request_behavior', 'recommended_job_object_notification', 'recommended_job_object_text', 'situation_description')
    NON_USER_FACING_REMOVE_INSTANCE_TUNABLES = ('_buff', 'targeted_situation', '_resident_job', '_relationship_between_job_members', 'audio_sting_on_start', 'background_audio', 'force_invite_only') + SITUATION_SCORING_REMOVE_INSTANCE_TUNABLES + SITUATION_START_FROM_UI_REMOVE_INSTANCE_TUNABLES + SITUATION_USER_FACING_REMOVE_INSTANCE_TUNABLES
    SITUATION_EVENT_REMOVE_INSTANCE_TUNABLES = ('_buff', '_cost', 'venue_invitation_message', 'venue_situation_player_job', 'category', 'main_goal', '_main_goal_visibility_test', 'minor_goal_chains', 'goal_sub_text', 'goal_button_text', 'highlight_first_incomplete_minor_goal', 'suppress_scoring_progress_bar', 'max_participants', '_initiating_sim_tests', '_icon', 'targeted_situation', '_resident_job', 'situation_description', 'job_display_ordering', 'entitlement', '_relationship_between_job_members', 'main_goal_audio_sting', 'audio_sting_on_start', 'background_audio', '_level_data', '_display_name', 'end_situation_dialog', 'screen_slam_gold', 'screen_slam_silver', 'screen_slam_bronze', 'screen_slam_no_medal', 'force_invite_only', 'recommended_job_object_notification', 'recommended_job_object_text', 'travel_request_behavior')

    @classmethod
    def _tuning_loaded_callback(cls):
        cls.situation_level_data = SituationLevelDataTuningMixin.get_aggregated_situation_level_data(cls._level_data)

    @classmethod
    def _verify_tuning_callback(cls):
        if cls._resident_job is not None and cls._resident_job.filter is None:
            logger.error('Resident Job: {} has no filter,', cls._resident_job, owner='manus')
        if cls.targeted_situation is not None and (cls.targeted_situation.target_job is None or cls.targeted_situation.actor_job is None):
            logger.error('target_job and actor_job are required if targeted_situation is enabled.', owner='manus')
        tuned_jobs = frozenset(cls.get_tuned_jobs())
        for job_relationships in cls.relationship_between_job_members:
            if job_relationships.job_x not in tuned_jobs:
                logger.error('job_x: {} has relationship tuning but is not functionally used in situation {}.', job_relationships.job_x, cls, owner='manus')
            if job_relationships.job_y not in tuned_jobs:
                logger.error('job_y: {} has relationship tuning but is not functionally used in situation {}.', job_relationships.job_y, cls, owner='manus')
            if len(job_relationships.relationship_bits_to_add) == 0:
                logger.error("relationship_bits_to_add cannot be empty for situation {}'s job pairs {} and {}.", cls, job_relationships.job_x, job_relationships.job_y, owner='manus')
            else:
                for bit in job_relationships.relationship_bits_to_add:
                    if bit is None:
                        logger.error("relationship_bits_to_add cannot contain empty bit for situation {}'s job pairs {} and {}.", cls, job_relationships.job_x, job_relationships.job_y, owner='manus')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._duration_alarm_handle = None
        self._goal_tracker = None
        self._dynamic_goals = self._seed.extra_kwargs.get('dynamic_goals', None)

    @classproperty
    def allow_user_facing_goals(cls):
        (goal_tracker_type, _) = cls.goal_tracker_type()
        force_user_facing_goals_from_tuned_tracker = goal_tracker_type in FORCE_USER_FACING_GOAL_TRACKERS
        return cls.main_goal is not None or (len(cls.minor_goal_chains) > 0 or force_user_facing_goals_from_tuned_tracker)

    def get_main_goal(self, **kwargs):
        if self.main_goal is not None:
            return self.main_goal(**kwargs)
        else:
            return

    def get_main_goal_audio_sting(self):
        return self.main_goal_audio_sting

    def get_minor_goal_chains(self):
        return self.minor_goal_chains

    def get_goal_sub_text(self):
        return self.goal_sub_text

    def get_goal_button_text(self):
        return self.goal_button_text

    @property
    def is_goal_button_enabled(self):
        return True

    @property
    def situation_display_type(self):
        if self.situation_display_type_override:
            return self.situation_display_type_override
        return super().situation_display_type

    @classmethod
    def fake_perform_job(cls):
        pass

    @classmethod
    def get_possible_zone_ids_for_situation(cls, host_sim_info=None, guest_ids=None):
        possible_zones = []
        venue_manager = services.get_instance_manager(sims4.resources.Types.VENUE)
        venue_service = services.current_zone().venue_service
        for venue_tuning in cls.compatible_venues:
            if venue_tuning.is_residential:
                if host_sim_info is not None:
                    home_zone_id = host_sim_info.household.home_zone_id
                    home_venue_tuning = venue_manager.get(build_buy.get_current_venue(home_zone_id))
                    if home_venue_tuning.is_residential:
                        possible_zones.append(home_zone_id)
                if guest_ids is not None:
                    for guest_id in guest_ids:
                        guest_id = int(guest_id)
                        guest_info = services.sim_info_manager().get(guest_id)
                        if guest_info is not None:
                            guest_zone_id = guest_info.household.home_zone_id
                            if guest_zone_id is not None and guest_zone_id and guest_zone_id not in possible_zones:
                                guest_venue_tuning = venue_manager.get(build_buy.get_current_venue(guest_zone_id))
                                if guest_venue_tuning.is_residential:
                                    possible_zones.append(guest_zone_id)
                            travel_group = guest_info.travel_group
                            if travel_group is not None:
                                travel_group_zone_id = travel_group.zone_id
                                if travel_group_zone_id is not None and travel_group_zone_id and travel_group_zone_id not in possible_zones:
                                    travel_group_venue_tuning = venue_manager.get(build_buy.get_current_venue(travel_group_zone_id))
                                    if travel_group_venue_tuning.is_rental:
                                        possible_zones.append(travel_group_zone_id)
                    possible_zones.extend(venue_service.get_zones_for_venue_type_gen(venue_tuning))
            else:
                possible_zones.extend(venue_service.get_zones_for_venue_type_gen(venue_tuning))
        return possible_zones

    @classmethod
    def default_job(cls):
        return cls._default_job

    @classmethod
    def resident_job(cls):
        return cls._resident_job

    @classmethod
    def get_prepopulated_job_for_sims(cls, sim, target_sim_id=None):
        if target_sim_id and cls.targeted_situation is not None:
            sim_info = services.sim_info_manager().get(target_sim_id)
            if sim_info is None:
                return
            else:
                prepopulated = [(sim.id, cls.targeted_situation.actor_job.guid64), (target_sim_id, cls.targeted_situation.target_job.guid64)]
                return prepopulated

    def _display_role_objects_notification(self, sim, bullets):
        text = self.recommended_job_object_text(bullets)
        notification = self.recommended_job_object_notification(sim, text=lambda *_, **__: text)
        notification.show_dialog()

    @property
    def pie_menu_icon(self):
        return self._pie_menu_icon

    @classproperty
    def display_name(self):
        return self._display_name

    @property
    def description(self):
        return self.situation_description

    @classproperty
    def icon(self):
        return self._icon

    @property
    def start_audio_sting(self):
        return self.audio_sting_on_start

    @property
    def audio_background(self):
        return self.background_audio

    def get_target_object(self):
        pass

    def get_created_object(self):
        pass

    def get_situation_items(self):
        pass

    @property
    def situation_goal_type_ids(self):
        return self._seed.situation_goal_type_ids

    @property
    def end_audio_sting(self):
        current_level = self.get_level()
        level_data = self.get_level_data(current_level)
        if level_data is not None and level_data.audio_sting_on_end is not None:
            return level_data.audio_sting_on_end
        else:
            return

    @classproperty
    def relationship_between_job_members(cls):
        return cls._relationship_between_job_members

    @classproperty
    def implies_greeted_status(cls):
        return cls._implies_greeted_status

    @classmethod
    def cost(cls):
        return cls._cost

    @classproperty
    def survives_active_household_change(cls):
        return cls._survives_active_household_change

    @classproperty
    def maintain_sims_consistency(cls):
        return cls._maintain_sims_consistency

    @classproperty
    def is_unique_situation(cls):
        return cls._is_unique

    def _get_duration(self):
        if self._seed.duration_override is not None:
            return self._seed.duration_override
        return self.duration + random.randint(0, self.duration_randomizer)

    def get_remaining_time(self):
        if self._duration_alarm_handle is None:
            return
        return self._duration_alarm_handle.get_remaining_time()

    def _get_remaining_time_for_gsi(self):
        return self.get_remaining_time()

    def _get_remaining_time_in_minutes(self):
        time_span = self.get_remaining_time()
        if time_span is None:
            return 0
        return time_span.in_minutes()

    def _get_goal_tracker(self):
        return self._goal_tracker

    def _send_build_buy_lock(self):
        if self.build_buy_lock_reason is not None:
            op = BuildBuyLockUnlock(True, self.build_buy_lock_reason)
            distributor.system.Distributor.instance().add_op_with_no_owner(op)

    def _save_custom(self, seed):
        super()._save_custom(seed)
        if self._goal_tracker is not None:
            self._goal_tracker.save_to_seed(seed)

    def start_situation(self):
        super().start_situation()
        self._set_duration_alarm()
        self._send_build_buy_lock()
        if self._goal_tracker is None:
            if self._dynamic_goals is None:
                (_, self._goal_tracker) = self.goal_tracker_type(self)
            else:
                self._goal_tracker = situations.dynamic_situation_goal_tracker.DynamicSituationGoalTracker(self)

    def load_situation(self):
        result = super().load_situation()
        if result:
            self._send_build_buy_lock()
        return result

    def _load_situation_states_and_phases(self):
        super()._load_situation_states_and_phases()
        self._set_duration_alarm()
        if not self._seed.goal_tracker_seedling:
            return
        if self._seed.goal_tracker_seedling.goal_tracker_type == GoalTrackerType.STANDARD_GOAL_TRACKER:
            self._goal_tracker = situations.situation_goal_tracker.SituationGoalTracker(self)
        elif self._seed.goal_tracker_seedling.goal_tracker_type == GoalTrackerType.DYNAMIC_GOAL_TRACKER:
            self._goal_tracker = situations.dynamic_situation_goal_tracker.DynamicSituationGoalTracker(self)

    def change_duration(self, duration):
        if not self.is_running:
            logger.error("Trying to change the duration of a situation {} that's not running.", self)
        self._set_duration_alarm(duration_override=duration)
        if self.is_user_facing:
            self.add_situation_duration_change_op()

    def _set_duration_alarm(self, duration_override=None):
        if duration_override is not None:
            duration = duration_override
        else:
            duration = self._get_duration()
        self.set_end_time(duration)
        if duration > 0:
            if self._duration_alarm_handle is not None:
                alarms.cancel_alarm(self._duration_alarm_handle)
            self._duration_alarm_handle = alarms.add_alarm(self, clock.interval_in_sim_minutes(duration), self._situation_timed_out)

    def _cancel_duration_alarm(self):
        if self.is_user_facing:
            logger.error('Canceling duration alarm for a User-Facing Situation {}', self, owner='rmccord')
        if self._duration_alarm_handle is not None:
            alarms.cancel_alarm(self._duration_alarm_handle)

    def on_situation_goal_button_clicked(self):
        pass

    def pre_destroy(self):
        pass

    def _destroy(self):
        if self._duration_alarm_handle is not None:
            alarms.cancel_alarm(self._duration_alarm_handle)
        if self._goal_tracker is not None:
            self._goal_tracker.destroy()
            self._goal_tracker = None
        if self.run_carry_fixup_on_destroy:
            sims_to_run_carry = [sim.sim_info for sim in self.sims_in_situation()]
            carry.carry_elements.run_fixup_carryable_sims(sims_to_run_carry=sims_to_run_carry)
        super()._destroy()

    def on_remove(self):
        if self.build_buy_lock_reason is not None:
            op = BuildBuyLockUnlock(False)
            distributor.system.Distributor.instance().add_op_with_no_owner(op)
        super().on_remove()

    def _situation_timed_out(self, _):
        logger.debug('Situation time expired: {}', self)
        self._self_destruct()

    @classmethod
    def is_situation_available(cls, initiating_sim, target_sim_id=0):
        is_targeted = cls.targeted_situation is not None and cls.targeted_situation.target_job is not None
        if is_targeted and target_sim_id:
            if not cls.targeted_situation.target_job.can_sim_be_given_job(target_sim_id, initiating_sim.sim_info):
                return TestResult(False)
        elif target_sim_id == 0 != is_targeted == False:
            return TestResult(False)
        single_sim_resolver = event_testing.resolver.SingleSimResolver(initiating_sim.sim_info)
        return cls._initiating_sim_tests.run_tests(single_sim_resolver)

    @classmethod
    def get_predefined_guest_list(cls):
        pass

    @classmethod
    def is_venue_location_valid(cls, zone_id):
        compatible_region = services.current_region() if cls.venue_region_must_be_compatible else None
        return services.current_zone().venue_service.get_zone_venue_type_valid_for_venue_types(zone_id, cls.compatible_venues, compatible_region=compatible_region) is not None

    @classmethod
    def get_venue_location(cls):
        compatible_region = services.current_region() if cls.venue_region_must_be_compatible else None
        (zone_id, _) = services.current_zone().venue_service.get_zone_and_venue_type_for_venue_types(cls.compatible_venues, compatible_region=compatible_region)
        return zone_id

    @classmethod
    def has_venue_location(cls):
        compatible_region = services.current_region() if cls.venue_region_must_be_compatible else None
        return services.current_zone().venue_service.has_zone_for_venue_type(cls.compatible_venues, compatible_region=compatible_region)

    @classproperty
    def main_goal_visibility_test(cls):
        return cls._main_goal_visibility_test

    @classproperty
    def _ensemble_data(cls):
        return cls._ensemble

    @property
    def should_track_score(self):
        return self.scoring_enabled or self._hidden_scoring_override

    @property
    def should_give_rewards(self):
        return self.scoring_enabled or self._hidden_scoring_override

    def is_in_joinable_state(self):
        return True

    @property
    def custom_event_keys(self):
        return [type(self)] + list(self.tags)

    @classproperty
    def use_spawner_tags_on_travel(cls):
        return cls._use_spawner_tags_on_travel
