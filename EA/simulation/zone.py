import collections
    gc_count_log = None
    perf_freeze_game_time_in_pause = False
def set_debug_lag(duration):
    pass

def freeze_game_time_in_pause(freeze):
    global perf_freeze_game_time_in_pause
    perf_freeze_game_time_in_pause = freeze
