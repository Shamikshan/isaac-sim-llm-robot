import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from control_msgs.action import FollowJointTrajectory
from rclpy.action import ActionServer
from rclpy.action.server import ServerGoalHandle
import threading


class IsaacBridgeNode(Node):

    def __init__(self):
        super().__init__('isaac_bridge_node')

        # Publisher — sends joint positions to Isaac Sim
        self.isaac_pub = self.create_publisher(
            JointState,
            '/isaac_joint_command',
            10
        )

        # Action server — receives commands from MoveIt2
        self.action_server = ActionServer(
            self,
            FollowJointTrajectory,
            '/panda_arm_controller/follow_joint_trajectory',
            self.execute_callback
        )

        self.get_logger().info('Isaac Bridge Node ready')

    def execute_callback(self, goal_handle: ServerGoalHandle):
        self.get_logger().info('Received trajectory from MoveIt2')

        trajectory = goal_handle.request.trajectory
        joint_names = trajectory.joint_names

        # Execute each point in the trajectory
        for point in trajectory.points:
            msg = JointState()
            msg.header.stamp = self.get_clock().now().to_msg()
            msg.name = joint_names
            msg.position = list(point.positions)
            self.isaac_pub.publish(msg)

            # Small delay between points
            import time
            duration = point.time_from_start.sec + point.time_from_start.nanosec * 1e-9
            if duration > 0:
                time.sleep(0.05)

        goal_handle.succeed()
        self.get_logger().info('Trajectory execution complete')

        result = FollowJointTrajectory.Result()
        return result


def main(args=None):
    rclpy.init(args=args)
    node = IsaacBridgeNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
