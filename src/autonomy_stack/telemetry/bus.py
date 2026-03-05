from __future__ import annotations

from collections import defaultdict
from typing import Callable, DefaultDict, List

from autonomy_stack.models import TelemetryPacket


Subscriber = Callable[[TelemetryPacket], None]


class TelemetryBus:
    """Simple in-process pub/sub bus for telemetry and replay."""

    def __init__(self) -> None:
        self._subscribers: DefaultDict[str, List[Subscriber]] = defaultdict(list)
        self._history: List[TelemetryPacket] = []

    def subscribe(self, topic: str, subscriber: Subscriber) -> None:
        self._subscribers[topic].append(subscriber)

    def publish(self, topic: str, packet: TelemetryPacket) -> None:
        self._history.append(packet)
        for callback in self._subscribers[topic]:
            callback(packet)

    def history(self) -> List[TelemetryPacket]:
        return list(self._history)
