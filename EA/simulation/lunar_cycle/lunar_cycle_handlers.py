import services
    set_phase_command.add_token_param('phase')
@GsiHandler('phases_view', lunar_phase_schema)
def generate_phases_view():
    phases = []
    lunar_cycle_service = services.lunar_cycle_service()
    for phase_type in LunarPhaseType:
        active_phase = lunar_cycle_service.current_phase == phase_type
        start_time = 'N/A'
        end_time = 'N/A'
        phase_length = lunar_cycle_service.get_phase_length(phase_type)
        if active_phase:
            start_time = lunar_cycle_service.current_phase_start
            end_time = start_time + phase_length
        phase_data = {'index': phase_type.value, 'phase': str(phase_type.name), 'start_time': str(start_time), 'end_time': str(end_time), 'expected_length': str(phase_length) if phase_length > TimeSpan.ZERO else '', 'active': str(active_phase)}
        phases.append(phase_data)
    return phases
