import services
class WeightedObjectives(TunableList):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, tunable=TunableTuple(description='\n                A set of tests that are run against the Sim. If the tests pass,\n                this objective and the weight are added to a list for randomization.\n                ', objective=TunableReference(description='\n                    The objective that will be provided if the tests pass.\n                    ', manager=services.get_instance_manager(Types.OBJECTIVE)), tests=TunableTestSet(description='\n                    The tests that must pass for this objective to be valid.\n                    '), weight=TunableRange(description='\n                    The weight of this objective against the other passing objectives.\n                    ', tunable_type=float, minimum=0, default=1)), **kwargs)
