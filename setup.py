from setuptools import find_packages, setup

package_name = 'llm_robot_bridge'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', ['launch/moveit_executor.launch.py']),
        ('share/' + package_name + '/config', ['config/moveit_cpp.yaml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='shamikshan',
    maintainer_email='shamikshan@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'llm_client_node = llm_robot_bridge.llm_client_node:main',
            'moveit_executor_node = llm_robot_bridge.moveit_executor_node:main',
            'isaac_bridge_node = llm_robot_bridge.isaac_bridge_node:main',
        ],
    },
)
