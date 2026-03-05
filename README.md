# Satellite Autonomy Stack

This project models autonomous satellite operations with mission planning, state estimation, fault handling, and command execution in a single loop.

## Highlights
- Designed the closed-loop autonomy architecture across dynamics, estimation, planning, control, and telemetry.
- Added safety-oriented fault detection and safe-mode override flow.
- Organized interfaces to support extension from baseline simulation to deeper flight software behaviors.
- Closed-loop mission runtime with deterministic step-based execution.
- Safety-first flow: anomaly checks with explicit safe-mode path.
- Modular boundaries align with flight software subsystem design.
- Constraint-aware planning hooks for power/data/mission logic.
- Clear path to Monte Carlo validation and higher-fidelity dynamics.
