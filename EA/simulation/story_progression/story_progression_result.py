import enum
class StoryProgressionResultType(enum.Int, export=False):
    SUCCESS = ...
    SUCCESS_MAKE_HISTORICAL = ...
    ERROR = ...
    FAILED_TESTS = ...
    FAILED_PRECONDITIONS = ...
    FAILED_NEXT_CHAPTER = ...
    FAILED_ACTION = ...
    FAILED_DEMOGRAPHICS = ...
    FAILED_NO_ARCS = ...
    FAILED_ROTATION = ...

class StoryProgressionResult:

    def __init__(self, result_type, *args):
        self._result_type = result_type
        if args:
            self._reason = args[0]
            self._format_args = args[1:]
        else:
            (self._reason, self._format_args) = (None, ())

    def __bool__(self):
        return self._result_type == StoryProgressionResultType.SUCCESS or self._result_type == StoryProgressionResultType.SUCCESS_MAKE_HISTORICAL

    @property
    def reason(self):
        if self._reason:
            self._reason = self._reason.format(*self._format_args)
            self._format_args = ()
        return self._reason

    def __str__(self):
        if self.reason:
            return self.reason
        return str(self._result_type)

    @property
    def result_type(self):
        return self._result_type

    @property
    def should_be_made_historical(self):
        return self._result_type == StoryProgressionResultType.SUCCESS_MAKE_HISTORICAL
