import cython
    cython_log.always('CYTHON cython_utils is imported!', color=sims4.log.LEVEL_WARN)
else:
    cython_log.always('Pure Python cython_utils is imported!', color=sims4.log.LEVEL_WARN)
    from cython_utils_ph import *