import services
class SectionalSofaTuning:
    SECTIONAL_SOFA_OBJECT_DEF = TunableReference(description='\n        Catalog definition for the sectional sofa object.\n        ', manager=services.get_instance_manager(Types.OBJECT))
