from sims4.service_manager import Service
class MiscOptionsService(Service):

    def __init__(self):
        self._restrict_npc_werewolves = False
        self._npc_relationship_autonomy_enabled = True
        self._self_discovery_enabled = True

    def save_options(self, options_proto):
        options_proto.restrict_npc_werewolves = self._restrict_npc_werewolves
        options_proto.npc_relationship_autonomy_enabled = self._npc_relationship_autonomy_enabled
        options_proto.self_discovery_enabled = self._self_discovery_enabled

    def load_options(self, options_proto):
        self._restrict_npc_werewolves = options_proto.restrict_npc_werewolves
        self._npc_relationship_autonomy_enabled = options_proto.npc_relationship_autonomy_enabled
        self._self_discovery_enabled = options_proto.self_discovery_enabled

    @property
    def restrict_npc_werewolves(self):
        return self._restrict_npc_werewolves

    def set_restrict_npc_werewolves(self, enabled:bool):
        self._restrict_npc_werewolves = enabled

    @property
    def npc_relationship_autonomy_enabled(self):
        return self._npc_relationship_autonomy_enabled

    def set_npc_relationship_autonomy_enabled(self, enabled:bool):
        self._npc_relationship_autonomy_enabled = enabled

    @property
    def self_discovery_enabled(self):
        return self._self_discovery_enabled

    def set_self_discovery_enabled(self, enabled:bool):
        self._self_discovery_enabled = enabled
