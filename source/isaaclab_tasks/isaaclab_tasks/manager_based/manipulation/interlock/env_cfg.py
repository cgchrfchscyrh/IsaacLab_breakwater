"""Interlocking environment config (template), relocated under interlock package.

Update USD paths/prims to match your robot and blocks.
"""
from isaaclab.assets import ArticulationCfg, RigidObjectCfg
from isaaclab.sensors import FrameTransformerCfg
from isaaclab.sensors.frame_transformer.frame_transformer_cfg import OffsetCfg
from isaaclab.sim.spawners.from_files.from_files_cfg import UsdFileCfg
from isaaclab.utils import configclass
from isaaclab.utils.assets import ISAAC_NUCLEUS_DIR

from isaaclab_tasks.manager_based.manipulation.stack.stack_env_cfg import StackEnvCfg


@configclass
class InterlockingEnvCfg(StackEnvCfg):
    def __post_init__(self):
        super().__post_init__()

        # Robot USD (already set to your provided absolute path)
        self.scene.robot = ArticulationCfg(
            prim_path="{ENV_REGEX_NS}/Robot",
            spawn=UsdFileCfg(
                usd_path="/home/liusongyang/Desktop/breakwater/teleop_2.usd",
                scale=(1.0, 1.0, 1.0),
            ),
        )

        # EE frame (adjust prims to match your robot)
        self.scene.ee_frame = FrameTransformerCfg(
            prim_path="{ENV_REGEX_NS}/Robot/root",
            debug_vis=False,
            visualizer_cfg=None,
            target_frames=[
                FrameTransformerCfg.FrameCfg(
                    prim_path="{ENV_REGEX_NS}/Robot/ee_link",
                    name="end_effector",
                    offset=OffsetCfg(pos=[0.0, 0.0, 0.0]),
                )
            ],
        )

        # Blocks (replace with your block USDs)
        cube_properties = RigidObjectCfg(
            prim_path="{ENV_REGEX_NS}/_tmp",
            init_state=RigidObjectCfg.InitialStateCfg(pos=[0.0, 0.0, 0.0]),
        )

        self.scene.cube_1 = RigidObjectCfg(
            prim_path="{ENV_REGEX_NS}/Cube_1",
            init_state=RigidObjectCfg.InitialStateCfg(pos=[0.4, 0.0, 0.0203]),
            spawn=UsdFileCfg(
                usd_path=f"{ISAAC_NUCLEUS_DIR}/Props/Blocks/your_block_1.usd",
                scale=(1.0, 1.0, 1.0),
                rigid_props=cube_properties,
            ),
        )
        self.scene.cube_2 = RigidObjectCfg(
            prim_path="{ENV_REGEX_NS}/Cube_2",
            init_state=RigidObjectCfg.InitialStateCfg(pos=[0.55, 0.05, 0.0203]),
            spawn=UsdFileCfg(
                usd_path=f"{ISAAC_NUCLEUS_DIR}/Props/Blocks/your_block_2.usd",
                scale=(1.0, 1.0, 1.0),
                rigid_props=cube_properties,
            ),
        )
        self.scene.cube_3 = RigidObjectCfg(
            prim_path="{ENV_REGEX_NS}/Cube_3",
            init_state=RigidObjectCfg.InitialStateCfg(pos=[0.60, -0.1, 0.0203]),
            spawn=UsdFileCfg(
                usd_path=f"{ISAAC_NUCLEUS_DIR}/Props/Blocks/your_block_3.usd",
                scale=(1.0, 1.0, 1.0),
                rigid_props=cube_properties,
            ),
        )
