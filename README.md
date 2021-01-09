# Drone Line Tracker

Gazebo simulator with Hector quadrotor (http://mirror.umd.edu/roswiki/hector_quadrotor.html) to train for line tracking.

<<<<<<< HEAD
This is a in progress project.
=======
This is a in progress project. 
>>>>>>> b9e8a653c8ffdfd5109200f41266388519e66ffb
The code is a modification of below project:

```
https://github.com/TIERS/drone-racing
<<<<<<< HEAD

```
For installation, refer to the above link.
The project is yet in early stage of development and not completely functional


## Requirement

Ubuntu 18.04 with ROS Melodic, OpenCV




## Run the simulator

Start Gazebo Simularo with command:

```
roslaunch tiers_drone_racing my_world.launch
```

Spawn the Quarator with embeddad dowward camera with below command
```
roslaunch hector_quadrotor_gazebo spawn_quadrotor_with_downward_cam.launch
```
Start RVIZ for furture analysis with
```
rosrun rviz rviz -d `rospack find hector_quadrotor_demo`/rviz_cfg/outdoor_flight.rviz
```

Run the node for camera vision proseccor with:
```
rosrun  tiers_drone_racing image_pub_sub.py
```
=======

```
For installation, refer to the above link.
The project is yet in early stage of development and not completely functional


## Requirement

Ubuntu 18.04 with ROS Melodic, OpenCV



>>>>>>> b9e8a653c8ffdfd5109200f41266388519e66ffb

You should see the original and processed camera frame

<<<<<<< HEAD
Run Hydrid Drone Control node for tello command and autonomous control of the drone thorugh the keyboard
```
rosservice call /enable_motors "enable: true"
rosrun tiers_drone_racing hybrid_controller.py
```
=======
Start Gazebo Simularo with command:

```
roslaunch tiers_drone_racing my_world.launch
```

Spawn the Quarator with embeddad dowward camera with below command
```
roslaunch hector_quadrotor_gazebo spawn_quadrotor_with_downward_cam.launch
```
Start RVIZ for furture analysis with
```
rosrun rviz rviz -d `rospack find hector_quadrotor_demo`/rviz_cfg/outdoor_flight.rviz
``` 

Run the node for camera vision proseccor with:
```
rosrun  tiers_drone_racing image_pub_sub.py 
```

You should see the original and processed camera frame

Run Hydrid Drone Control node for tello command and autonomous control of the drone thorugh the keyboard
```
rosservice call /enable_motors "enable: true"
rosrun tiers_drone_racing hybrid_controller.py
```
>>>>>>> b9e8a653c8ffdfd5109200f41266388519e66ffb


## Contact

To be added after completing the project
