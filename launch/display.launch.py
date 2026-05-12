from launch import LaunchDescription
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch.substitutions import Command
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    # --- 1. FILE PATH SETUP ---
    # This finds the actual folder where your package is installed on the system.
    package_dir = get_package_share_directory('prosthetic_leg')

    # This creates the full path to your leg.urdf file
    urdf_file = os.path.join(package_dir, 'urdf', 'leg.urdf')

    # --- 2. ROBOT STATE PUBLISHER ---
    # This node is the "Heart" of the system.
    # It reads the URDF file and calculates the 3D position of every link.
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{
            'robot_description': ParameterValue(
                Command(['cat ', urdf_file]),
                value_type=str
            )
        }]
    )

    # --- 3. JOINT STATE PUBLISHER GUI ---
    # This is the "Remote Control."
    # It pops up the window with sliders for the Hip, Knee, and Ankle.
    joint_state_gui_node = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui'
    )

    # --- 4. RVIZ2 ---
    # This is the "Eyes" (The 3D Viewer).
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        # Adding back the argument to load a default URDF config
        # This prevents you from having to manually add the 'RobotModel' in RViz every time.
        arguments=['-d', os.path.join(
            get_package_share_directory('urdf_tutorial'),
            'rviz',
            'urdf.rviz'
        )]
    )

    # --- 5. THE RETURN (The missing piece!) ---
    # This list tells ROS 2 exactly which nodes to start up.
    return LaunchDescription([
        robot_state_publisher_node,
        joint_state_gui_node,
        rviz_node
    ])