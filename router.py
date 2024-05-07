import time
import queue
import vision
import messages
import autopilot

import commands as mavs
import definitions as vars

command_queue = queue.PriorityQueue()

class Command:
    def __init__(self, priority, name, body):
        self.priority = priority
        self.name = name
        self.body = body

    def __lt__(self, other):
        return self.priority < other.priority

def put_command(command):
    command_queue.put(command)

def command_executor(stop_command):
    connection = False
    while not connection and not stop_command.is_set():
        try:
            time.sleep(2)
            con = mavs.connect()
            messages.display(messages.command_executor_connected, [vars.mavlink_url])
            mavs.disconnect(con[0])
            connection = True
            autopilot.state['connection'] = True
        except Exception as e:
            messages.display(messages.fatal_error, [e])
            pass

    while not stop_command.is_set():
        try:
            command = command_queue.get(timeout=1)
            execute_command(command)
            command_queue.task_done()
            time.sleep(1)
        except:
            pass

    stopped_time = time.strftime("%H:%M:%S, %Y, %d %B", time.localtime())  
    messages.display(messages.command_executor_done, [stopped_time])

def execute_command(command):
    messages.display(messages.command_executor_executing_command, 
                     [command.name, command.priority, command.body])

    if command.name in commands:
        commands[command.name](command.body)

def command_monitor(params):
    monitor = mavs.telemetry(params['target'])
    messages.display(messages.command_monitor_log, [monitor])

    if monitor != {}:
        if params['target'] == 'SYS_STATUS':
            battery_remaining = int(monitor['battery_remaining'])
            autopilot.state['battery'] = battery_remaining
            if battery_remaining < 20:
                messages.display(
                    messages.command_monitor_battery_remaining, 
                    [monitor])
            if battery_remaining < 3:
                command_queue.queue.clear()
                put_command(Command(0,'LAND',{}))

def command_telemetry_viable_status(telemetry):
    altitude = -int(round(telemetry['z']))
    speed = int(round(((telemetry['vx'] ** 2) + (telemetry['vy'] ** 2)) ** 0.5))
    autopilot.state['speed'] = speed
    autopilot.state['altitude'] = altitude
    if speed > 1:
        messages.display(
            messages.command_telemetry_current_speed, 
            [speed])
    if altitude > 1:
        messages.display(
            messages.command_telemetry_current_altitude, 
            [altitude])

def command_telemetry_mode_change(telemetry):
    servo5_raw = int(telemetry['servo5_raw'])
    autopilot_mode = autopilot.state['bee_state']
    if servo5_raw == 1100:
        autopilot_mode = 'OFF'
    elif servo5_raw == 1500:
        autopilot_mode = 'READY'
    elif servo5_raw == 1900:
        autopilot_mode = 'DESTROY'
    elif servo5_raw == 0:
        if autopilot.state['bee_state'] == 'READY' and \
            autopilot.state['altitude'] > 1:
                messages.display(
                    messages.anti_drone_system_is_detected)
                time.sleep(2)
                autopilot_mode = 'KILL'
        elif autopilot.state['bee_state'] != 'KILL':
            messages.display(
                    messages.rc_lost_can_not_switch_to_kill_mode)
    
    if autopilot_mode != autopilot.state['bee_state']:
        autopilot.state['bee_state'] = autopilot_mode
        messages.display(
                    messages.bee_state_changed_to, [autopilot_mode])
        command_queue.queue.clear()

def command_telemetry(params):
    telemetry = mavs.telemetry(params['target'])
    messages.display(messages.command_telemetry_log, [telemetry])
    
    if telemetry != {}:
        if params['target'] == 'LOCAL_POSITION_NED':
            command_telemetry_viable_status(telemetry)
        if params['target'] == 'SERVO_OUTPUT_RAW':
            command_telemetry_mode_change(telemetry)
                    
    messages.display(
        messages.command_telemetry_autopilot_state, 
        [autopilot.state])

def command_init(params):
    messages.display(messages.initializing_autopilot)
    mavs.copter_init()

def command_land(params):
    mavs.land()

def command_kill(params):
    ruined = autopilot.state['ruined']
    frame = autopilot.state['frame']
    altitude = autopilot.state['altitude']
    speed = autopilot.state['speed']
    frame = autopilot.state['frame']
    
    if ruined == False:
        # Don't follow if drone is landed
        if altitude == 0:
            return
        # or on its way
        if frame != {} and speed > 0:
            return
        
        # Find target and follow
        result = vision.get_camera_image()
        if result != {}:
            d = 0
            boxes = result.boxes.xyxy.tolist()
            if len(boxes) > 0:
                autopilot.state['target_lost'] = 0
                x1, y1, x2, y2 = boxes[0]

                if vision.is_target_close_enough(x1, y1, x2, y2) == False:
                    n, e, d, y = vision.get_ned_target(x1, y1, x2, y2, altitude)
                    autopilot.state['frame'] = (n, e, d, y)
                    messages.display(messages.command_kill_following_target,
                                                        [n, e, d, y])
                    mavs.follow_target(n, e, d, y)
                else:
                    # If close enough for bombing, - take bombing position
                    messages.display(messages.command_kill_preparing_for_attack)
                    mavs.prepare_for_attack(altitude)
                    # Then realize bomb
                    res = mavs.attack()
                    if res == True:
                        messages.display(messages.command_kill_target_attacked)
                        autopilot.state['ruined'] = True
                        # After attack we just fallback
                        messages.display(messages.command_kill_fallback)
                        mavs.fallback()
                        # Mission completed
                        command_queue.queue.clear()
                        messages.display(messages.command_kill_mission_completed)
            else:
                tl_count = int(autopilot.state['target_lost'])
                messages.display(messages.command_kill_target_lost)
                autopilot.state['target_lost'] = int(tl_count + 1)
                D_coord = vision.get_altitude_correction(altitude)
                d = mavs.target_search(tl_count, D_coord)
            
            # if altitude was changed we have to urgently update state
            if d != 0:
                put_command(
                    Command(0,'TELEMETRY',{'target':'LOCAL_POSITION_NED'}))


commands = {
    'INIT': command_init,
    'MONITOR': command_monitor,
    'TELEMETRY': command_telemetry,
    'DESTROY':command_kill,
    'LAND': command_land,
}