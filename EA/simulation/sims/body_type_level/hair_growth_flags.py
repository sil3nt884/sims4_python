import enum
class HairGrowthFlags(enum.IntFlags, export=False):
    NONE = 0
    FACIAL_HAIR = 256
    ARM_HAIR = 512
    LEG_HAIR = 1024
    TORSOFRONT_HAIR = 2048
    TORSOBACK_HAIR = 4096
    ALL = FACIAL_HAIR | ARM_HAIR | LEG_HAIR | TORSOFRONT_HAIR | TORSOBACK_HAIR
