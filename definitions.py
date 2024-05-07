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