"""Interlocking task config registration.

This module registers a template Gym environment id for an interlocking task. It is a
lightweight template so you can quickly replace the USD paths for your robot and blocks.

Replace the placeholders in `interlocking_env_cfg.py` with your own USD asset paths.
"""
from __future__ import annotations

import gym

from .interlocking_env_cfg import InterlockingEnvCfg


gym.register(
    id="Isaac-Interlocking-Task-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    kwargs={
        # Pass the env config class directly so IsaacLab can build the env.
        "env_cfg_entry_point": InterlockingEnvCfg,
    },
    disable_env_checker=True,
)
