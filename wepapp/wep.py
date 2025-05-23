#! /usr/bin/env python

#run only one video at a time. stop processing video when press stop and save the video which is processed until
import GPUtil
import tensorflow as tf 
#from wepcore.detection_yolo11 import detect
from wepcore.detection import detect
import wepcore.constants as cons
import logging as log
import wepcore.setup as cfg
import typing

log.info("Setup complete ({})".format(cfg.version_info))

# comment out below line to enable tensorflow outputs
#os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
physical_devices = tf.config.experimental.list_physical_devices('GPU')
if len(physical_devices) > 0:
    tf.config.experimental.set_memory_growth(physical_devices[0], True)
    log.info("GPU devices found: {}".format(physical_devices))
else:
    log.info("No GPU devices found")

msg: typing.Dict[str,typing.Dict] = {}
msg[cons.PAYLOAD] = {}
payload = msg[cons.PAYLOAD]
payload[cons.VIDEO_LINK] = cfg.source.get(cons.VIDEO_LINK)        #'/Users/reed/Stuff/ereed/customers/iterate/wep/redo/wepcache/AR_15.mp4'
payload[cons.BUILDING] = cfg.source.get(cons.BUILDING)            #'Building A'
payload[cons.VIDEO_TYPE] = cfg.source.get(cons.VIDEO_TYPE)        #'mp4'
payload[cons.FRIENDLY_NAME] = cfg.source.get(cons.FRIENDLY_NAME)  #'friendly_name'
payload[cons.FILE_ORIGINAL_NAME] = cfg.source.get(cons.FILE_NAME) #'9mm_fast_walk.mp4'
payload[cons.LATITUDE] = cfg.source.get(cons.LATITUDE) #
payload[cons.LONGITUDE] = cfg.source.get(cons.LONGITUDE) #

log.info("Input request: {}".format(payload))

msg_local = msg.copy()
msg_passing: typing.List[str] = []

try:
    if (cfg.source.get(cons.VIDEO_TYPE) in cons.VIDEO_STREAM_TYPES):
        #for every 5*60*fps frames (5 mins) the python_function will break, save the video and come out. Again will save the next 5*60*fps frames as new video.....Thats y for every 5*60*fps frames we r exiting from python_function and restarting the python_function to save last 5 mins frames.
        log.info('Detection for video stream starts...')
    elif (cfg.source.get(cons.VIDEO_TYPE) in cons.VIDEO_FILE_TYPES):
        log.info('Detection for video starts...')

    log.info("GPU Utilization before: ")
    GPUtil.showUtilization()
        
    summary_results = detect(msg,msg_local,msg_passing)
    log.info("Response: {} {}".format(summary_results, type(summary_results)))

    log.info("GPU Utilization after:")
    GPUtil.showUtilization()

    if 'data_weapon' in summary_results.keys():
        data_weapon = summary_results['data_weapon']
        log.info("Response: {} {}".format(data_weapon, type(data_weapon)))
        #push.do_push(json.dumps(data_weapon))

except Exception as e:
    log.error("Processing exception occurred: {}".format(e))
    pass
