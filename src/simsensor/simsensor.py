import os
import rospy
import rospkg

from geometry_msgs.msg import TwistWithCovarianceStamped

from qt_gui.plugin import Plugin
from python_qt_binding import loadUi
from python_qt_binding.QtWidgets import QWidget

from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtGui import *

class SimSensor(Plugin):
    def __init__(self, context):
        super(SimSensor, self).__init__(context)
        self.setObjectName('SimSensor')

        self._widget = QWidget()
        ui_file = os.path.join(rospkg.RosPack().get_path('simsensor'), 'resource', 'SimSensor.ui')
        loadUi(ui_file, self._widget)
        self._widget.setObjectName('SimSensorUi')
        if context.serial_number() > 1:
            self._widget.setWindowTitle(self._widget.windowTitle() + (' (%d)' % context.serial_number()))
        context.add_widget(self._widget)

        self.twist_msg = TwistWithCovarianceStamped()
        self.twist_msg.header.frame_id = "base_link"

        self.twist_pub = rospy.Publisher("twist", TwistWithCovarianceStamped, queue_size=10)
        self.timer = rospy.Timer(rospy.Duration(1.0/30), self.timer_callback)

        self._widget.twist_x_slider.valueChanged.connect(self.x_changed)
        self._widget.twist_y_slider.valueChanged.connect(self.y_changed)
        self._widget.twist_z_slider.valueChanged.connect(self.z_changed)
        self._widget.twist_roll_slider.valueChanged.connect(self.roll_changed)
        self._widget.twist_pitch_slider.valueChanged.connect(self.pitch_changed)
        self._widget.twist_yaw_slider.valueChanged.connect(self.yaw_changed)
        self._widget.frame_edit.textChanged.connect(self.frame_changed)
       
    @pyqtSlot()
    def frame_changed(self):
        self.twist_msg.header.frame_id = self._widget.frame_edit.text()
 
    @pyqtSlot()
    def x_changed(self):
        self.twist_msg.twist.twist.linear.x = self._widget.twist_x_slider.value()/100.0
        self._widget.twist_x_lcd.display(self.twist_msg.twist.twist.linear.x)
    
    @pyqtSlot()
    def y_changed(self):
        self.twist_msg.twist.twist.linear.y = self._widget.twist_y_slider.value()/100.0
        self._widget.twist_y_lcd.display(self.twist_msg.twist.twist.linear.y)
    
    @pyqtSlot()
    def z_changed(self):
        self.twist_msg.twist.twist.linear.z = self._widget.twist_z_slider.value()/100.0
        self._widget.twist_z_lcd.display(self.twist_msg.twist.twist.linear.z)
    
    @pyqtSlot()
    def roll_changed(self):
        self.twist_msg.twist.twist.angular.x = self._widget.twist_roll_slider.value()/100.0
        self._widget.twist_roll_lcd.display(self.twist_msg.twist.twist.angular.x)
    
    @pyqtSlot()
    def pitch_changed(self):
        self.twist_msg.twist.twist.angular.y = self._widget.twist_pitch_slider.value()/100.0
        self._widget.twist_pitch_lcd.display(self.twist_msg.twist.twist.angular.y)
    
    @pyqtSlot()
    def yaw_changed(self):
        self.twist_msg.twist.twist.angular.z = self._widget.twist_yaw_slider.value()/100.0
        self._widget.twist_yaw_lcd.display(self.twist_msg.twist.twist.angular.z)
    
    def shutdown_plugin(self):
        self.timer.shutdown()
        self.twist_pub.unregister()

    def timer_callback(self, event):
        self.twist_msg.header.stamp = event.current_real
        self.twist_msg.header.seq += 1
        self.twist_pub.publish(self.twist_msg)

    def save_settings(self, plugin_settings, instance_settings):
        pass
    def restore_settings(self, plugin_settings, instance_settings):
        pass

