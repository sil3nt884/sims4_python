from zone_director import ZoneDirectorBase
class SituationZoneDirectorMixin:
    INSTANCE_TUNABLES = {'_zone_director': ZoneDirectorBase.TunableReference(description='\n            This zone director will automatically be requested by the situation\n            during zone spin up.\n            ')}

    @classmethod
    def get_zone_director_request(cls, host_sim_info=None, zone_id=None):
        return (cls._zone_director(), cls._get_zone_director_request_type())

    @classmethod
    def _get_zone_director_request_type(cls):
        raise NotImplementedError
