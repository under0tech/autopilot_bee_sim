import subprocess
import os

def run_process(command):
    print(f"Running command: {command}")
    process = subprocess.Popen(command, shell=True)

if __name__ == "__main__":
    commands = [
        "~/Apps/Simulator/AirSimNH/LinuxNoEditor/AirSimNH.sh",
        "cd ~/Apps/ardupilot && sim_vehicle.py -v ArduCopter -f airsim-copter",
        "cd ~/Apps/MissionPlanner && ./gc.sh"
    ]

    for command in commands:
        run_process(command)
