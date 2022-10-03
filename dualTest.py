import pyzed.sl as sl
import sys
from signal import signal, SIGINT
import pyrealsense2 as rs
import time 




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

    return pipeline, zed, config

def start_recording(pipeline, zed,config,  duration):
    framesCount = 0
    framesLimit = duration*30
    start = time.time()
    pipeline.start(config)
    while time.time()-start < duration:
        zed.grab()
        if zed.grab == sl.ERROR_CODE.SUCCESS:
            zed.record()
        frames = pipeline.poll_for_frames()
        # Each new frame is added to the SVO file
        framesCount += 1
        print("Frames Count: " +  str(framesCount), end='\r')
    pipeline.stop
    zed.disable_recording()
    zed.close()
    return pipeline, zed