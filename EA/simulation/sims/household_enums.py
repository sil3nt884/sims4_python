import enum
class HouseholdChangeOrigin(enum.Int, export=False):
    UNKNOWN = 0
    LOAD = 1
    REFRESH = 2
    GALLERY = 3
    MY_SAVES = 4
    CLONING = 5
    CREATION_BASIC_EXTRA = 6
    ADD_BASIC_EXTRA = 7
    NPC_GRADUATION = 8
    CHEAT = 9
    BIRTH = 10
    TUTORIAL = 11
    HIDING = 12
    LIVE_TRANSFER_DIALOG = 13
    ADOPTION = 14
    TEMPLATE = 15
    STAYOVER_RELATIVE = 16
    CHEAT_BREED_PICK_INTER = 17
    CHEAT_LOD_SIM_INFO = 18
    CHEAT_FILTER_TEST_SIM_TEMP_GEN = 19
    CHEAT_FILTER_CREATE_FROM_SIM_TEMP = 20
    CHEAT_GENEALOGY_GEN_DYNASTY = 21
    CHEAT_DEBUG_CREATE_SIM_INTER = 22
    CHEAT_PETS_CREATE_PET_BREED = 23
    CHEAT_SIMS_SPAWN_SIMPLE = 24
    CHEAT_SIMS_SPAWN = 25
    CHEAT_FILTER_CREATE_HOUSEHOLD_FROM_TEMP = 26
    NEIGH_POP_SERVICE_UNKNOWN = 27
    NEIGH_POP_SERVICE_HOMELESS = 28
    NEIGH_POP_SERVICE_RENT = 29
