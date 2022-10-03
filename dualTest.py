import pyzed.sl as sl
import sys
from signal import signal, SIGINT
import pyrealsense2 as rs




def handler(signal_received, frame):
    zed.disable_recording()
    zed.close()
    try:
        pipeline.stop()
    except:
        print('No Pipeline')
    sys.exit(0)

def initialize():
    zed = sl.Camera()
    signal(SIGINT, handler)
    init = sl.InitParameters()
    init.camera_resolution = sl.RESOLUTION.HD1080
    init.camera_fps = 30
    init.depth_mode = sl.DEPTH_MODE.NONE

    status = zed.open(init)
    if status != sl.ERROR_CODE.SUCCESS:
        print(repr(status))
        exit(1) 
    # Enable recording with the filename specified in argument
    zed_output = 'zed.svo'
    intel_output = 'intel.bag'
    recording_param = sl.RecordingParameters(zed_output, sl.SVO_COMPRESSION_MODE.H264)
    err = zed.enable_recording(recording_param)
    if err != sl.ERROR_CODE.SUCCESS:
        print(repr(err))
        exit(1)


    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 1280, 800, rs.format.bgr8, 30)
    config.enable_record_to_file(intel_output)
    pipeline.start(config)
    return pipeline, zed

def start_recording(pipeline, zed, time):
    framesCount = 0
    frames = time*30
    while framesCount < frames:
        frames = pipeline.wait_for_frames()
        # Each new frame is added to the SVO file
        zed.grab()
        framesCount += 1
    return pipeline, zed