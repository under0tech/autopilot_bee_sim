import time
import definitions as vars
from pymavlink import mavutil

command_delays =  {
    'disconnect': 0.2,
    'land' : 10,
    'fallback': 3,
    'prepare_for_attack': 1,
    'attack': 1,
    'target_search' : 0.5
}

def wait_for_execution(target, delay=0):
    if delay == 0:
        delay = command_delays.get(target)
    time.sleep(delay)

def connect(system=255):
    master = mavutil.mavlink_connection(vars.mavlink_url, 
                                        source_system=system)
    vehicle = master.wait_heartbeat()
    return master, vehicle

def disconnect(master):
    wait_for_execution('disconnect')
    master.close()

def send_message_to_gc(message):
    master, vehicle = connect(1)
    master.mav.statustext_send(
        mavutil.mavlink.MAV_SEVERITY_NOTICE, message.encode())
    disconnect(master)

def copter_init():
    master, vehicle = connect(1)
    master.mav.request_data_stream_send(
    master.target_system,
    master.target_component,
    mavutil.mavlink.MAV_DATA_STREAM_ALL, 1, 1)
    disconnect(master)

def land():
    master, vehicle = connect()
    print("Landing!")
    master.mav.command_long_send(
        master.target_system,
        master.target_component,
        mavutil.mavlink.MAV_CMD_NAV_LAND,
        0,
        0, 0, 0, 0, 0, 0, 0)

    wait_for_execution('land')
    disconnect(master)

def telemetry(target):
    master, vehicle = connect(1)
    msg = master.recv_match(type=target, blocking=False)
    telemetry = {}
    if msg is not None and msg.get_srcSystem() == 1 \
        and msg.get_srcComponent() == 1:
            telemetry = msg.to_dict()
    disconnect(master)
    return telemetry

def fallback():
    master, vehicle = connect()
    print("Fallback (10m back and left, 10m up)!")
    msg = master.mav.set_position_target_local_ned_encode(
        0, 0, 0, 9, 0b110111111000, -10, -10, -10, 0, 0, 0, 0, 0, 0, 0, 0
    )
    master.mav.send(msg)

    wait_for_execution('fallback')
    disconnect(master)

def prepare_for_attack(altitude):
    master, vehicle = connect()
    target_altitude = altitude - 5
    print(f"Preparing for attack, target altitude {target_altitude}m")
    msg = master.mav.set_position_target_local_ned_encode(
        0, 0, 0, 9, 0b110111111000, 0, 0, target_altitude, 0, 0, 0, 0, 0, 0, 0, 0
    )
    master.mav.send(msg)

    wait_for_execution('prepare_for_attack')
    disconnect(master)

def attack():
    master, vehicle = connect()
    msg = master.mav.command_long_encode(
            master.target_system,
            master.target_component,
            mavutil.mavlink.MAV_CMD_DO_SET_SERVO,
            0,
            6,  # Param 1 (AUX channel number)
            1100,  # Param 2,
            0, 0, 0, 0, 0)
    master.mav.send(msg)    

    wait_for_execution('attack')
    disconnect(master)
    return True

def follow_target(n_coord, e_coord, d_coord, yaw_angle):
    master, vehicle = connect()
    msg = master.mav.set_position_target_local_ned_encode(
        0, 0, 0, 9, 3576,
        n_coord,
        e_coord,
        d_coord,
        1, 0, 0, 0, 0, 0, yaw_angle, 0)
    master.mav.send(msg)

    # waiting for command to be executed
    delay = int(n_coord / 7 + 1)
    wait_for_execution(None, delay)

    disconnect(master)

def target_search(target_lost_count, D_coord):
    master, vehicle = connect()
    
    yaw_angle = 0 
    d = 0
    if target_lost_count > vars.target_lost_limit:
        yaw_angle = 0.7854 # 15 deg
        d = D_coord
    
    msg = master.mav.set_position_target_local_ned_encode(
        0, 0, 0, 9, 3576,
        -2,
        0,
        d,
        1, 0, 0, 0, 0, 0, yaw_angle, 0)
    master.mav.send(msg)

    wait_for_execution('target_search')
    disconnect(master)
    return d