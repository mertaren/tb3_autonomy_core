import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import String
from cv_bridge import CvBridge
from ultralytics import YOLO
import cv2

class PerceptionNode(Node):
    def __init__(self):
        super().__init__('perception_node')
        self.get_logger().info("Perception node started...")
        
        # Bridge object
        self.bridge = CvBridge()
        
        self.publisher_ = self.create_publisher(String,
                                                '/detected_object',
                                                10)
        
        self.subscription = self.create_subscription(
            Image,  
            '/camera/image_raw', 
            self.image_callback,  
            10)  # QoS 
        
        self.model = YOLO('yolov8n.pt')
        self.get_logger().info("Model loaded.")        
        
    def image_callback(self, msg):
        
        try:
            cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
            
            results = self.model(cv_image, verbose=False, imgsz=640)
            
            annotated_frame = results[0].plot()
            
            detection_msg = String()
            
            if len(results[0].boxes) > 0:
                # Get object ID
                class_id = int(results[0].boxes[0].cls)
                # Transform ID to String
                object_name = results[0].names[class_id]
                
                # Publish
                self.get_logger().info(f"Detected: {object_name}")
                detection_msg.data = object_name
                self.publisher_.publish(detection_msg)
            else:
                pass
            
            cv2.imshow("Robot Cam", annotated_frame)
            cv2.waitKey(1)
            
        except Exception as e:
            self.get_logger().error(f"Error: {e}")
        
def main(args=None):
    rclpy.init(args=args)
    node = PerceptionNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
    
if __name__ == '__main__':
    main()    
    
        