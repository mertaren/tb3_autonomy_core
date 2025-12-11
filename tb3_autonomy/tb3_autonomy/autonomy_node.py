#!/usr/bin/env python3
import time
import rclpy
from rclpy.node import Node
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import String

# Global param
detected_object = None

class DetectionListener(Node):
    def __init__(self):
        super().__init__('detection_listener')
        self.subscription = self.create_subscription(
            String,
            '/detected_object',
            self.listener_callback,
            10) # QoS

    def listener_callback(self, msg):
        global detected_object
        detected_object = msg.data
        # self.get_logger().info(f"Anomaly Detected: {msg.data}")

def main():
    rclpy.init()
    
    nav = BasicNavigator()
    listener = DetectionListener()
    
    # Start log
    print("--- System is Starting Up ---")
    
    # Goal 1
    p1 = PoseStamped()
    p1.header.frame_id = 'map'
    p1.header.stamp = nav.get_clock().now().to_msg()
    p1.pose.position.x = 0.297996461391449
    p1.pose.position.y = 2.288670063018799
    p1.pose.orientation.w = 1.0

    # Goal 2
    p2 = PoseStamped()
    p2.header.frame_id = 'map'
    p2.header.stamp = nav.get_clock().now().to_msg()
    p2.pose.position.x = -1.671874403953552
    p2.pose.position.y = 0.5187898278236389
    p2.pose.orientation.w = 1.0

    waypoints = [p1, p2]
    
    
    while rclpy.ok():
        nav.followWaypoints(waypoints)

        # Game loop
        while not nav.isTaskComplete():
            
            rclpy.spin_once(listener, timeout_sec=0.1)
            
            # Anomaly check
            global detected_object
            if detected_object is not None:
                print(f"!!! Anomaly Detected: {detected_object} !!!")
                print("Robot is shutting down...")
                
                # Cancel nav
                nav.cancelTask()
                
                # İnceleme 5 saniye sürer.
                print("Investigation is underway. Please wait...")
                time.sleep(5.0)
                
                print("Threat detected. Patrol continues.")
                detected_object = None # flag reset
                
                nav.followWaypoints(waypoints)
        
        
        # if it's one-time
        #   break
        

    rclpy.shutdown()

if __name__ == '__main__':
    main()