#! /usr/bin/python3
#---------------------------------------------------------------------------
# Cedric Adjih - Inria - 2017
# Inspired from G.H.:
# https://github.com/iot-lab/iot-lab-mqtt/blob/master/iotlabmqtt/clients/log.py
#---------------------------------------------------------------------------

import argparse
import time
import sys
import uuid
sys.path.append("../")

from iotlabmqtt import mqttcommon
from iotlabmqtt.clients import common as clientcommon

#---------------------------------------------------------------------------

COMMAND = "get-diff-time/{ref_time}"

class SimpleShell(clientcommon.CmdShell):
    """Shell for the SimpleRequestServer"""
    
    def __init__(self, args):
        super(self.__class__, self).__init__()
        self.args = args
        self.get_time_client = mqttcommon.RequestClient(
            args.topic, COMMAND, clientid=str(uuid.uuid4()))
        self.mqtt = mqttcommon.MQTTClient(
            self.args.server, self.args.port, [self.get_time_client],
            read_config=self.args.read_config,
            config_file_name=self.args.config)

    #--------------------------------------------------
    # Command 'difftime' (mqtt: 'get-diff-time')
    
    def do_difftime(self, arg_list):
        ref_time_str = "{}".format(time.time())
        data = self.get_time_client.request(
            self.mqtt, b"...", ref_time = ref_time_str, timeout=2)
        data_str = data.decode("utf-8")
        print("time: {}".format(data_str))
    
    def help_difftime(self):
        print("difftime\n  Retrieve time diff from server (through mqtt)")
    
    #--------------------------------------------------
        
    def run(self):
        self.mqtt.start()
        try:
            self.cmdloop()
        except KeyboardInterrupt:
            pass
        self.mqtt.stop()
     
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

server = SimpleShell(args)
server.run()

#---------------------------------------------------------------------------
