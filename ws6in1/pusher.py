#!/bin/env python3

import ws6in1

from influxdb_client import InfluxDBClient, Point
import paho.mqtt.client as mqtt

import configparser
import argparse
import logging
import time

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser()
    parser.add_argument("config_file")
    args = parser.parse_args()
    config = configparser.ConfigParser()
    config.read(args.config_file)
    logging.info("read config")

    interval = config["ws6in1"].getfloat("interval", 30.0)
    model = config["ws6in1"]["model"]
    driver = ws6in1.ws6in1(model)

    exclude_keys = ["usUnits", "dateTime"]

    influx_client = InfluxDBClient.from_config_file(args.config_file)
    write_api = influx_client.write_api()
    bucket = config["influx2"]["bucket"]
    logging.info("connected to influxdb")

    topic_prefix = config["mqtt"]["topic_prefix"]
    mqtt_client = mqtt.Client()
    if "ca_cert" in config["mqtt"]:
        mqtt_client.tls_set(ca_certs=config["mqtt"]["ca_cert"], certfile=config["mqtt"]["cert"], keyfile=config["mqtt"]["key"])
    if "password" in config["mqtt"]:
        mqtt_client.username_pw_set(username=config["mqtt"]["username"], password=config["mqtt"]["password"])
    mqtt_client.connect(config["mqtt"]["host"], config["mqtt"].getint("port"))
    mqtt_client.loop_start()

    try:
        for result in driver.genLoopPackets():
            # remove all keys with None values and the excluded keys
            clean_result = {k: v for k, v in result.items() if v is not None and k not in exclude_keys}
            point = Point("bresser")
            for key in clean_result:
                point = point.field(key, clean_result[key])
                mqtt_client.publish(topic_prefix + model + "/" + key, clean_result[key])
            point = point.time(clean_result["datetime"])

            write_api.write(bucket=bucket, record=point)
            write_api.flush()
            logging.debug(f"wrote {clean_result} to influxDB and mqtt")
            time.sleep(interval)
    except KeyboardInterrupt:
        write_api.flush()
        influx_client.close()
        logging.warning("exiting due to keyboard interrupt")


