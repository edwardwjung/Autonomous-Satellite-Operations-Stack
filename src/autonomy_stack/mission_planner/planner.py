from __future__ import annotations

from autonomy_stack.models import Action, PlannerOutput, SpacecraftState


class MissionPlanner:
    """Constraint-aware mission planner skeleton.

    Priority order in v1:
    1) downlink if storage is high
    2) image if battery is healthy
    3) keep attitude tracking
    """

    def plan(self, state: SpacecraftState) -> PlannerOutput:
        tasks = []
        if state.housekeeping.data_storage_used_mb > 900.0:
            tasks.append(Action("downlink_data", {"band": "x"}))
        elif state.housekeeping.battery_soc > 0.35:
            tasks.append(Action("take_image", {"target": "site_alpha"}))
        else:
            tasks.append(Action("slew_to_orientation", {"q": [1.0, 0.0, 0.0, 0.0]}))
        return PlannerOutput(tasks=tasks)
