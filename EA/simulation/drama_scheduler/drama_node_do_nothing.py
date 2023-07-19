from drama_scheduler.drama_node import BaseDramaNode, DramaNodeRunOutcome
class DoNothingDramaNode(BaseDramaNode):

    @classproperty
    def simless(cls):
        return True

    def _run(self):
        return DramaNodeRunOutcome.SUCCESS_NODE_COMPLETE
