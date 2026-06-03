import launch
import launch_ros
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    # 获取默认的urdf路径
    urdf_package_path = get_package_share_directory('fishbot_description')
    default_urdf_path = os.path.join(urdf_package_path, 'urdf', 'fishbot', 'fishbot.urdf.xacro')
    default_rviz2_config_path = os.path.join(urdf_package_path, 'config', 'display_robot_model.rviz')
    
    # 定义SDF世界文件路径
    world_file_path = os.path.join(urdf_package_path, 'worlds', 'warehouse_world.sdf')
    
    # 定义桥接配置文件路径
    gazebo_config_path = os.path.join(urdf_package_path, 'config', 'gazebo_bridge.yaml')
    
    # 声明一个urdf目录的参数
    action_declare_arg_mode_path = launch.actions.DeclareLaunchArgument(
        name='model',
        default_value=str(default_urdf_path),
        description='加载的模型文件路径'
    )

    # 通过文件路径，获取内容，并转换成参数值对象
    substitutions_command_result = launch.substitutions.Command(
        ['xacro ', launch.substitutions.LaunchConfiguration('model')]
    )
    robot_description_value = launch_ros.parameter_descriptions.ParameterValue(
        substitutions_command_result, value_type=str
    )

    # 机器人状态发布器
    action_robot_state_publisher = launch_ros.actions.Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': robot_description_value}]
    )

    # 关节状态发布器
    action_joint_state_publisher = launch_ros.actions.Node(
        package='joint_state_publisher',
        executable='joint_state_publisher'
    )

    # 启动Gazebo  world_file_path
    action_gz_sim = launch.actions.IncludeLaunchDescription(
        launch.launch_description_sources.PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py')
        ),
        launch_arguments={
            'gz_args': world_file_path + ' -r'  
        }.items()
    )

    # 将机器人模型生成到Gazebo中
    action_gz_spawn = launch_ros.actions.Node(
        package='ros_gz_sim',
        executable='create',
        arguments=['-topic', 'robot_description'],
        output='screen'
    )

    # ROS-Gazebo桥接节点
    action_gz_bridge = launch_ros.actions.Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        parameters=[{'config_file': gazebo_config_path}],
        output='screen'
    )

    # RViz2可视化
    action_rviz2_node = launch_ros.actions.Node(
        package='rviz2',
        executable='rviz2',
        arguments=['-d', default_rviz2_config_path],
        output='screen'
    )

    return launch.LaunchDescription([
        action_declare_arg_mode_path,
        action_robot_state_publisher,
        action_joint_state_publisher,
        action_gz_sim,
        action_gz_spawn,
        action_gz_bridge,
        action_rviz2_node,
    ])