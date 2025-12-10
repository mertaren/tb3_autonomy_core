from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='tb3_autonomy',
            executable='patroller',
            name='patrol_manager',
            output='screen',
            parameters=[
                {'patrol_speed': 0.15}
            ]
        )
    ])