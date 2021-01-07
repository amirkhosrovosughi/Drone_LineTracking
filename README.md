# Drone Line Tracker

Gazebo simulator with Hector quadrotor (http://mirror.umd.edu/roswiki/hector_quadrotor.html) to train for line tracking
This is a in progress project
The code is a modification of:

```
https://github.com/TIERS/drone-racing

```
For installation, refer to the above link.


## Requirement

Ubuntu 18.04 with ROS Melodic already installed.




## Run the simulator

Start Gazebo Simularo with command:

```
source ~/drone_racing_ws/devel/setup.bash
roslaunch tiers_drone_racing hector_dronerace.launch
```

Start the motors in another terminal window/tab:
```
source ~/drone_racing_ws/devel/setup.bash
rosservice call /enable_motors "enable: true"
```

In order to control the UAV with keyboard teleop, install it with
```
sudo apt install ros-melodic-teleop-twist-keyboard
``` 

if you don't have it yet, and run the teleop node in a separate terminal window/tab:
```
rosrun tiers_drone_racing tello_controller.py 
```

## Camera view

Install the `image_view` package:
```
sudo apt install ros-melodic-image-view
```

```
rosrun image_view image_view image:=/camera/rgb/image_raw
```

## Contact

For any questions, write to `jopequ@utu.fi`.

Visit us at [https://tiers.utu.fi](https://tiers.utu.fi)
