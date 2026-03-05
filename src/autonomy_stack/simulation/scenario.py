from __future__ import annotations

from autonomy_stack.models import AttitudeState, Housekeeping, OrbitState, SpacecraftState


def default_initial_state() -> SpacecraftState:
    return SpacecraftState(
        orbit=OrbitState(
            t=0.0,
            position_km=[6878.0, 0.0, 0.0],
            velocity_km_s=[0.0, 7.5, 0.1],
        ),
        attitude=AttitudeState(
            quaternion=[1.0, 0.0, 0.0, 0.0],
            body_rate_deg_s=[0.0, 0.0, 0.0],
        ),
        housekeeping=Housekeeping(
            battery_soc=0.8,
            data_storage_used_mb=150.0,
            temperature_c=25.0,
        ),
    )
