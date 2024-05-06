# Autopilot with Target Following for FPV Combat Drone 
(Simulator version BEE_SIM_00_01)

## Autopilot "BEE"
Autopilot "BEE", installed on the companion computer on the FPV Combat Drone, has the ability to locate and track targets autonomously. It can approach targets, prepare for an attack, execute the attack (releasing the bomb), and safely fallback to complete the mission — all without requiring operator involvement. The system operates in automatic mode. It can also detect anti-drone systems and switch into KILL mode to neutralize threat.

### MODES:
`OFF` - autopilot is waiting from roperator to be switched onto any of the modes. No one module work besides listening to telemetry and logging.

`READY` - besides all modules listed in the previous mode also included Anti-Drone system work recognition with further switching to mode `KILL`.

`KILL` - switched into this mode automatically because of anti-drone system is detected. Task the same as for 'DESTROY'.

`DESTROY` - find a target and destroy that. In this mode autopilot switch on camera and look for targets and in case the target is detected it capture the target and follow for destroying.

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
2. In the `Actions` tab, ARM the motors.
3. Perform a takeoff with an altitude of 4m.
4. In the `Servo\Relay` tab, set `Low` for `servo 5`. This indicates that the Autopilot is in the `OFF` mode.
5. In the `Servo\Relay` tab, set `High` for `servo 6`. This indicates that the bomb is armed and onboard.

Go to the `AirSim game` and ensure that the copter is at an altitude of 4m. Press `Ctrl+3` to show the front camera view (which uses in the target following process).

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

## Troubleshooting
Be patient while setting up the environment and familiarizing yourself with each component. There are plenty of pitfalls that may demand your attention and time to resolve. This is normal. It took me a few weeks to set up and run the environment correctly.

## Get in touch
Message me on Twitter if you have any questions.
https://twitter.com/dmytro_sazonov
