from __future__ import annotations

import argparse
import logging
from dataclasses import replace

from autonomy_stack.autonomy.agent import AutonomyAgent
from autonomy_stack.control.executor import CommandExecutor
from autonomy_stack.dynamics.propagator import DynamicsPropagator
from autonomy_stack.estimation.ekf import EKFEstimator
from autonomy_stack.fault_detection.detector import FaultDetector
from autonomy_stack.mission_planner.planner import MissionPlanner
from autonomy_stack.models import Action, Mode, StepOutput, TelemetryPacket
from autonomy_stack.simulation.scenario import default_initial_state
from autonomy_stack.telemetry.bus import TelemetryBus
from autonomy_stack.utils.logging import configure_logging

logger = logging.getLogger(__name__)


class AutonomyStack:
    def __init__(self) -> None:
        self.bus = TelemetryBus()
        self.dynamics = DynamicsPropagator()
        self.estimator = EKFEstimator()
        self.planner = MissionPlanner()
        self.agent = AutonomyAgent()
        self.executor = CommandExecutor()
        self.fault_detector = FaultDetector()

    def run(self, steps: int, dt_s: float) -> list[StepOutput]:
        state = default_initial_state()
        outputs: list[StepOutput] = []

        for i in range(steps):
            state = self.dynamics.step(state, dt_s=dt_s)

            telemetry = TelemetryPacket(
                t=state.orbit.t,
                state=state,
                sensors={"gyro_z": state.attitude.body_rate_deg_s[2]},
            )
            self.bus.publish("telemetry.raw", telemetry)

            estimated = self.estimator.update(telemetry)
            fault = self.fault_detector.detect(estimated)

            planner_output = self.planner.plan(estimated)
            action = self.agent.choose_action(estimated, planner_output)

            if fault is not None and fault.severity >= 3:
                action = Action("enter_safe_mode")

            state = self.executor.apply(estimated, action)

            if state.mode == Mode.SAFE:
                # Simple safe-mode power policy.
                hk = replace(
                    state.housekeeping,
                    battery_soc=min(1.0, state.housekeeping.battery_soc + 0.005),
                    data_storage_used_mb=max(0.0, state.housekeeping.data_storage_used_mb - 10.0),
                )
                state = replace(state, housekeeping=hk)

            result = StepOutput(
                t=telemetry.t,
                telemetry=telemetry,
                estimated_state=estimated,
                planner=planner_output,
                selected_action=action,
                fault=fault,
            )
            outputs.append(result)
            logger.info(
                "step=%d t=%.1f mode=%s action=%s battery=%.2f storage=%.1f fault=%s",
                i,
                telemetry.t,
                state.mode.value,
                action.name,
                state.housekeeping.battery_soc,
                state.housekeeping.data_storage_used_mb,
                fault.fault_id if fault else "none",
            )

        return outputs


def main() -> None:
    parser = argparse.ArgumentParser(description="Run autonomy stack simulation")
    parser.add_argument("--steps", type=int, default=20)
    parser.add_argument("--dt", type=float, default=1.0)
    args = parser.parse_args()

    configure_logging()
    stack = AutonomyStack()
    stack.run(steps=args.steps, dt_s=args.dt)


if __name__ == "__main__":
    main()
