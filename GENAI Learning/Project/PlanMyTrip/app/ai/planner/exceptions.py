class PlannerError(Exception):
    """Base planner exception."""


class PlannerGenerationError(PlannerError):
    """Raised when planner generation fails."""