#! /usr/bin/python3
#---------------------------------------------------------------------------
# Cedric Adjih - Inria - 2017

import argparse
import time
import sys
sys.path.append("../")

from iotlabmqtt import mqttcommon

#---------------------------------------------------------------------------

class SimpleRequestClient(object):
    
    def __init__(self, args):
        self.args = args
        self.request_client = mqttcommon.RequestClient(
            args.topic, args.command,
            clientid="someclientid")
        self.mqtt = mqttcommon.MQTTClient(
            self.args.server, self.args.port, [self.request_client])

    def cmd_get_time(self, *args):
        print(args)

    def run(self):
        self.mqtt.start()
        while True:
            data = self.request_client.request(self.mqtt, "...", timeout=0.5)
            print("request-reply: {}".format(data))
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

server = SimpleRequestClient(args)
server.run()

#---------------------------------------------------------------------------
