from sims.household_enums import HouseholdChangeOrigin
class HouseholdRegionTelemetryData:

    def __init__(self, region_description_id=None):
        self.region_description_id = region_description_id
        self.played_household_count = 0
        self.played_sim_info_count = 0
        self.region_occupied_lot_count = 0
        self.region_total_lot_count = None
        self.townie_household_count = 0
        self.townie_sim_info_count = 0

    @property
    def is_townie_data(self):
        return self.region_description_id == 0

    def _send_telemetry(self):
        telemetry_hook = TELEMETRY_HOOK_TOWNIE_SIM_INFO_WORLD if self.is_townie_data else TELEMETRY_HOOK_PLAYED_SIM_INFO_WORLD
        with telemetry_helper.begin_hook(story_writer, telemetry_hook) as hook:
            hook.write_int(TELEMETRY_HOOK_REGION_ID, self.region_description_id)
            hook.write_int(TELEMETRY_HOOK_PLAYED_HOUSEHOLD_COUNT, self.played_household_count)
            hook.write_int(TELEMETRY_HOOK_PLAYED_SIM_INFO_COUNT, self.played_sim_info_count)
            if self.is_townie_data:
                hook.write_int(TELEMETRY_HOOK_TOWNIE_HOUSEHOLD_COUNT, self.townie_household_count)
                hook.write_int(TELEMETRY_HOOK_TOWNIE_SIM_INFOS_COUNT, self.townie_sim_info_count)
            else:
                hook.write_int(TELEMETRY_HOOK_OCCUPIED_LOT_COUNT, self.region_occupied_lot_count)
                hook.write_int(TELEMETRY_HOOK_TOTAL_LOT_COUNT, self.region_total_lot_count)

    @classmethod
    def send_household_region_telemetry(cls):
        household_manager = services.household_manager()
        if household_manager is None:
            return
        persistence_service = services.get_persistence_service()
        per_region_data = dict()
        for household in household_manager.values():
            is_townie_household = household.home_zone_id == 0
            region_description_id = 0 if is_townie_household else get_region_description_id_from_zone_id(household.home_zone_id)
            region_data = per_region_data.get(region_description_id, None)
            if region_data is None:
                region_data = HouseholdRegionTelemetryData(region_description_id=region_description_id)
                per_region_data[region_description_id] = region_data
            if household.is_played_household:
                region_data.played_household_count += 1
                region_data.played_sim_info_count += len(household)
            if is_townie_household:
                region_data.townie_household_count += 1
                region_data.townie_sim_info_count += len(household)
            else:
                region_data.region_occupied_lot_count += 1
                if region_data.region_total_lot_count is None:
                    neighborhood_proto = persistence_service.get_neighborhood_proto_buf_from_zone_id(household.home_zone_id)
                    region_data.region_total_lot_count = len(neighborhood_proto.lots)
        for region_data in per_region_data.values():
            region_data._send_telemetry()

def send_sim_added_telemetry(sim_info, reason=HouseholdChangeOrigin.UNKNOWN):
    with telemetry_helper.begin_hook(household_writer, TELEMETRY_HOOK_HOUSEHOLD_SIM_ADDED, sim_info=sim_info) as hook:
        hook.write_int(TELEMETRY_HOOK_SIM_AGE, sim_info.age)
        hook.write_int(TELEMETRY_HOOK_REASON, reason)
