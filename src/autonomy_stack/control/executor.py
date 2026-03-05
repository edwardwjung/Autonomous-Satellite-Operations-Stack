from __future__ import annotations

import logging
from dataclasses import replace

from autonomy_stack.models import Action, Mode, SpacecraftState

logger = logging.getLogger(__name__)


class CommandExecutor:
    """Applies high-level actions to spacecraft state."""

    def apply(self, state: SpacecraftState, action: Action) -> SpacecraftState:
        logger.info("execute action=%s args=%s", action.name, action.args)

        if action.name == "take_image":
            hk = replace(
                state.housekeeping,
                data_storage_used_mb=min(1024.0, state.housekeeping.data_storage_used_mb + 50.0),
                battery_soc=max(0.0, state.housekeeping.battery_soc - 0.02),
            )
            return replace(state, housekeeping=hk)

        if action.name == "downlink_data":
            hk = replace(
                state.housekeeping,
                data_storage_used_mb=max(0.0, state.housekeeping.data_storage_used_mb - 120.0),
                battery_soc=max(0.0, state.housekeeping.battery_soc - 0.01),
            )
            return replace(state, housekeeping=hk)

        if action.name == "enter_safe_mode":
            return replace(state, mode=Mode.SAFE)

        return state
