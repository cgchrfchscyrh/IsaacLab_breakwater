# Template env config for an interlocking task.
#
# 说明：这是一个最小模板，用于快速将你的自定义 robot.usd 和 block.usd 集成到一个 stack-like 环境中。
# 请按注释替换 USD 路径与关节/末端执行器名称以配合你的机器人。

from isaaclab.assets import ArticulationCfg, RigidObjectCfg
from isaaclab.sensors import FrameTransformerCfg
from isaaclab.sensors.frame_transformer.frame_transformer_cfg import OffsetCfg
from isaaclab.sim.spawners.from_files.from_files_cfg import UsdFileCfg
from isaaclab.utils import configclass
from isaaclab.utils.assets import ISAAC_NUCLEUS_DIR

# 基类 StackEnvCfg 提供了大部分 MDP / 观测 / 终止条件等逻辑
from isaaclab_tasks.manager_based.manipulation.stack.stack_env_cfg import StackEnvCfg


@configclass
class InterlockingEnvCfg(StackEnvCfg):
    """简单的交错/嵌套（interlocking）任务配置模板。

    默认的 USD 路径使用占位符（ISAAC_NUCLEUS_DIR 下的路径），请用你本地的 `robot.usd` 和 `block.usd` 覆盖。
    如果你的机器人是可关节控制的（Articulation），请在 `spawn` 中指向包含关节的 USD 文件。
    """

    def __post_init__(self):
        # 调用父类的后初始化，设置默认参数
        super().__post_init__()

        # ---------- 机器人（示例） ----------
        # 默认使用一个位于 ISAAC_NUCLEUS_DIR 的占位 robot USD（请替换为你的 robot.usd 路径）。
        # 你也可以替换为 isaaclab_assets 里已有的 ArticulationCfg（如 FRANKA_PANDA_CFG）
        self.scene.robot = ArticulationCfg(
            prim_path="{ENV_REGEX_NS}/Robot",
            spawn=UsdFileCfg(
                # 已替换为用户提供的 robot.usd 绝对路径
                usd_path="/home/liusongyang/Desktop/breakwater/teleop_2.usd",
                scale=(1.0, 1.0, 1.0),
            ),
        )

        # ---------- 末端执行器/帧（示例） ----------
        # 请根据你的机器人修改 prim_path 与偏移量（offset）
        self.scene.ee_frame = FrameTransformerCfg(
            prim_path="{ENV_REGEX_NS}/Robot/root",  # TODO: 替为你机器人中合适的根/基座 prim
            debug_vis=False,
            visualizer_cfg=None,
            target_frames=[
                FrameTransformerCfg.FrameCfg(
                    prim_path="{ENV_REGEX_NS}/Robot/ee_link",  # TODO: 替为你末端执行器 prim
                    name="end_effector",
                    offset=OffsetCfg(pos=[0.0, 0.0, 0.0]),
                )
            ],
        )

        # ---------- 方块（示例三块） ----------
        # cube_properties 使用默认刚体属性，可按需调整
        cube_properties = RigidObjectCfg(
            prim_path="{ENV_REGEX_NS}/_tmp",
            init_state=RigidObjectCfg.InitialStateCfg(pos=[0.0, 0.0, 0.0]),
        )

        self.scene.cube_1 = RigidObjectCfg(
            prim_path="{ENV_REGEX_NS}/Cube_1",
            init_state=RigidObjectCfg.InitialStateCfg(pos=[0.4, 0.0, 0.0203]),
            spawn=UsdFileCfg(
                # TODO: 替换为你的 block.usd 路径
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

        # ---------- 动作/控制/夹爪设置（占位） ----------
        # 这里我们保留父类默认动作配置。若你的机器人关节命名与父类不同，请在此处替换
        # 例如： self.actions.arm_action = mdp.JointPositionActionCfg(asset_name="robot", joint_names=["your_joint.*"], ...)

        # ---------- 说明 ----------
        # 1) 替换上面所有 TODO 注释中的路径/prim 名称为你实际的 USD 文件与 prim。
        # 2) 如果使用非 ISAAC_NUCLEUS 的本地 USD，可以直接使用绝对路径，例如 
        #    usd_path="/home/you/assets/robot.usd"
        # 3) 若需要自定义奖励/终止/事件逻辑，请在 `isaaclab_tasks/manager_based/manipulation/stack/mdp.py` 中
        #    添加或覆盖相应函数，或基于该文件编写你自己的 mdp 模块并在此处进行引用。
