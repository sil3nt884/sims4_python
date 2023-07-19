import enum
class OutfitOverrideOptionFlags(enum.IntFlags):
    DEFAULT = 0
    OVERRIDE_ALL_OUTFITS = 1
    IGNORE_BATHING = 2
    MANNEQUIN_MODE = 4
    APPLY_MODIFIER_VARIATION = 8
    FROM_SCRATCH = 16
    APPLY_GENETICS_FROM_OVERRIDE = 32
    OVERRIDE_CUSTOM_TEXTURES = 64
    OVERRIDE_HAIR_MATCH_FLAGS = 128

    import _cas
except:

    class _cas:
        SimInfo = None
        OutfitData = None

        @staticmethod
        def age_up_sim(*_, **__):
            pass

        @staticmethod
        def get_buffs_from_part_ids(*_, **__):
            return []

        @staticmethod
        def get_tags_from_outfit(*_, **__):
            return set()

        @staticmethod
        def generate_offspring(*_, **__):
            pass

        @staticmethod
        def generate_household(*_, **__):
            pass

        @staticmethod
        def generate_merged_outfit(*_, **__):
            pass

        @staticmethod
        def generate_random_siminfo(*_, **__):
            pass

        @staticmethod
        def generate_occult_siminfo(*_, **__):
            pass

        @staticmethod
        def is_duplicate_merged_outfit(*_, **__):
            pass

        @staticmethod
        def is_online_entitled(*_, **__):
            pass

        @staticmethod
        def apply_siminfo_override(*_, **__):
            pass

        @staticmethod
        def randomize_part_color(*_, **__):
            pass

        @staticmethod
        def randomize_skintone_from_tags(*_, **__):
            pass

        @staticmethod
        def set_caspart(*_, **__):
            pass

        @staticmethod
        def randomize_caspart(*_, **__):
            pass

        @staticmethod
        def randomize_caspart_list(*_, **__):
            pass

        @staticmethod
        def get_caspart_bodytype(*_, **__):
            pass

        @staticmethod
        def relgraph_set_edge(*_, **__):
            pass

        @staticmethod
        def relgraph_get_genealogy(*_, **__):
            pass

        @staticmethod
        def relgraph_set_marriage(*_, **__):
            pass

        @staticmethod
        def relgraph_set_engagement(*_, **__):
            pass

        @staticmethod
        def relgraph_add_child(*_, **__):
            pass

        @staticmethod
        def relgraph_get(*_, **__):
            pass

        @staticmethod
        def relgraph_set(*_, **__):
            pass

        @staticmethod
        def relgraph_cull(*_, **__):
            pass

        @staticmethod
        def change_bodytype_level(*_, **__):
            pass
