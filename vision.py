import cv2
import airsim
import definitions as vars

from datetime import datetime
from ultralytics import YOLO

model = YOLO(vars.vision_model)
image_width = vars.camera_width
image_height = vars.camera_height
following_altitude = vars.following_altitude
yaw_conversion_factor = 0.002
threshold_percentage=0.03
approach_factor = 0.8

def get_camera_image():
    result = {}
    png_file_name = f'logs/img_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.png'

    if vars.airsim_camera:
        client = airsim.MultirotorClient() # SIM
        png_image = client.simGetImage(vars.video_source, airsim.ImageType.Scene)
        if png_image is not None:
            img = cv2.imdecode(airsim.string_to_uint8_array(png_image), cv2.COLOR_BGR2RGB)
            
            results = model(img, classes=vars.vision_classes)
            frame = results[0].plot()
            cv2.imwrite(png_file_name, frame)
            result = results[0]
        client.enableApiControl(False)
    else:
        cam = cv2.VideoCapture(vars.video_source)
        if not cam.isOpened():
            return result
        success, frame = cam.read()
        if success:
            results = model(frame, classes=vars.vision_classes)
            anotated_frame = results[0].plot()
            cv2.imwrite(png_file_name, anotated_frame)
            result = results[0]
        cam.release()
        cv2.destroyAllWindows()

    return result

def get_ned_coordinates(x1, y1, x2, y2, altitude):
    target_x = (x1 + x2) / 2
    target_y = (y1 + y2) / 2

    relative_x = (2 * target_x / image_width) - 1
    relative_y = (2 * target_y / image_height) - 1

    N_coord = relative_y * altitude
    E_coord = relative_x * altitude
    
    D_coord = get_altitude_correction(altitude)

    return N_coord, E_coord, D_coord

def get_yaw_angle(x1, y1, x2, y2):
    target_x = (x1 + x2) / 2
    yaw_angle = (target_x - image_width / 2) * yaw_conversion_factor

    return yaw_angle

def get_target_threshold_area(x1, y1, x2, y2):
    target_area = (x2 - x1) * (y2 - y1)
    threshold_area = \
        image_width * image_height * threshold_percentage

    return target_area, threshold_area

def is_target_close_enough(x1, y1, x2, y2):
    target_area, threshold_area = \
        get_target_threshold_area(x1, y1, x2, y2)
    
    return target_area > threshold_area

def get_ned_target(x1, y1, x2, y2, altitude):
    N_coord, E_coord, D_coord = get_ned_coordinates(
        x1, y1, x2, y2, altitude)
    yaw_angle = get_yaw_angle(x1, y1, x2, y2)
    target_area, threshold_area = \
        get_target_threshold_area(x1, y1, x2, y2)
    long_factor = threshold_area / target_area

    return round(N_coord * long_factor * approach_factor, 4), \
        round(E_coord, 4), round(D_coord, 4), round(yaw_angle, 4)

def get_altitude_correction(altitude):
    D_coord = 0
    if altitude > 0 and altitude not in [following_altitude, \
                                         following_altitude-1, \
                                         following_altitude+1]:
        D_coord = int(altitude - following_altitude)
        if D_coord > following_altitude:
            D_coord = following_altitude
    return D_coord