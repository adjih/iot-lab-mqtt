#! /usr/bin/python3
#---------------------------------------------------------------------------
# Cedric Adjih - Inria - 2017
#---------------------------------------------------------------------------

import argparse
import time
import sys
sys.path.append("../")

import iotlabmqtt.mqttcommon

#---------------------------------------------------------------------------
# Configuration

DEFAULT_SERVER = "test.mosquitto.org"
DEFAULT_PORT = 1883

parser = argparse.ArgumentParser()
parser.add_argument("--topic-to", type=str, default = "iotlabmqtt/test/status")
parser.add_argument("--topic-from", type=str, default = "iotlabmqtt/test/in")
parser.add_argument("--server", type=str, default=DEFAULT_SERVER)
parser.add_argument("--port", type=int, default=DEFAULT_PORT)
parser.add_argument("--read-config", action="store_true", default=False)
parser.add_argument("--config", type=str, default=None)
args = parser.parse_args()


#--------------------------------------------------
# Actual code

def handle_topic_from(message):
    print("{}> {}".format(message.topic, message.payload))

topics = [iotlabmqtt.mqttcommon.Topic(args.topic_from, handle_topic_from)]
client = iotlabmqtt.mqttcommon.MQTTClient(
    args.server, args.port, topics=topics,
    read_config=args.read_config, config_file_name=args.config)
client.start()

print("- To interact with this process, you can use:")
info_vars = vars(args)
info_vars["server"] = client.server
info_vars["port"] = client.port
print("mosquitto_sub -h {server} -p {port} -t {topic_to} ..."
      .format(**info_vars))
print("mosquitto_pub -h {server} -p {port} -t {topic_from} -l ..."
      .format(**info_vars))

while True:
    msg = "hello %s" % time.time()
    client.publish(args.topic_to, bytearray(msg, "utf-8"))    
    time.sleep(1)

#---------------------------------------------------------------------------
