#! /usr/bin/python3
#---------------------------------------------------------------------------
# Cedric Adjih - Inria - 2017
#---------------------------------------------------------------------------

from __future__ import print_function

import argparse
import time
import sys
import uuid
sys.path.append("../")

from iotlabmqtt import mqttcommon

#---------------------------------------------------------------------------

COMMAND = "get-diff-time/{ref_time}"

class SimpleRequestClient(object):
    
    def __init__(self, args):
        self.args = args
        self.request_client = mqttcommon.RequestClient(
            args.topic, COMMAND, clientid=str(uuid.uuid4()))
        self.mqtt = mqttcommon.MQTTClient(
            self.args.server, self.args.port, [self.request_client])

    def run(self):
        self.mqtt.start()
        while True:
            request_content = bytearray("...", "utf-8")
            ref_time_str = "{}".format(time.time())
            data = self.request_client.request(
                self.mqtt, request_content, ref_time=ref_time_str, timeout=0.5)
            str_data = data.decode("utf-8")
            print("request-reply: {}".format(str_data))
            time.sleep(1)

#---------------------------------------------------------------------------
# Configuration

DEFAULT_SERVER = "test.mosquitto.org"
DEFAULT_PORT = 1883

parser = argparse.ArgumentParser()
parser.add_argument("--topic", type=str, default = "iotlabmqtt/test")
parser.add_argument("--server", type=str, default=DEFAULT_SERVER)
parser.add_argument("--port", type=int, default=DEFAULT_PORT)
args = parser.parse_args()

#--------------------------------------------------
# Running

server = SimpleRequestClient(args)
server.run()

#---------------------------------------------------------------------------
