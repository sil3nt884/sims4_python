import _common_typesimport enum
class Pack(enum.Int):
    try:
        BASE_GAME = _common_types.BASE_GAME
        SP01 = _common_types.SP01
        GP01 = _common_types.GP01
        EP01 = _common_types.EP01
        FP01 = _common_types.FP01
        SP02 = _common_types.SP02
        GP02 = _common_types.GP02
        SP03 = _common_types.SP03
        SP04 = _common_types.SP04
        EP02 = _common_types.EP02
        GP03 = _common_types.GP03
        SP05 = _common_types.SP05
        SP06 = _common_types.SP06
        SP07 = _common_types.SP07
        SP08 = _common_types.SP08
        SP09 = _common_types.SP09
        SP10 = _common_types.SP10
        GP04 = _common_types.GP04
        GP05 = _common_types.GP05
        GP06 = _common_types.GP06
        GP07 = _common_types.GP07
        GP08 = _common_types.GP08
        GP09 = _common_types.GP09
        GP10 = _common_types.GP10
        EP03 = _common_types.EP03
        EP04 = _common_types.EP04
        EP05 = _common_types.EP05
        EP06 = _common_types.EP06
        EP07 = _common_types.EP07
        EP08 = _common_types.EP08
        EP09 = _common_types.EP09
        EP10 = _common_types.EP10
        SP11 = _common_types.SP11
        SP12 = _common_types.SP12
        SP13 = _common_types.SP13
        SP14 = _common_types.SP14
        SP15 = _common_types.SP15
        SP16 = _common_types.SP16
        SP17 = _common_types.SP17
        SP18 = _common_types.SP18
        SP19 = _common_types.SP19
        SP20 = _common_types.SP20
        SP21 = _common_types.SP21
        SP22 = _common_types.SP22
        SP23 = _common_types.SP23
        SP24 = _common_types.SP24
        SP25 = _common_types.SP25
        SP26 = _common_types.SP26
        SP27 = _common_types.SP27
        SP28 = _common_types.SP28
        SP29 = _common_types.SP29
        SP30 = _common_types.SP30
        EP11 = _common_types.EP11
        EP12 = _common_types.EP12
        EP13 = _common_types.EP13
        EP14 = _common_types.EP14
        EP15 = _common_types.EP15
        EP16 = _common_types.EP16
        EP17 = _common_types.EP17
        EP18 = _common_types.EP18
        EP19 = _common_types.EP19
        EP20 = _common_types.EP20
        GP11 = _common_types.GP11
        GP12 = _common_types.GP12
        GP13 = _common_types.GP13
        GP14 = _common_types.GP14
        GP15 = _common_types.GP15
        GP16 = _common_types.GP16
        GP17 = _common_types.GP17
        GP18 = _common_types.GP18
        GP19 = _common_types.GP19
        GP20 = _common_types.GP20
        SP31 = _common_types.SP31
        SP32 = _common_types.SP32
        SP33 = _common_types.SP33
        SP34 = _common_types.SP34
        SP35 = _common_types.SP35
        SP36 = _common_types.SP36
        SP37 = _common_types.SP37
        SP38 = _common_types.SP38
        SP39 = _common_types.SP39
        SP40 = _common_types.SP40
        SP41 = _common_types.SP41
        SP42 = _common_types.SP42
        SP43 = _common_types.SP43
        SP44 = _common_types.SP44
        SP45 = _common_types.SP45
        SP46 = _common_types.SP46
        SP47 = _common_types.SP47
        SP48 = _common_types.SP48
        SP49 = _common_types.SP49
        SP50 = _common_types.SP50
    except:
        pass
try:
    import _zone
except ImportError:
    available_packs = set(Pack)

    def is_available_pack(pack):
        return pack in available_packs
is_available_pack = _zone.is_available_packavailable_packs = {pack for pack in Pack if is_available_pack(pack)}
class UnavailablePackError(ValueError):
    pass

def get_available_packs():
    return tuple(pack for pack in Pack if is_available_pack(pack))

def are_packs_available(packs):
    if not isinstance(packs, tuple):
        packs = (packs,)
    return any(is_available_pack(p) for p in packs)

def get_pack_name(value) -> str:
    try:
        return str(Pack(value))
    except:
        return '<Unknown Pack>'

def get_pack_enum(folder_name) -> Pack:
    try:
        pack_enum_name = 'Pack.{}'.format(folder_name[2:]).lower()
        for pack in Pack:
            if str(pack).lower() == pack_enum_name:
                return pack
        return Pack.BASE_GAME
    except:
        return Pack.BASE_GAME
