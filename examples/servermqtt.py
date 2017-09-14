#! /usr/bin/python3
#---------------------------------------------------------------------------
# Cedric Adjih - Inria - 2017
#---------------------------------------------------------------------------

import argparse
import time
import sys
sys.path.append("../")

from iotlabmqtt import mqttcommon

#---------------------------------------------------------------------------

COMMAND = "get-diff-time/{ref_time}"

class SimpleRequestServer(object):
    
    def __init__(self, args):
        self.args = args
        request_server = mqttcommon.RequestServer(
            args.topic, COMMAND, callback=self.cmd_get_diff_time)
        self.mqtt = mqttcommon.MQTTClient(
            self.args.server, self.args.port, [request_server],
            read_config=self.args.read_config,
            config_file_name=self.args.config)

    def cmd_get_diff_time(self, message, ref_time):
        print("request: topic={} request={} arg={}".format(
            message.topic, message.payload, ref_time))
        ref_time_float = float(ref_time)
        reply = "{}".format(time.time()-ref_time_float)
        return bytearray(reply, "utf-8")

    def run(self):
        self.mqtt.start()
        while True:
            sys.stdout.write(".")
            sys.stdout.flush()
            time.sleep(1)

#---------------------------------------------------------------------------
# Configuration

DEFAULT_SERVER = "test.mosquitto.org"
DEFAULT_PORT = 1883

parser = argparse.ArgumentParser()
parser.add_argument("--topic", type=str, default = "iotlabmqtt/test")
parser.add_argument("--server", type=str, default=DEFAULT_SERVER)
parser.add_argument("--port", type=int, default=DEFAULT_PORT)
parser.add_argument("--read-config", action="store_true", default=False)
parser.add_argument("--config", type=str, default=None)
args = parser.parse_args()

#--------------------------------------------------
# Running

server = SimpleRequestServer(args)
server.run()

#---------------------------------------------------------------------------
