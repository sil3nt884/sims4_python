from animation.posture_manifest import MATCH_ANY, MATCH_NONE, PostureManifestEntry, PostureManifest
    SIT_PICKUP_POSTURES = _SIT_FAMILY_PICKUP_POSTURES
else:
    SIT_PICKUP_POSTURES = _SIT_FAMILY_BG_PICKUP_POSTURES
class PostureConstants:
    SIT_POSTURE_TYPE = TunableReference(description='\n        A reference to the sit posture type.\n        ', manager=services.get_instance_manager(sims4.resources.Types.POSTURE))
