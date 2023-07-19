import enum
    _log_arb_contents = False
class ActorType(enum.Int, export=False):
    Sim = int(149264255)
    Object = int(200706046)
    Door = int(2935391323)
    ProceduralObject = int(1054400919)
    Creature = int(2661483290)

class CreatureType(enum.Int):
    Invalid = 0
    Rabbit = int(2689485353)
    Hen = int(915067390)
    Chick = int(4176957319)
    Rooster = int(3987889111)
    Cow = int(1083682102)
    Llama = int(2978855956)

class InteractionAsmType(enum.IntFlags, export=False):
    Unknown = 0
    Interaction = 1
    Outcome = 2
    Response = 4
    Reactionlet = 8
    Canonical = 16

class ProceduralControlType(enum.Int, export=False):
    UNKNOWN = 0
    WHEEL = 1
    SPHERE_WHEEL = 2
    SKATE = 3
    LIP_SYNC = 4
