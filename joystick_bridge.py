import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
import spidev


class JoystickBridge(Node):
    def __init__(self):
        super().__init__('joystick_bridge')
        #use a higher queue size to ensure smooth movement
        self.publisher_ = self.create_publisher(JointState, 'joint_states', 10)

        #SPI for MCP3008
        self.spi = spidev.SpiDev()
        self.spi.open(0, 0)
        self.spi.max_speed_hz = 1350000

        #20Hz update rate
        self.timer = self.create_timer(0.05, self.timer_callback)

    def read_adc(self, ch):
        #bitmasking        r = self.spi.xfer2([1, (8 + ch) << 4, 0])
        return ((r[1] & 3) << 8) + r[2]

    def map_val(self, val, out_min, out_max):
        #LERP
        return (val / 1023.0) * (out_max - out_min) + out_min

    def timer_callback(self):
        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()

        #list ALL joints in the URDF
        msg.name = [
            'HIP_1_Flexion',  # CH0
            'HIP_2_Lateral',  # CH1
            'KNEE_1_Flexion',  # CH2
            'KNEE_2_Rotation',  # Unassigned
            'ANKLE_1_Pitch',  # CH3
            'ANKLE_2_Roll'  # Unassigned
        ]

        #read POTs
        #if direction inverted - swap the min/max numbers (e.g., 1.57, -1.57)
        val0 = self.map_val(self.read_adc(0), -1.57, 1.57)
        val1 = self.map_val(self.read_adc(1), -0.5, 0.5)
        val2 = self.map_val(self.read_adc(2), 0.0, 1.57)
        val3 = self.map_val(self.read_adc(3), -0.6, 0.6)

        #set positions (0.0 for unassigned joints)
        msg.position = [val0, val1, val2, 0.0, val3, 0.0]

        self.publisher_.publish(msg)


def main():
    rclpy.init()
    node = JoystickBridge()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.spi.close()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
