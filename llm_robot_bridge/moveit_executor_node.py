import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import PoseStamped
import json

from moveit import MoveItPy


class MoveItExecutorNode(Node):

    def __init__(self):
        super().__init__('moveit_executor_node')

        # MoveItPy gets all params from the launch file
        self.moveit = MoveItPy(node_name='moveit_executor_node')
        self.arm = self.moveit.get_planning_component('panda_arm')
        self.get_logger().info('MoveIt2 Executor Node ready')

        self.action_sub = self.create_subscription(
            String,
            '/robot_action',
            self.action_callback,
            10
        )

    def action_callback(self, msg):
        try:
            action = json.loads(msg.data)
            self.get_logger().info(f'Received action: {action}')

            if action['action'] == 'pick':
                target = action['target_position']
                self.move_to_position(target[0], target[1], target[2])
            else:
                self.get_logger().warn(f'Unknown action: {action["action"]}')

        except json.JSONDecodeError:
            self.get_logger().error('Invalid JSON received')
        except KeyError as e:
            self.get_logger().error(f'Missing key in action: {e}')

    def move_to_position(self, x, y, z):
        self.get_logger().info(f'Moving to position: x={x}, y={y}, z={z}')

        target_pose = PoseStamped()
        target_pose.header.frame_id = 'panda_link0'
        target_pose.header.stamp = self.get_clock().now().to_msg()
        target_pose.pose.position.x = x
        target_pose.pose.position.y = y
        target_pose.pose.position.z = z
        target_pose.pose.orientation.x = 1.0
        target_pose.pose.orientation.y = 0.0
        target_pose.pose.orientation.z = 0.0
        target_pose.pose.orientation.w = 0.0

    # Wait a moment for current state to be fresh
        import time
        time.sleep(0.5)

        self.arm.set_start_state_to_current_state()
        self.arm.set_goal_state(
            pose_stamped_msg=target_pose,
            pose_link='panda_link8'
        )

        plan_result = self.arm.plan()

        if plan_result:
            self.get_logger().info('Plan found! Switching to Isaac Sim in 5 seconds...')
            import time
            time.sleep(5)
            self.get_logger().info('Executing now!')
            self.moveit.execute(
                plan_result.trajectory,
                controllers=['panda_arm_controller']
            )
            self.get_logger().info('Execution complete')

        else:
            self.get_logger().error('Planning failed - target may be unreachable')


def main(args=None):
    rclpy.init(args=args)
    node = MoveItExecutorNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
