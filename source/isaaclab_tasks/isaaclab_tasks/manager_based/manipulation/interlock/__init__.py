"""Register the Interlocking task as a Gym environment.

This package hosts your custom interlocking task implementation with a clean, reusable
layout: env_cfg.py for configuration, optional mdp.py for task logic.
"""
from __future__ import annotations

import gym

from .env_cfg import InterlockingEnvCfg


gym.register(
    id="Isaac-Interlocking-Task-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    kwargs={
        "env_cfg_entry_point": InterlockingEnvCfg,
    },
    disable_env_checker=True,
)
