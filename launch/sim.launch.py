import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
    #setup paths
    pkg_dir = get_package_share_directory('prosthetic_leg')
    urdf_file = os.path.join(pkg_dir, 'urdf', 'leg.urdf')

    #start gazebo
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py')]),
        launch_arguments={'gz_args': '-r empty.sdf'}.items(),
    )

    #state publisher
    rsp = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': open(urdf_file).read(), 'use_sim_time': True}]
    )

    #spawn robot
    spawn_robot = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-name', 'prosthetic_leg',
            '-file', urdf_file,
            '-x', '0', '-y', '0', '-z', '1.0'
        ],
        output='screen'
    )

    return LaunchDescription([
        gazebo,
        rsp,
        spawn_robot
    ])
