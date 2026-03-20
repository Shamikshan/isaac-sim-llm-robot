import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import requests
import json

# Paste your Cloudflare URL here
COLAB_URL = "https://captain-newfoundland-forth-radiation.trycloudflare.com"

class LLMClientNode(Node):

    def __init__(self):
        super().__init__('llm_client_node')

        # Subscriber: listens for scene descriptions
        self.scene_sub = self.create_subscription(
            String,
            '/scene_description',
            self.scene_callback,
            10
        )

        # Publisher: publishes the action received from Qwen
        self.action_pub = self.create_publisher(
            String,
            '/robot_action',
            10
        )

        self.get_logger().info('LLM Client Node started. Waiting for scene descriptions...')

    def scene_callback(self, msg):
        scene = msg.data
        self.get_logger().info(f'Received scene: {scene}')

        # Send to Colab
        try:
            response = requests.post(
                f"{COLAB_URL}/generate",
                json={"prompt": scene},
                timeout=30
            )
            result = response.json()
            action_str = result["response"]
            self.get_logger().info(f'Qwen response: {action_str}')

            # Validate it's proper JSON
            action = json.loads(action_str)
            self.get_logger().info(f'Parsed action: {action}')

            # Publish to /robot_action topic
            out_msg = String()
            out_msg.data = action_str
            self.action_pub.publish(out_msg)

        except requests.exceptions.Timeout:
            self.get_logger().error('Request to Colab timed out')
        except json.JSONDecodeError:
            self.get_logger().error(f'Qwen returned invalid JSON: {action_str}')
        except Exception as e:
            self.get_logger().error(f'Error: {str(e)}')


def main(args=None):
    rclpy.init(args=args)
    node = LLMClientNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()