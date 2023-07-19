import services
def write_buff_telemetry(hook_tag, buff, sim):
    if not sim.is_simulating:
        return
    current_zone = services.current_zone()
    if current_zone is None or not current_zone.is_zone_running:
        return
    logger.debug('{}: buff:{}', hook_tag, buff.buff_type)
    with telemetry_helper.begin_hook(buff_telemetry_writer, hook_tag, sim=sim) as hook:
        hook.write_int(TELEMETRY_FIELD_BUFF_ID, buff.buff_type.guid64)
