# Autopilot with Target Following for FPV Combat Drone (Guide for Developers)

## Architecture
The Autopilot "BEE" has a multi-threaded architecture. At its core, it has a command queue and a command router which is responsible for processing all queued commands. The router operates within its own thread, called the `Router thread`, while two other processes — the `Telemetry thread` and the `Terminator thread` — simply append commands to the queue.

![image](https://github.com/under0tech/autopilot_bee_sim/assets/113665703/adc549b2-6c00-4d3b-943d-f531d67c705b)

The `Telemetry thread` is tasked with adding commands to the queue for system monitoring and telemetry requests, providing the Autopilot with vital information on current altitude and aircraft speed. It inserts telemetry requests every 4 seconds.

`Terminator thread` is responsible for adding commands that lead to locating, tracking, and destroying the target. It adds such commands every second.

While in operation, the Autopilot utilizes various sub-modules, including computer vision with [YOLOv8 from Ultralytics](https://www.ultralytics.com), [Microsoft AirSim module](https://pypi.org/project/airsim) for notifications, and camera screens from the Simulator. [MAVLink commands](https://www.ardusub.com/developers/pymavlink.html) are employed for controlling the FPV Drone and sending notifications to Ground Control station ([Ardupilot](https://ardupilot.org)).

## main.py and threads
`main.py` serves as the primary file for starting the Autopilot. To execute it, please refer to the instructions outlined in [README.md](README.md). Upon initiation, it establishes the command queue, initializes the sub-processes (threads) detailed above, and adds the `INIT command` for autopilot initialization, facilitating the request of all streams from the FPV Drone.

## Autopilot state and settings
Autopilot has a few files which describes it initial state [autopilot.py](autopilot.py) and settings [definitions.py](definitions.py).
```python
state = {
    'connection' : False,
    'bee_state' : 'OFF', # OFF, READY, KILL, DESTROY
    'battery': 0,
    'speed': 0,
    'altitude': 0,
    'ruined': False,
    'frame': {},
    'target_lost': 0,
}
```
The `Autopilot state`, as listed below, is utilized for Autopilot operations and encompasses vital parameters that can be changed during program execution.

- **`connection`**: Upon establishment of a connection with the FPV Drone, this parameter remains `False`.
- **`bee_state`**: Can be set to one of the following modes: `OFF`, `READY`, `KILL`, `DESTROY`, as detailed in the introduction section of [README.md](README.md).
- **`battery`**: Indicates the current battery capacity in percentages. If the capacity drops below 20%, the Autopilot begins notifying the pilot with the message `low battery voltage`. When the percentage falls below 3%, it enforces the landing of the FPV Drone.
- **`speed`** and **`altitude`**: Reflect the current speed and altitude, respectively.
- **`ruined`**: Initially set as `False`, this parameter remains so until the bomb is installed on the drone.
- **`frame`**: Initially equal to `{}`, this parameter remains unchanged until the first target is recognized for tracking.
- **`target_lost`**: During the tracking process, if the target is lost, this parameter counts the number of times the target is lost. It uses in the additional logic related to controlling altitude in case of target loss.

```python
mavlink_url = 'tcp:localhost:5762'
logger_name = 'BEE-UA913'
vision_model = 'pt/yolov8n.pt'
vision_classes = [2] # 2-car, 7-truck, 0-Person
video_source = 0
camera_width = 256 # VideoCamera = 640, AIRSIM = 256
camera_height = 144 # VideoCamera = 480, AIRSIM = 144
airsim_camera = True # if False using VideoCamera
following_altitude = 4
target_lost_limit = 3
```

The `Autopilot settings`, as listed below, is utilized for Autopilot operations and encompasses settings for video camera, mavlink connection and so on.

- **`mavlink_url`**: Specifies the URL for connecting to the MAVLink interface, typically in the format `'tcp:localhost:5762'`.
- **`logger_name`**: Defines the name of the logger associated with the Autopilot, such as `'BEE-UA913'`.
- **`vision_model`**: Indicates the path to the vision model file used for object detection, e.g., `'pt/yolov8n.pt'`.
- **`vision_classes`**: Specifies the classes to be detected by the vision model, represented as a list of integers, e.g., `[2]` where 2 represents a car, 7 represents a truck, and 0 represents a person.
- **`video_source`**: Specifies the source of the video feed, typically represented as an integer, where `0` denotes the default camera source.
- **`camera_width`** and **`camera_height`**: Define the dimensions of the camera feed, where `camera_width` is the width of the frame and `camera_height` is the height. These values may vary depending on the source of the video feed, with different values specified for a VideoCamera (`640x480`) and AIRSIM (`256x144`) sources.
- **`airsim_camera`**: A boolean flag indicating whether to use the AIRSIM camera (`True`) or the default VideoCamera (`False`).
- **`following_altitude`**: Specifies the altitude (in meters) at which the drone will follow the target.
- **`target_lost_limit`**: Defines the maximum number of times the target can be lost during tracking before additional actions are taken (altitude control).

## Messages and logger
The application contains predefined messages for various situations and a list of targets to be notified accordingly. Messages can be sent to Ground Control (or FPV Goggles), AirSim console, application console, log, or all of them simultaneously. The logic for managing this functionality is implemented in [messages.py](messages.py). Additionally, [logger.py](logger.py) is utilized to log messages into a log file, which can be valuable for tracking the target path and investigating autopilot flight.

## MAVLink commands
Communication between the companion computer (autopilot) and the FPV Combat Drone is facilitated through MAVLink commands, which are listed in the file [commands.py](commands.py). These commands are responsible for various functions, including notifications to Ground Control, drone landing, telemetry requests, system monitoring, as well as commands for controlling the drone's altitude, direction, and movement. 

The file also contains predefined scenarios for target following, target search, preparation for attack, attack, fallback, and drone initialization. It encompasses all aspects of communication between the autopilot and FPV Drone.

Every command is associated with its specific delay period, indicating that the system (router) must wait until the command is executed. These delays are defined within the `command_delays` object.

## Router
...

## Computer vision
...
[How to prepare your own dataset and model for computer vision](https://medium.com/@dmytrosazonov/diy-for-a-spy-utilizing-yolov8-object-detection-in-military-operations-053d787b6f62)

## How to migrate to genuine FPV Combat Drone?
...

## Get in touch
Message me on Twitter if you have some questions.
https://twitter.com/dmytro_sazonov
