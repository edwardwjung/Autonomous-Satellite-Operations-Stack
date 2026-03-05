from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class Mode(str, Enum):
    NOMINAL = "nominal"
    DEGRADED = "degraded"
    SAFE = "safe"


@dataclass
class OrbitState:
    t: float
    position_km: List[float]
    velocity_km_s: List[float]


@dataclass
class AttitudeState:
    quaternion: List[float]
    body_rate_deg_s: List[float]


@dataclass
class Housekeeping:
    battery_soc: float
    data_storage_used_mb: float
    temperature_c: float


@dataclass
class SpacecraftState:
    orbit: OrbitState
    attitude: AttitudeState
    housekeeping: Housekeeping
    mode: Mode = Mode.NOMINAL


@dataclass
class TelemetryPacket:
    t: float
    state: SpacecraftState
    sensors: Dict[str, float] = field(default_factory=dict)


@dataclass
class FaultReport:
    fault_id: str
    severity: int
    description: str


@dataclass
class Action:
    name: str
    args: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PlannerOutput:
    tasks: List[Action]
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class StepOutput:
    t: float
    telemetry: TelemetryPacket
    estimated_state: SpacecraftState
    planner: PlannerOutput
    selected_action: Action
    fault: Optional[FaultReport]
