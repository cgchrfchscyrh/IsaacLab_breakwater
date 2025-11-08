"""MDP helper functions for the interlocking task.

提供奖励、终止条件、事件等函数模板，供 `env_cfg.py` 引用。根据需求修改。
"""
from __future__ import annotations

from isaaclab.managers import SceneEntityCfg
from isaaclab.utils.math import geometry


def interlock_success(*, cube_a: SceneEntityCfg, cube_b: SceneEntityCfg, threshold: float = 0.02) -> bool:
    """示例终止条件：判断两块方块在 XY 平面上的距离是否小于阈值，代表互锁完成。

    Args:
        cube_a: 第一个方块的场景实体配置（由 DoneTerm 传入）。
        cube_b: 第二个方块的场景实体配置。
        threshold: 判断互锁的距离阈值（米）。

    Returns:
        True 表示任务完成，False 表示继续。
    """

    pos_a = cube_a.data.root_state_w[:, :3]
    pos_b = cube_b.data.root_state_w[:, :3]

    # 仅比较 XY 平面距离（可根据需求改为三维距离或加入姿态判定）
    dist = geometry.distance(pos_a[:, :2], pos_b[:, :2])
    return (dist < threshold).all()


def reward_interlock_stability(*, cube_a: SceneEntityCfg, cube_b: SceneEntityCfg, target_height: float = 0.05) -> float:
    """示例奖励：鼓励方块在互锁后保持期望高度。

    Args:
        cube_a: 第一个方块。
        cube_b: 第二个方块。
        target_height: 期望高度。

    Returns:
        正奖励表示更接近目标。
    """

    height_a = cube_a.data.root_state_w[:, 2]
    height_b = cube_b.data.root_state_w[:, 2]
    error = ((height_a - target_height) ** 2 + (height_b - target_height) ** 2).mean()
    return -error
