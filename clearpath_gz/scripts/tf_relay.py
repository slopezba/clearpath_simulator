#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from tf2_msgs.msg import TFMessage
from rclpy.qos import QoSProfile, QoSDurabilityPolicy, QoSReliabilityPolicy, QoSHistoryPolicy


class TFFlexibleRelay(Node):
    def __init__(self):
        super().__init__('tf_flexible_relay')

        # QoS flexible para tf (acepta volatile o transient_local)
        qos_tf_flexible = QoSProfile(
            reliability=QoSReliabilityPolicy.RELIABLE,
            durability=QoSDurabilityPolicy.SYSTEM_DEFAULT,  # se adapta
            history=QoSHistoryPolicy.KEEP_ALL,
            depth=0  # depth=0 para KEEP_ALL
        )

        # QoS para tf_static (siempre transient_local)
        qos_tf_static = QoSProfile(depth=1)
        qos_tf_static.durability = QoSDurabilityPolicy.TRANSIENT_LOCAL

        # Suscriptores
        self.sub_tf = self.create_subscription(
            TFMessage, '/a200_0000/tf', self.tf_callback, qos_tf_flexible)
        self.sub_tf_static = self.create_subscription(
            TFMessage, '/a200_0000/tf_static', self.tf_static_callback, qos_tf_static)

        # Publicadores (lo normal: /tf con VOLATILE, /tf_static con TRANSIENT_LOCAL)
        qos_tf_out = QoSProfile(depth=100)
        qos_tf_out.durability = QoSDurabilityPolicy.VOLATILE

        self.pub_tf = self.create_publisher(TFMessage, '/tf', qos_tf_out)
        self.pub_tf_static = self.create_publisher(TFMessage, '/tf_static', qos_tf_static)

        self.get_logger().info(
            "Relay flexible activo: /a200_0000/tf → /tf (VOLATILE), /a200_0000/tf_static → /tf_static"
        )

    def tf_callback(self, msg: TFMessage):
        self.pub_tf.publish(msg)

    def tf_static_callback(self, msg: TFMessage):
        self.pub_tf_static.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = TFFlexibleRelay()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    rclpy.shutdown()


if __name__ == "__main__":
    main()
