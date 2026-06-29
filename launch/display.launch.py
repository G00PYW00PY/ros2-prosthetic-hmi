from launch import LaunchDescription
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch.substitutions import Command
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    #find where folder is stored
    package_dir = get_package_share_directory('prosthetic_leg')

    #path to urdf
    urdf_file = os.path.join(package_dir, 'urdf', 'leg.urdf')

    #read urdf and find positions
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

    #gui
    joint_state_gui_node = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui'
    )

    #rviz2
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        #default urdf config
        arguments=['-d', os.path.join(
            get_package_share_directory('urdf_tutorial'),
            'rviz',
            'urdf.rviz'
        )]
    )

    #tell ros2 what nodes
    return LaunchDescription([
        robot_state_publisher_node,
        joint_state_gui_node,
        rviz_node
    ])
