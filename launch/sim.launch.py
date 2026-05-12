import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
    # 1. Setup paths
    pkg_dir = get_package_share_directory('prosthetic_leg')
    urdf_file = os.path.join(pkg_dir, 'urdf', 'leg.urdf')

    # 2. Start Gazebo (Harmonic)
    # This launches the empty simulator world
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py')]),
        launch_arguments={'gz_args': '-r empty.sdf'}.items(),
    )

    # 3. Robot State Publisher
    # Still needed so Gazebo knows the robot structure
    rsp = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': open(urdf_file).read(), 'use_sim_time': True}]
    )

    # 4. Spawn the robot in Gazebo
    # This takes the URDF and places it at (0,0,1) meter height
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