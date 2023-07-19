import sims4.telemetry
class LiveEventTelemetry:

    @staticmethod
    def send_live_event_dialog_telemetry(test_name, sim_info, dialog_response):
        with telemetry_helper.begin_hook(ab_test_telemetry_writer, TELEMETRY_HOOK_AB_TEST_DIALOG, sim_info=sim_info) as hook:
            hook.write_string(TELEMETRY_FIELD_AB_TEST_NAME, test_name.name)
            hook.write_enum(TELEMETRY_FIELD_DIALOG_RESPONSE, dialog_response)
