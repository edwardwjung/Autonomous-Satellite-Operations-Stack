from __future__ import annotations

from autonomy_stack.models import FaultReport, Mode, SpacecraftState


class FaultDetector:
    """Simple residual/threshold fault checks for v1."""

    def detect(self, state: SpacecraftState) -> FaultReport | None:
        if state.housekeeping.battery_soc < 0.12:
            return FaultReport(
                fault_id="low_power",
                severity=3,
                description="Battery state of charge below 12%",
            )
        if state.housekeeping.temperature_c > 75.0:
            return FaultReport(
                fault_id="thermal_high",
                severity=2,
                description="Thermal limit exceeded",
            )
        if state.mode == Mode.SAFE:
            return FaultReport(
                fault_id="safe_mode",
                severity=1,
                description="Vehicle is in safe mode",
            )
        return None
