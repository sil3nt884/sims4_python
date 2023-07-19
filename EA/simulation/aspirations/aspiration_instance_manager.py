from aspirations.aspiration_types import AspriationType
class AspirationInstanceManager(InstanceManager):

    def all_whim_sets_gen(self):
        for aspiration in self.types.values():
            if aspiration.aspiration_type == AspriationType.WHIM_SET:
                yield aspiration
