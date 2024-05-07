import airsim
import logger
import commands as mavs

client = airsim.MultirotorClient()

main_autopilot_started = {
    "log_info": "[AUTOPILOT STARTED]",
    "console": "\033[93m[AUTOPILOT STARTED]\033[0m"
    }

main_stopping_threads = {
    "log_info": "[STOPPING THREADS]",
    "console": "\033[93m[STOPPING THREADS]\033[0m"
    }

command_executor_done = {
    "log_info": "thread \'Command executor\', DONE.",
    "console": "thread \033[93mCommand executor\033[0m, DONE at {0}."
    }

command_executor_connected = {
    "log_info": "MAVLink connection is established: '{0}'",
    "console": "MAVLink connection is established: \033[92m{0}\033[0m"
    }

command_executor_executing_command = {
    "log_debug": "Executing command: {0}, Priority: {1}, Body: {2}",
    "console": "Executing command: {0}, Priority: {1}, Body: {2}"
    }

command_monitor_log = {
    "log_debug": "Monitoring: {0}",
    "console": "Monitoring: {0}"
    }

command_telemetry_log = {
    "log_debug": "Telemetry: {0}",
    "console": "Telemetry: {0}"
    }

command_monitor_battery_remaining = {
    "log_info": "low battery voltage {0}%",
    "console": "\033[93m[low battery voltage {0}%]\033[0m",
    "gc": "low battery voltage {0}%",
    "sim": "low battery voltage {0}%"
    }

command_telemetry_current_speed = {
    "log_info": "Current speed [{0} m/s]",
    "console": "current speed: - \033[93m[{0} m/s]\033[0m"
    }

command_telemetry_current_altitude = {
    "log_info": "Current altitude [{0} m]",
    "console": "current altitude: - \033[93m[{0} m]\033[0m"
    }

command_telemetry_autopilot_state = {
    "log_info": "Autopilot state: {0}",
    "console": "AUTOPILOT STATE: \033[95m{0}\033[0m"
    }

anti_drone_system_is_detected = {
    "log_info": "Anti-drone system is detected!",
    "console": "Anti-drone system is detected!",
    "gc": "Anti-drone system is detected!",
    "sim": "Anti-drone system is detected!"
    }

rc_lost_can_not_switch_to_kill_mode = {
    "log_info": "RC lost, can not switch to KILL mode!",
    "console": "RC lost, can not switch to KILL mode!",
    "gc": "RC lost, can not switch to KILL mode!",
    "sim": "RC lost, can not switch to KILL mode!"
    }

bee_state_changed_to = {
    "log_info": "Bee state changed to [{0}]",
    "console": "Bee state changed to [{0}]",
    "gc": "{0}",
    "sim": "{0}"
    }

initializing_autopilot = {
    "log_info": "Initializing autopilot",
    "console": "Initializing autopilot",
    "gc": "Initializing autopilot",
    "sim": "Initializing autopilot"
    }

command_kill_following_target = {
    "log_info": "[FOLLOWING TARGET N:{0}, E:{1}, D:{2}, Y:{3}]",
    "console": "\033[93m[FOLLOWING TARGET N:{0}, E:{1}, D:{2}, Y:{3}]\033[0m",
    "gc": "Target following",
    "sim": "FOLLOWING TARGET N:{0}, E:{1}, D:{2}, Y:{3}"
    }

command_kill_preparing_for_attack = {
    "log_info": "[PREPARING FOR ATTACK: target altitude 5m]",
    "console": "\033[93m[PREPARING FOR ATTACK]\033[0m",
    "gc": "PREPARING FOR ATTACK",
    "sim": "PREPARING FOR ATTACK"
    }

command_kill_target_attacked = {
    "log_info": "[TARGET ATTACKED]",
    "console": "\033[93m[TARGET ATTACKED]\033[0m",
    "gc": "TARGET ATTACKED",
    "sim": "TARGET ATTACKED"
    }

command_kill_fallback = {
    "log_info": "[FALLBACK]",
    "console": "\033[93mFALLBACK [10m back and left, 10m up]\033[0m",
    "gc": "FALLBACK",
    "sim": "FALLBACK"
    }

command_kill_mission_completed = {
    "log_info": "[MISSION COMPLETED]",
    "console": "\033[93mMISSION COMPLETED\033[0m",
    "gc": "MISSION COMPLETED",
    "sim": "MISSION COMPLETED"
    }

command_kill_target_lost = {
    "log_info": "[TARGET LOST]",
    "console": "\033[93mTARGET LOST\033[0m",
    "gc": "TARGET LOST",
    "sim": "TARGET LOST"
    }

telemetry_requestor_done = {
    "log_info": "thread \'Telemetry requestor\', DONE.",
    "console": "thread \033[93mTelemetry requestor\033[0m, DONE at {0}."
    }

terminator_process_done = {
    "log_info": "thread \'Terminator process\', DONE.",
    "console": "thread \033[93mTerminator process\033[0m, DONE at {0}."
    }

terminator_process_connecting = {
    "log_info": "Terminator: attempting to connect with '{0}'",
    "console": "Terminator: attempting to connect with \033[91m{0}\033[0m"
    }

terminator_process_connected = {
    "log_info": "Terminator: connected with '{0}'",
    "console": "Terminator: connected with \033[92m{0}\033[0m"
    }

telemetry_process_connecting = {
    "log_info": "Telemetry: attempting to connect with '{0}'",
    "console": "Telemetry: attempting to connect with \033[91m{0}\033[0m"
    }

telemetry_process_connected = {
    "log_info": "Telemetry: connected with '{0}'",
    "console": "Telemetry: connected with \033[92m{0}\033[0m"
    }

fatal_error = {
    "log_fatal": "{0}"
    }

main_autopilot_finished = {
    "log_info": "[AUTOPILOT FINISHED]",
    "console": "\033[93m[AUTOPILOT FINISHED]\033[0m"
    }

def display(msg, params=[]):
    if msg.get('log_info'):
        logger.log_message(None, msg['log_info'].format(*params), 'info')
    if msg.get('log_debug'):
        logger.log_message(None, msg['log_debug'].format(*params), 'debug')
    if msg.get('log_fatal'):
        logger.log_message(None, msg['log_fatal'].format(*params), 'fatal')
    if msg.get('console'):
        print(msg['console'].format(*params))
    if msg.get('gc'):
        mavs.send_message_to_gc(msg['gc'].format(*params))
    if msg.get("sim"):
        client.simPrintLogMessage(msg['sim'].format(*params),'',1)
