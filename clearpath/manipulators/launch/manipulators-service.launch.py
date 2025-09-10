from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument, ExecuteProcess
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import EnvironmentVariable, FindExecutable, PathJoinSubstitution, LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():

    # Include Packages
    pkg_clearpath_manipulators = FindPackageShare('clearpath_manipulators')

    # Declare launch files
    launch_file_moveit = PathJoinSubstitution([
        pkg_clearpath_manipulators, 'launch', 'moveit.launch.py'])

    # Include launch files
    launch_moveit = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([launch_file_moveit]),
        launch_arguments=
            [
                (
                    'setup_path'
                    ,
                    '/home/salva/clearpath/'
                )
                ,
                (
                    'use_sim_time'
                    ,
                    'true'
                )
                ,
                (
                    'namespace'
                    ,
                    'a200_0000'
                )
                ,
            ]
    )

    # Create LaunchDescription
    ld = LaunchDescription()
    ld.add_action(launch_moveit)
    return ld
