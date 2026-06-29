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

        #have both rviz and gazebo
        ('share/' + package_name + '/launch', glob('launch/*.launch.py')),

        #call urdf
        ('share/' + package_name + '/urdf', glob('urdf/*')),

        #rviz
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
