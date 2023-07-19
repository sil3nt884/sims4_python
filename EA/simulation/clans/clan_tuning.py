import enum
class ClanValue(_ClanDisplayMixin, metaclass=HashedTunedInstanceMetaclass, manager=services.get_instance_manager(sims4.resources.Types.CLAN_VALUE)):
    INSTANCE_TUNABLES = {'discipline_ranked_stat': TunableReference(description='\n            The ranked statistic representing how well a Sim is following this clan value.\n            ', manager=services.get_instance_manager(sims4.resources.Types.STATISTIC), class_restrictions=('RankedStatistic',), export_modes=ExportModes.All)}

class Clan(_ClanDisplayMixin, metaclass=HashedTunedInstanceMetaclass, manager=services.get_instance_manager(sims4.resources.Types.CLAN)):
    INSTANCE_TUNABLES = {'clan_values': TunableList(description='\n            The list of values that members of this clan should follow.\n            ', tunable=TunableReference(manager=services.get_instance_manager(sims4.resources.Types.CLAN_VALUE)), export_modes=ExportModes.All), 'clan_hierarchy_ranked_stat': TunableReference(description='\n            The ranked statistic that is used to represent a Sims hierarchy within the clan.\n            ', manager=services.get_instance_manager(sims4.resources.Types.STATISTIC), class_restrictions=('RankedStatistic',), export_modes=ExportModes.All), 'clan_trait': TunableReference(description='\n            The trait that represents being a member of this clan.\n            ', manager=services.get_instance_manager(sims4.resources.Types.TRAIT))}

class ClanOpType(enum.Int):
    ADD_SIM_TO_CLAN = ...
    REMOVE_SIM_FROM_CLAN = ...
    MAKE_CLAN_LEADER = ...

class ClanLootOp(BaseLootOperation):
    FACTORY_TUNABLES = {'operation': TunableEnumEntry(description='\n            The operation to perform.\n            ', tunable_type=ClanOpType, default=ClanOpType.ADD_SIM_TO_CLAN), 'clan': TunablePackSafeReference(description='\n            A reference to the clan for which this operation is being applied.\n            ', manager=services.get_instance_manager(sims4.resources.Types.CLAN))}

    def __init__(self, *args, operation=None, clan=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._operation = operation
        self._clan = clan

    def _apply_to_subject_and_target(self, subject, target, resolver):
        clan_service = services.clan_service()
        if clan_service is None:
            return
        if self._operation == ClanOpType.ADD_SIM_TO_CLAN:
            clan_service.add_sim_to_clan(subject, self._clan)
        elif self._operation == ClanOpType.REMOVE_SIM_FROM_CLAN:
            clan_service.remove_sim_from_clan(subject, self._clan)
        elif self._operation == ClanOpType.MAKE_CLAN_LEADER:
            clan_service.reassign_clan_leader(subject, self._clan)
