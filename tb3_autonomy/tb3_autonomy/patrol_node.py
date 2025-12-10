import rclpy
from rclpy.node import Node

class PatrolNode(Node):
    def __init__(self):
        super().__init__('patrol_node')
        self.get_logger().info("Patrol System Initializing...")
        
        # Params
        self.declare_parameter('patrol_speed', 0.1)
        
        #self.create_subscription(test_state, '/test_state', self.test_callback, 10)
        
        # Control loop - 10hz
        self.timer = self.create_timer(0.1, self.control_loop)
        
        self.get_logger().info("Patrol System Ready! Waiting for commands...")

    def control_loop(self):
        """
        for State machine
        """
        self.get_logger().info("Patrol Loop ALIVE!", throttle_duration_sec=5)
        pass

def main(args=None):
    rclpy.init(args=args)
    node = PatrolNode()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Shutting down patrol node...")
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()