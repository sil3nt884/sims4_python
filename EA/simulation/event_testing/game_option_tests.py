import enumimport servicesfrom event_testing.results import TestResultfrom event_testing.test_base import BaseTestfrom event_testing.test_events import TestEventfrom sims4.collections import frozendictfrom sims4.common import Pack, is_available_packfrom sims4.tuning.tunable import TunableEnumEntry, HasTunableSingletonFactory, AutoFactoryInit, Tunable
class TestableGameOptions(enum.IntFlags):
    CIVIC_POLICY_NPC_VOTING_ENABLED = ...
    ECO_FOOTPRINT_GAMEPLAY = ...
    DUST_SYSTEM_ENABLED = ...
    RESTRICT_NPC_WEREWOLVES = ...
    DISABLE_LUNAR_EFFECTS = ...
    NPC_RELATIONSHIP_AUTONOMY_ENABLED = ...
    SELF_DISCOVERY_ENABLED = ...
    CAREER_LAY_OFF_ENABLED = ...
    REQUIRED_PACK_BY_OPTION = frozendict({CAREER_LAY_OFF_ENABLED: Pack.EP13, SELF_DISCOVERY_ENABLED: Pack.EP13, NPC_RELATIONSHIP_AUTONOMY_ENABLED: Pack.EP12, RESTRICT_NPC_WEREWOLVES: Pack.GP12, DUST_SYSTEM_ENABLED: Pack.SP22, ECO_FOOTPRINT_GAMEPLAY: Pack.EP09, CIVIC_POLICY_NPC_VOTING_ENABLED: Pack.EP09})

    @property
    def supporting_pack_installed(self):
        pack = TestableGameOptions.REQUIRED_PACK_BY_OPTION.get(self, None)
        return pack is None or is_available_pack(pack)

class SimInfoGameplayOptionsTest(HasTunableSingletonFactory, AutoFactoryInit, BaseTest):
    FACTORY_TUNABLES = {'gameplay_option': TunableEnumEntry(description='\n            The gameplay option to test. This test will pass if this option is\n            set.\n            ', tunable_type=TestableGameOptions, default=TestableGameOptions.CIVIC_POLICY_NPC_VOTING_ENABLED), 'invert': Tunable(description='\n            If enabled, requires the option to be unset for the test to pass.\n            ', tunable_type=bool, default=False)}

    def get_expected_args(self):
        return {}

    def get_test_events_to_register(self):
        return (TestEvent.TestedGameOptionChanged,)

    def get_custom_event_registration_keys(self):
        return ((TestEvent.TestedGameOptionChanged, self.gameplay_option),)

    def __call__(self, test_targets=None):
        if not self.gameplay_option.supporting_pack_installed:
            return TestResult(False, '{} option missing required pack', self.gameplay_option, self.tooltip)
        value = None
        if self.gameplay_option == TestableGameOptions.CIVIC_POLICY_NPC_VOTING_ENABLED or self.gameplay_option == TestableGameOptions.ECO_FOOTPRINT_GAMEPLAY:
            street_service = services.street_service()
            if street_service is not None:
                if self.gameplay_option == TestableGameOptions.CIVIC_POLICY_NPC_VOTING_ENABLED:
                    value = street_service.enable_automatic_voting
                else:
                    value = street_service.enable_eco_footprint
        elif self.gameplay_option == TestableGameOptions.DUST_SYSTEM_ENABLED:
            dust_service = services.dust_service()
            if dust_service is not None:
                value = dust_service.game_option_enabled
        elif self.gameplay_option == TestableGameOptions.RESTRICT_NPC_WEREWOLVES:
            misc_option_service = services.misc_options_service()
            if misc_option_service is not None:
                value = misc_option_service.restrict_npc_werewolves
        elif self.gameplay_option == TestableGameOptions.DISABLE_LUNAR_EFFECTS:
            lunar_cycle_service = services.lunar_cycle_service()
            value = lunar_cycle_service.lunar_effects_disabled
        elif self.gameplay_option == TestableGameOptions.NPC_RELATIONSHIP_AUTONOMY_ENABLED:
            misc_option_service = services.misc_options_service()
            if misc_option_service is not None:
                value = misc_option_service.npc_relationship_autonomy_enabled
        elif self.gameplay_option == TestableGameOptions.SELF_DISCOVERY_ENABLED:
            misc_option_service = services.misc_options_service()
            if misc_option_service is not None:
                value = misc_option_service.self_discovery_enabled
        elif self.gameplay_option == TestableGameOptions.CAREER_LAY_OFF_ENABLED:
            career_service = services.get_career_service()
            if career_service is not None:
                value = career_service.career_lay_off_enabled
        if value is None:
            return TestResult(False, 'game option {} is unknown in current pack', self.gameplay_option, tooltip=self.tooltip)
        if self.invert:
            if value:
                return TestResult(False, 'test negated, game option {} is set to {}', self.gameplay_option, value, tooltip=self.tooltip)
        elif not value:
            return TestResult(False, 'game option {} is set to {}', self.gameplay_option, value, tooltip=self.tooltip)
        return TestResult.TRUE
