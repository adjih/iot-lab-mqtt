#! /usr/bin/python3
#---------------------------------------------------------------------------
# Cedric Adjih - Inria - 2017

import argparse
import time
import sys
sys.path.append("../")

from iotlabmqtt import mqttcommon

#---------------------------------------------------------------------------

class SimpleRequestServer(object):
    
    def __init__(self, args):
        self.args = args
        request_server = mqttcommon.RequestServer(
            args.topic, args.command, callback=self.cmd_get_time)
        self.mqtt = mqttcommon.MQTTClient(
            self.args.server, self.args.port, [request_server])

    def cmd_get_time(self, message):
        print("request: topic={} request={}".format(
            message.topic, message.payload))
        return "{}".format(time.time())

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
parser.add_argument("--topic", type=str, default = "/iotlabmqtt/test")
parser.add_argument("--command", type=str, default = "get-time")
parser.add_argument("--server", type=str, default=DEFAULT_SERVER)
parser.add_argument("--port", type=int, default=DEFAULT_PORT)
args = parser.parse_args()

#--------------------------------------------------
# Running

server = SimpleRequestServer(args)
server.run()

#---------------------------------------------------------------------------
