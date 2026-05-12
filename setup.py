from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'prosthetic_leg'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
         ['resource/prosthetic_leg']),
        ('share/' + package_name, ['package.xml']),

        # This line now includes BOTH your RViz display and your Gazebo sim launch files
        ('share/' + package_name + '/launch', glob('launch/*.launch.py')),

        # This ensures your URDF folder and everything inside it gets installed
        ('share/' + package_name + '/urdf', glob('urdf/*')),

        # Added a placeholder for RViz config files (useful for the symposium!)
        ('share/' + package_name + '/rviz', glob('rviz/*.rviz')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='lr27',
    maintainer_email='lr27@todo.todo',
    description='Prosthetic Leg Simulation for ROS 2 Jazzy',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            # If you want to make a shortcut like "leg_demo", you'd put it here
        ],
    },
)