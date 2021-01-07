# Drone Line Tracker

Gazebo simulator with Hector quadrotor (http://mirror.umd.edu/roswiki/hector_quadrotor.html) to train for line tracking.

This is a in progress project. 
The code is a modification of below project:

```
https://github.com/TIERS/drone-racing

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

You should see the original and processed camera frame

Run Hydrid Drone Control node for tello command and autonomous control of the drone thorugh the keyboard
```
rosrun tiers_drone_racing hybrid_controller.py
```


## Contact

To be added after completing the project
