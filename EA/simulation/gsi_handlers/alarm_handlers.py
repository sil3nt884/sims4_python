from sims4.gsi.dispatcher import GsiHandler
@GsiHandler('alarms', alarm_schema)
def generate_alarm_data(*args, zone_id:int=None, **kwargs):
    return alarms.get_alarm_data_for_gsi()
