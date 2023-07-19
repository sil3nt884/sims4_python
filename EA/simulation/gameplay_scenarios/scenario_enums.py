import enum
class ScenarioEntryMethod(enum.IntFlags):
    NEW_HOUSEHOLD = 1
    EXISTING_HOUSEHOLD = 2

class ScenarioProperties(enum.IntFlags):
    ONBOARDING = 1

class ScenarioCategory(DynamicEnum):
    INVALID = 0

class ScenarioDifficultyCategory(DynamicEnum):
    INVALID = 0

class ScenarioTheme(DynamicEnum):
    INVALID = 0
