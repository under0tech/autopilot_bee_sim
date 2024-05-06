# Autopilot with Target Following for FPV Combat Drone (Simulator version)

## Autopilot "BEE"
Autopilot "BEE", installed on the companion computer on the FPV Combat Drone, has the ability to locate and track targets autonomously. It can approach targets, prepare for an attack, execute the attack (releasing the bomb), and safely fallback to complete the mission — all without requiring operator involvement. The system operates in automatic mode. It can also detect anti-drone systems and switch into KILL mode to neutralize threat.

### MODES:
`OFF`  -  autopilot is inactive, awaiting operator input to switch to any of the modes. Only telemetry monitoring and logging are active.

`READY`  -  in addition to the functionalities of the previous mode, the Anti-Drone system is activated for threat recognition, with the option to switch to the `KILL` mode.

`KILL`  -  automatically activated when the Anti-Drone system detects a threat. Tasks align with those of the `DESTROY` mode.

`DESTROY`  -  locate and neutralize a target. Autopilot activates the camera, scans for targets, captures them upon detection, and proceeds with destruction.

## Simulator
Simulator version is designed to develop and debug computer vision with target following and entire Autopilot work using `Microsoft AirSim`, `ArduCopter SITL` and `Mission Planner` running on Linux.

## Environment
For the development and debugging process, a robust computer is necessary due to the requirements for `Microsoft AirSim`. During the Autopilot development I used an `Ubuntu 23.10 - based computer` equipped with a `16-Core processor` and `16GB RAM`.

Set up the environment:
1. [Microsoft AirSim](https://github.com/Microsoft/AirSim/releases)
2. [ArduCopter SITL](https://ardupilot.org/dev/docs/sitl-with-airsim.html)
3. [Mission Planner](https://ardupilot.org/planner/)

Copy files from the folder `env` to their destinations:
1. File `gc.sh` to the folder `~/Apps/MissionPlanner`
2. File `settings.json` to the folder `~/Documents/AirSim`
3. File `run.py` to the folder `~/Apps/AirSim`

Run the environment:
```bash
cd ~/Apps/AirSim
python3 run.py
```
If all three programs have started successfully, you'll be able to view the copter in the `AirSim Simulator` and control its motor arming/disarming using `Mission Planner`. This indicates that the installation was successful, and you can proceed.

## Be ready for Autopilot run
Before starting the Autopilot, ensure the copter is properly configured using `Mission Planner`.
1. Navigate to the `Actions` tab and switch the copter to `Guided` mode.
   
   ![image](https://github.com/under0tech/autopilot_bee_sim/assets/113665703/5a2ba9e4-30d3-4da1-b8fe-f856ccc2aa82)
3. In the `Actions` tab, ARM the motors.
   
   ![image](https://github.com/under0tech/autopilot_bee_sim/assets/113665703/866ac070-41cc-463a-ae6f-8b9fd1595350)
5. Perform a takeoff with an altitude of 4m.
   
   ![image](https://github.com/under0tech/autopilot_bee_sim/assets/113665703/81bf43a9-963e-4319-b7bb-4ffb0da1a235)
7. In the `Servo\Relay` tab, set `Low` for `servo 5`. This indicates that the Autopilot is in the `OFF` mode.
8. In the `Servo\Relay` tab, set `High` for `servo 6`. This indicates that the bomb is armed and onboard.
   
   ![image](https://github.com/under0tech/autopilot_bee_sim/assets/113665703/6d582501-4db7-4691-aed7-3df5b7b22388)

Go to the `AirSim game` and ensure that the copter is at an altitude of 4m. Press `Ctrl+3` to show the front camera view (which uses in the target following process).

![image](https://github.com/under0tech/autopilot_bee_sim/assets/113665703/04d3a434-f111-4972-864e-43c8b763eb5d)

## How to Use
1. Install the required dependencies using `requirements.txt`.
```bash
pip install -r requirements.txt
```
2. Run the Autopilot, using `python3 main.py` command.
```bash
python3 main.py
```
Afterward, monitor the Autopilot's activity in your `Terminal` and logs. At its start, the autopilot is in `OFF` mode, meaning it won't locate or follow the target. To activate this function, switch `servo 5` to `High`, indicating a transition to `DESTROY` mode. Now, go to the `AirSim game` and observe the Autopilot in action.

![image](https://github.com/under0tech/autopilot_bee_sim/assets/113665703/6818e8d3-b7ea-40a1-bfdd-37df8ec793d0)

## Customize this Autopilot
The primary objective of sharing this source code is to initiate discussions within the developer community in Ukraine about automated combat drones. This initiative aims to establish a strategic advantage on the battlefield by implementing automated flight systems equipped with computer vision on homeborn FPV drones to bolster support for the Ukrainian army.

If you are a developer or possess developer skills, feel free to utilize this code to develop your own Autopilots integrated with Computer Vision capabilities. For more detailed instructions, please refer to [README_DEV.md](README_DEV.md). Share your creations with those involved in the production and supply of FPV drones for the Ukrainian military and #SupportUkraine in such way.

## Troubleshooting
Be patient while setting up the environment and familiarizing yourself with each component. There are plenty of pitfalls that may demand your attention and time to resolve. This is normal. It took me a few weeks to set up and run the environment.

## Get in touch
Text me on Twitter if you have any questions.
https://twitter.com/dmytro_sazonov
