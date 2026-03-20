from launch import LaunchDescription
from launch_ros.actions import Node
from moveit_configs_utils import MoveItConfigsBuilder
import os
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():

    panda_dir = get_package_share_directory('moveit_resources_panda_moveit_config')
    llm_bridge_dir = get_package_share_directory('llm_robot_bridge')

    moveit_config = (
        MoveItConfigsBuilder('moveit_resources_panda')
        .robot_description(
            file_path=os.path.join(panda_dir, 'config', 'panda.urdf.xacro')
        )
        .robot_description_semantic(
            file_path=os.path.join(panda_dir, 'config', 'panda.srdf')
        )
        .robot_description_kinematics(
            file_path=os.path.join(panda_dir, 'config', 'kinematics.yaml')
        )
        .joint_limits(
            file_path=os.path.join(panda_dir, 'config', 'joint_limits.yaml')
        )
        .to_moveit_configs()
    )

    moveit_cpp_yaml = os.path.join(llm_bridge_dir, 'config', 'moveit_cpp.yaml')

    moveit_executor_node = Node(
        package='llm_robot_bridge',
        executable='moveit_executor_node',
        output='screen',
        parameters=[
            moveit_config.robot_description,
            moveit_config.robot_description_semantic,
            moveit_config.robot_description_kinematics,
            moveit_config.joint_limits,
            moveit_cpp_yaml,
            {'use_sim_time': True},
        ],
    )

    return LaunchDescription([moveit_executor_node])
