import services
class LunarEffectTracker(SimInfoTracker):

    def __init__(self, sim_info):
        self._sim_info = sim_info
        self._active_effects = None

    def on_lod_update(self, old_lod, new_lod):
        if not self.is_valid_for_lod(new_lod):
            self._clean_up()

    @property
    def sim_info(self):
        return self._sim_info

    @property
    def has_data_to_save(self):
        return bool(self._active_effects)

    def should_apply_lunar_effect(self, lunar_effect, start_time):
        if not self._active_effects:
            return True
        return (lunar_effect.guid64, start_time) not in self._active_effects

    def track_lunar_effect_applied(self, lunar_effect, start_time):
        if self._active_effects is None:
            self._active_effects = {}
        effect_key = (lunar_effect.guid64, start_time)
        self._active_effects[effect_key] = start_time + create_time_span(minutes=lunar_effect.effect_duration)

    def find_active_effect_tooltip(self):
        if not self._active_effects:
            return
        lunar_cycle_instances = services.get_instance_manager(Types.LUNAR_CYCLE)
        for effect_key in self._active_effects:
            (lunar_effect_guid, _start_time) = effect_key
            lunar_effect = lunar_cycle_instances.get(lunar_effect_guid)
            if not lunar_effect.is_tracked_effect:
                pass
            else:
                prospective_tooltip = lunar_effect.get_lunar_effect_tooltip(self._sim_info)
                if prospective_tooltip is not None:
                    return prospective_tooltip

    def prune_stale_effects(self, time_now):
        if not self._active_effects:
            return
        lunar_cycle_instances = services.get_instance_manager(Types.LUNAR_CYCLE)
        for (effect_key, end_time) in tuple(self._active_effects.items()):
            if end_time is UNSET:
                (lunar_effect_guid, start_time) = effect_key
                lunar_effect = lunar_cycle_instances.get(lunar_effect_guid)
                if lunar_effect is None or not lunar_effect.is_tracked_effect:
                    del self._active_effects[effect_key]
                else:
                    end_time = start_time + create_time_span(minutes=lunar_effect.effect_duration)
                    self._active_effects[effect_key] = end_time
                    if time_now < end_time:
                        pass
                    else:
                        del self._active_effects[effect_key]
            if time_now < end_time:
                pass
            else:
                del self._active_effects[effect_key]

    def _clean_up(self):
        self._sim_info = None
        self._active_effects = None

    def save_lunar_effects(self, lunar_effects_data):
        if not self._active_effects:
            return
        for (lunar_effect_tuning_id, start_time) in self._active_effects:
            with ProtocolBufferRollback(lunar_effects_data.applied_effects) as applied_lunar_effect_proto:
                applied_lunar_effect_proto.lunar_effect_id = lunar_effect_tuning_id
                applied_lunar_effect_proto.effect_start_time = start_time

    def load_lunar_effects(self, lunar_effects_data):
        for applied_lunar_effect_proto in lunar_effects_data.applied_effects:
            if self._active_effects is None:
                self._active_effects = {}
            lunar_effect_guid = applied_lunar_effect_proto.lunar_effect_id
            effect_start_time = DateAndTime(applied_lunar_effect_proto.effect_start_time)
            effect_key = (lunar_effect_guid, effect_start_time)
            self._active_effects[effect_key] = UNSET
