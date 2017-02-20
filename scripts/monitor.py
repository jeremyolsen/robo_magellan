#!/usr/bin/env python
#
import rospy
import rospkg

from std_msgs.msg import String

import uav_state

# Enum maps to sound name
import soundmap

def monitor():
    rospy.init_node('monitor', anonymous=True)

    UAV = uav_state.UAV_State()

    pubFile  = rospy.Publisher('playfile', String, queue_size=10)
    pubToken = rospy.Publisher('play', String, queue_size=10)
    rate = rospy.Rate(0.5) # some hz

    # Get an instance of RosPack with the default search paths
    rospack = rospkg.RosPack()

    # Get the file path for rospy_tutorials
    basepath = rospack.get_path('robo_magellan') + "/scripts/sounds/"

    # TODO Are we connected to px? Is MAVROS up?

    # state
    play_file = False
    last_mode = None
    last_arm = None

    while not rospy.is_shutdown():
        #
        this_mode = str(UAV.get_mode())
        if this_mode != last_mode:
            pubToken.publish(this_mode)
            rospy.loginfo(this_mode)
        last_mode = this_mode

        #
        this_arm = UAV.get_arm()
        if this_arm != last_arm:
            token = soundmap.SoundMapEnum.ARMED.name
            if this_arm:
                token = soundmap.SoundMapEnum.ARMED.name
            else:
                token = soundmap.SoundMapEnum.DISARMED.name
            pubToken.publish(token)
            rospy.loginfo('Arm state: '+token)
        last_arm = this_arm

        #
        rate.sleep()

if __name__ == '__main__':
    # Start the node
    try:
        monitor()
    except rospy.ROSInterruptException:
        pass

