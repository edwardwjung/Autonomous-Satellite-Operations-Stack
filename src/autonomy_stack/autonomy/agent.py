from __future__ import annotations

from autonomy_stack.models import Action, PlannerOutput, SpacecraftState


class AutonomyAgent:
    """Action selector with safety guardrails hook.

    In v1, this uses planner priority directly.
    """

    def choose_action(self, _state: SpacecraftState, planner_output: PlannerOutput) -> Action:
        if planner_output.tasks:
            return planner_output.tasks[0]
        return Action("idle")
