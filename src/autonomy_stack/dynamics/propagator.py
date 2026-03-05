from __future__ import annotations

from dataclasses import replace

from autonomy_stack.models import SpacecraftState


class DynamicsPropagator:
    """Placeholder orbit/attitude propagator.

    Designed to swap in SGP4 plus perturbations (J2/drag/SRP) later.
    """

    def step(self, state: SpacecraftState, dt_s: float) -> SpacecraftState:
        orbit = replace(
            state.orbit,
            t=state.orbit.t + dt_s,
            position_km=[state.orbit.position_km[0] + state.orbit.velocity_km_s[0] * dt_s,
                         state.orbit.position_km[1] + state.orbit.velocity_km_s[1] * dt_s,
                         state.orbit.position_km[2] + state.orbit.velocity_km_s[2] * dt_s],
        )
        return replace(state, orbit=orbit)
