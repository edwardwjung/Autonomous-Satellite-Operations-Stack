from __future__ import annotations

from autonomy_stack.models import SpacecraftState, TelemetryPacket


class EKFEstimator:
    """EKF interface layer.

    This v1 implementation is a pass-through to establish module contracts.
    """

    def update(self, telemetry: TelemetryPacket) -> SpacecraftState:
        return telemetry.state
