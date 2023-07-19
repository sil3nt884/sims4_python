import enum
class StoryProgressionDomainType(enum.Int):
    MY_HOUSEHOLDS = 0
    OTHER_HOUSEHOLDS = 1

class StoryProgTunables:
    DOMAIN_ENABLEMENT_DEFAULTS = TunableMapping(description='\n        Default enablement states for all story progression domains that can be enabled/disabled.\n        ', key_type=TunableEnumEntry(tunable_type=StoryProgressionDomainType, default=StoryProgressionDomainType.MY_HOUSEHOLDS), value_type=Tunable(tunable_type=bool, default=True), tuple_name='CategoryEnablementDefaultTuple', export_modes=ExportModes.ClientBinary)
    HISTORY = TunableTuple(chapter_history_lifetime=TunableTimeSpan(description="\n            How long a chapter's history will be stored in persistence.\n            ", default_days=5), no_history_discovery_string=TunableLocalizedStringFactoryVariant(description='\n            String to display when there are no historical arcs to discover.\n            '), death_type_discovery_string_map=TunableMapping(description='\n            Mapping of death type to a discovery string. \n            ', key_type=TunableEnumEntry(tunable_type=DeathType, default=DeathType.NONE), value_type=TunableLocalizedStringFactoryVariant()))
